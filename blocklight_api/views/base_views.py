from blocklight_api.filters import DatasetFilterBackend
from blocklight_api.mixins import UserSpecificFilteringMixin, ShopifySelectedStoreFilteringMixin
from blocklight_api.serializers.core_serializers import ChartDataSerializer
from allauth.socialaccount.models import SocialAccount

from datetime import datetime
from dateutil.relativedelta import relativedelta

from django.core.exceptions import FieldError
from django.core.paginator import Paginator
from django.db.models import Count, Avg, Sum, Min, Max, StdDev, Value, CharField, FloatField

from functools import reduce
import operator
from pytz import timezone

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.settings import api_settings
import logging
logger = logging.getLogger(__name__)


class BaseDatasourceViewSet(UserSpecificFilteringMixin, ShopifySelectedStoreFilteringMixin,
                            viewsets.ReadOnlyModelViewSet):

    filter_backends = api_settings.DEFAULT_FILTER_BACKENDS \
        + UserSpecificFilteringMixin.filter_backends \
        + ShopifySelectedStoreFilteringMixin.filter_backends \
        + [DatasetFilterBackend]

    required_subclass_fields = [
        'queryset',
        'serializer_class',
        'chart_data_serializer',
        'since_until_field',
    ]

    # TODO: Consider better design
    dynamic_groupby_map = {
        'hour_dynamic': 'hours',
        'day_dynamic': 'days',
        'week_dynamic': 'weeks',
        'month_dynamic': 'months',
        'year_dynamic': 'years',
        'timerange_dynamic': 'all'
    }

    def __init__(self, *args, **kwargs):
        super(BaseDatasourceViewSet, self).__init__(*args, **kwargs)
        for f in self.required_subclass_fields:
            if not hasattr(self, f):
                raise AttributeError(
                    "The subclass of {} needs to define field: {}".format(
                        self.__class__, f
                    )
                )

    def get_since_until_field(self):
        if not getattr(self, 'since_until_field', None):
            return AttributeError("You need to specify since_until_field.")
        return self.since_until_field

    def _get_chart_data_serializer(self, *args, **kwargs):
        return ChartDataSerializer(*args, **kwargs)

    def _get_intervals(self, start_date, end_date, interval):
        tz = timezone('UTC')
        intervals = []

        if interval == 'all':
            interval_start_date = start_date.replace(
                tzinfo=tz, 
                hour=0, 
                minute=0, 
                second=0, 
                microsecond=0
            )

            interval_end_date = end_date.replace(
                tzinfo=tz, 
                hour=23, 
                minute=59, 
                second=59, 
                microsecond=999999
            )

            intervals.append((interval_start_date, interval_end_date))

        else: 
        
            end_date = end_date.replace(tzinfo=tz)

            interval_start_date = start_date.replace(
                tzinfo=tz, 
                hour=0, 
                minute=0, 
                second=0, 
                microsecond=0
            )
        
            interval_end_date = (
                start_date + relativedelta(**{interval: 1})
            ).replace(
                tzinfo=tz, 
                hour=23, 
                minute=59, 
                second=59, 
                microsecond=999999
            )
        
            while interval_start_date.date() < end_date.date():
                intervals.append((interval_start_date, interval_end_date))
                interval_start_date = interval_end_date.replace( 
                    hour=0, 
                    minute=0, 
                    second=0, 
                    microsecond=0
                )
                interval_end_date = (interval_start_date + relativedelta(**{interval: 1})).replace(
                    hour=23, 
                    minute=59, 
                    second=59, 
                    microsecond=999999
                )
        
        return intervals

    
    def parse_filters_param(self):
        """
            Returns dict of field[__operation] -> value
        """
        fltrs_parsed = {}

        # help(self.request)
        # Eg: fltrs='((user_iden=61)and(total_price__gt=0))'
        # Eg: fltrs='(user_iden=61)and(total_price__gt=0)'
        # Eg: fltrs='total_price__gt=0'
        # TODO: Simplify or implement Interpreter design pattern for full
        #      boolean syntax handling ('and' and 'or' ops)
        fltrs = self.request.query_params.get('filter', None)
        if not fltrs:
            return fltrs_parsed

        # if there is only one expression it may or may not have parantheses
        #    around it
        if fltrs.count('=') == 1:
            fltrs = fltrs.strip('(').strip(')')

            f_spl = fltrs.split('=')
            responseIfOneFilter = {
                # django knows __lt, __gt etc. but not __eq
                f_spl[0] if not f_spl[0].endswith('_eq') else f_spl[0][:-4]:
                f_spl[1].strip('"').strip("'")
            }
            fltrs_parsed.update(responseIfOneFilter)
            return fltrs_parsed

        fltrs = fltrs.strip()
        if (fltrs[0] != '(') or (fltrs[-1] != ')'):
            raise ValueError(
                'Wrong format of filter expession: {} Use format like:'
                + ' ((price__lt=50)and(total_price__gt=100))'.format(fltrs)
            )

        fltrs = fltrs[1:] if fltrs[:2] == '((' else fltrs
        fltrs = fltrs[:-1] if fltrs[-2:] == '))' else fltrs

        for f in fltrs.split('and'):
            if (f[0] != '(') or (f[-1] != ')'):
                raise ValueError(
                    'Wrong format of filter expession: {} Use format like:'
                    + ' ((price__lt=50)and(total_price__gt=100))'.format(fltrs)
                )
            f_spl = f[1:-1].split('=')
            if f_spl and f_spl[0]:
                fltrs_parsed[
                    # django knows __lt, __gt etc. but not __eq
                    f_spl[0] if not f_spl[0].endswith('_eq') else f_spl[0][:-4]
                ] = f_spl[1].strip('"').strip("'")
        return fltrs_parsed

    def _translate_dynamic_datetime_term(self, dt_term, dt_sign='+'):
        """
        Returns two different types - datetime or relativedelta
        Translates
                - datetime_string,
                - 'now',
                - '1y/m/d'
            to datetime or relativedelta.
        """
        datetime_format = '%Y-%m-%d %H:%M:%S%z'
        dynamic_expression_map = {
            'y': 'years',
            'm': 'months',
            'd': 'days',
        }

        try:
            return datetime.strptime(dt_term, datetime_format)
        except ValueError:
            if (not dt_term[-1] in dynamic_expression_map.keys()) and (
                    dt_term != 'now'):
                raise ValueError(
                    "{} not matching format {} or \"now, {}\"".format(
                        dt_term,
                        datetime_format,
                        ', '.join(dynamic_expression_map.keys())
                    )
                )

        if dt_term == 'now':
            return datetime.now()

        return relativedelta(**{
            dynamic_expression_map[dt_term[-1]]:
                int('{}{}'.format(dt_sign, dt_term[:-1]))
        })

    def _translate_dynamic_datetime(self, dt_expr):
        """
        Translates datetime expression to datetime object.
        Examples:
            'now'
            '2019-12-28 00:00:00-0000'
            'now\-1d'
            '2019-12-28 00:00:00-0000\-1y'
            'now\-1y\+1m\-3d'
            '2019-11-28 00:00:00-0000\-1m\+3d'
        Args:
            dt_expr: Datetime expression. Eg. 'now\-1y\+1m\-3d'
        Returns:
            datetime: Translated datetime
        """
        # dt = r'now'
        # dt = r'now\-1y'
        # dt = r'now\-1m'
        # dt = r'now\-1d'
        # dt = r'2019-12-28 00:00:00-0000\-1y'
        # dt = r'2019-12-28 00:00:00-0000\-1m'
        # dt = r'now\-1y\+1m\-3d'
        # dt = r'2019-11-28 00:00:00-0000\-1m\+3d'
        # dt = r'2019-03-31 00:00:00-0000\+1m'
        # dt = r'2019-03-31 00:00:00-0000\-1m'

        # Create list of tuples of ('+/-', 'term')
        #    eg: [('+', '2019-12-28 00:00:00-0000'), ('-', '1m'), ('+', '3d')]
        dt_splited_nested = [
            [
                ('+' if (i == 0) else '-', dt_spl_minus)
                for i, dt_spl_minus in enumerate(
                    dt_spl_plus_tpl[1].split(r'\-')
                )
            ]
            for dt_spl_plus_tpl in [
                ('+', dt_spl_plus)
                for dt_spl_plus in dt_expr.split(r'\+')
            ]
        ]

        dt_tuples = [i for j in dt_splited_nested for i in j]

        dt_terms = map(
            lambda dt_tpl: self._translate_dynamic_datetime_term(
                dt_tpl[1], dt_tpl[0]
            ),
            dt_tuples
        )

        return reduce(operator.add, dt_terms)

    def parse_timerange_params(self):
        """
            Returns dict of since, until vals
            It translates marks for dynamic time for:
                - now
                - (now/datetime)(-/+)Xd
                - (now/datatime)(-/+)Xm
                - (now/datatime)(-/+)Xy
                - (now/datatime)(-/+)Xy(-/+)Xm...
        """
        # Eg: fltrs='((user_iden=61)and(total_price__gt=0))'
        # Eg: fltrs='(user_iden=61)and(total_price__gt=0)'
        # Eg: fltrs='total_price__gt=0'
        # TOD: Simplify or implement Interpreter design pattern for full
        #      boolean syntax handling ('and' and 'or' ops)

        tr_since = self.request.query_params.get('timerange-since', None)
        tr_until = self.request.query_params.get('timerange-until', None)

        tr_parsed = {
            'since': self._translate_dynamic_datetime(tr_since)
            if tr_since else None,
            'until': self._translate_dynamic_datetime(tr_until)
            if tr_since else None,
        }

        return tr_parsed

    def _parse_aggs_param(self, aggs):
        func_mapping = {
            'count': Count,
            'avg': Avg,
            'sum': Sum,
            'min': Min,
            'max': Max,
            'stddev': StdDev
        }

        parsed_aggs = {}

        for agg in aggs:
            agg_spl = agg.strip().split('__')
            if (
                (agg_spl[-1].lower() == 'distinct') and (len(agg_spl) < 3)
            ) or (len(agg_spl) < 2):
                raise ValueError(
                    "For aggregation use format"
                    " '<field>__<function>[__distinct]'. eg: price__sum."
                    " Notice there are TWO underscores between"
                    " field and function."
                )

            if agg_spl[-1].lower() == 'distinct':
                agg_distinct = True
                agg_func = agg_spl[-2]
                agg_field = '__'.join(agg_spl[:-2])
            else:
                agg_distinct = False
                agg_func = agg_spl[-1]
                agg_field = '__'.join(agg_spl[:-1])

            if agg_func not in func_mapping:
                raise ValueError(
                    "Function '{}' not found."
                    " Available functions are: {}".format(
                        agg_func, func_mapping.keys()
                    )
                )

            parsed_aggs[agg] = func_mapping[agg_func](
                agg_field, distinct=agg_distinct, output_field=FloatField()
            )

        return parsed_aggs

    @action(detail=False, methods=['get'])
    def chart_data(self, request, **kwargs):
        # /?group-by=week_dynamic,buyer_accepts_marketing&aggregate=sum(total_price),avg(total_price)
        # /?filter=((user_iden=61)and(total_price__gt=0))&group-by=week_dynamic,buyer_accepts_marketing&aggregate=total_price__sum,total_price__avg  # noqa
        # /?filter=((user_iden=61)and(total_price__gt=0))&group-by=email,buyer_accepts_marketing&aggregate=total_price__sum,total_price_avg  # noqa
        # http://localhost:8000/api/v1/shopify_orders/chart_data/?filter=((user_iden=61)and(total_price__gt=0))&group-by=email,buyer_accepts_marketing&aggregate=total_price__sum,total_price__avg  # noqa
        # http://localhost:8000/api/v1/shopify_orders/chart_data/?filter=((user_iden=61)and(total_price__gt=0)and(created_at__gt='2019-09-01 00:00:00-0000')and(created_at__lt='2019-12-31 00:00:00-0000'))&group-by=email,buyer_accepts_marketing&aggregate=stotal_price__sum,total_price__avg  # noqa
        # http://localhost:8000/api/v1/shopify_orders/chart_data/?filter=((user_iden=61)and(total_price__gt=0)and(created_at__gt='2019-09-01 00:00:00-0000')and(created_at__lt='2019-12-31 00:00:00-0000'))&group-by=week_dynamic,email,buyer_accepts_marketing&aggregate=total_price__sum,total_price__avg  # noqa
        # http://localhost:8000/api/v1/shopify_orders/chart_data/?filter=((user_iden=61)and(total_price__gt=0)and(since__eq='2019-09-01 00:00:00-0000')and(until__eq='2019-12-31 00:00:00-0000'))&group-by=week_dynamic,email,buyer_accepts_marketing&aggregate=total_price__sum,total_price__avg  # noqa

        # create parser methods in the view for grps and aggs
        grps = request.query_params.get('group-by', None)
        aggs = request.query_params.get('aggregate', None)
        try:
            fltrs = self.parse_filters_param()
        except ValueError as e:
            return Response(
                [{"message": ". ".join(e.args)}],
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            timerange = self.parse_timerange_params()
        except ValueError as e:
            return Response(
                [{"message": ". ".join(e.args)}],
                status=status.HTTP_400_BAD_REQUEST
            )

        if (grps is None) or (aggs is None):
            return Response(
                [
                    # need to return array to enable filter form on REST WEB UI
                    {
                        "message":
                            "Parameter 'group-by' or 'aggregate' is missing."
                    }
                ],
                status=status.HTTP_400_BAD_REQUEST
            )

        grps = grps.split(',') if grps else []
        aggs = aggs.split(',') if aggs else aggs
        try:
            aggs = self._parse_aggs_param(aggs)
        except ValueError as e:
            return Response(
                [{"message": ". ".join(e.args)}],
                status=status.HTTP_400_BAD_REQUEST
            )

        if (len(grps) == 0) or (len(aggs) == 0):
            return Response(
                [{
                    "message":
                        "Parameter 'group-by' or 'aggregate' is missing."
                }],
                status=status.HTTP_400_BAD_REQUEST
            )

        if len(set(self.dynamic_groupby_map.keys()) & set(grps)) > 1:
            return Response(
                [{
                    "message": (
                        "There is only one possible dynamic grouping at once"
                    )
                }],
                status=status.HTTP_400_BAD_REQUEST
            )

        # TODO: Consider better design
        if (
            len(set(self.dynamic_groupby_map.keys()) & set(grps))
            and (grps[0] not in self.dynamic_groupby_map.keys())
        ):
            return Response(
                [{
                    "message": (
                        "Grouping week_dynamic is supported only as"
                        " a first group.")
                }],
                status=status.HTTP_400_BAD_REQUEST
            )

        if grps[0] in self.dynamic_groupby_map.keys():
            if (timerange['since'] is None) or (timerange['until'] is None):
                return Response(
                    [{
                        "message": (
                            "(Currently)When using week_dynamic, "
                            "timerange-since and timerange-until are required."
                        )
                    }],
                    status=status.HTTP_400_BAD_REQUEST
                )

        qs = self.filter_queryset(self.get_queryset())

        # TODO: Consider better design
        if grps[0] in self.dynamic_groupby_map.keys():

            intervals = self._get_intervals(
                timerange['since'],
                timerange['until'],
                self.dynamic_groupby_map[grps[0]]
            )
            s_u_field = self.get_since_until_field()

            try:
                chart_data = reduce(
                    lambda a, b: a.union(b),
                    map(
                        lambda interval: qs.filter(**{
                            **{
                                '{}__gt'.format(s_u_field): interval[0],
                                '{}__lt'.format(s_u_field): interval[1],
                            },
                            **fltrs
                        }
                        ).annotate(
                            **{
                                '{}__gt'.format(s_u_field):
                                    Value(interval[0], output_field=CharField(max_length=30)),  # noqa
                                '{}__lt'.format(s_u_field):
                                    Value(interval[1], output_field=CharField(max_length=30))  # noqa
                            }
                        ).values(*
                            grps[1:] + \
                            [
                                '{}__gt'.format(s_u_field),
                                '{}__lt'.format(s_u_field)
                            ]
                        ).annotate(
                            **aggs
                        ).order_by(),
                        intervals
                    )
                )
            except FieldError as e:
                # There can be wrong name of field. In that case the exception
                # will print problematic field together with all available
                # fields
                return Response(
                    [{"message": ". ".join(e.args)}],
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            try:
                chart_data = qs.filter(
                    **fltrs
                ).values(
                    *grps
                ).annotate(
                    **aggs
                ).order_by()
            except FieldError as e:
                # There can be wrong name of field. In that case the exception
                # will print problematic field together with all available
                # fields
                return Response(
                    [{"message": ". ".join(e.args)}],
                    status=status.HTTP_400_BAD_REQUEST
                )

        if not len(chart_data):
            return Response([])

        fields = chart_data[0].keys()

        page_chart_data = self.paginate_queryset(chart_data)

        if page_chart_data is not None:
            serializer = self._get_chart_data_serializer(
                page_chart_data,
                fields=fields,
                many=True
            )
            return self.get_paginated_response(serializer.data)

        serializer = self._get_chart_data_serializer(
            chart_data,
            fields=fields,
            many=True
        )

        return Response(serializer.data)


class TimelineViewSet(viewsets.ModelViewSet):

    PAGE_SIZE = 100
    filter_backends = api_settings.DEFAULT_FILTER_BACKENDS

    required_subclass_fields = {
        "basename",
        "src",
        "route_name",
        "serializer_class",
        "get_queryset",
        "ts_field",
        "composite_key"
    }

    def __init__(self, *args, **kwargs):
        super(TimelineViewSet, self).__init__(*args, **kwargs)
        for f in self.required_subclass_fields:
            if not hasattr(self, f):
                raise AttributeError(
                    "The subclass of {} needs to define field: {}".format(
                        self.__class__, f
                    )
                )

    def paginate_queryset(self, queryset, pn):
        paginator = Paginator(queryset, TimelineViewSet.PAGE_SIZE)
        max_page = paginator.num_pages
        page_obj = paginator.get_page(pn)
        return page_obj

    def list(self, request, *args, **kwargs):
        try:
            page = int(request.GET["page"])
        except KeyError as e:
            page = 1

        queryset = super().filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset, page)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            self.pagination_class.page = page
            self.pagination_class.request = request
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
