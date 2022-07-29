import logging
from rest_framework import filters
from functools import reduce
from django_filters import rest_framework as df_r_filters
import django_filters
from django.template.loader import render_to_string
from blocklight_api import models as blapi_models
from allauth.socialaccount.models import SocialAccount
from django.db.models import Count, Q
from django.db import transaction
from django_filters import Filter, FilterSet
from django_filters.constants import EMPTY_VALUES

from django_filters import Filter, FilterSet
from django_filters.constants import EMPTY_VALUES

logger = logging.getLogger(__name__)


class PredefinedMetricFilterSet(df_r_filters.FilterSet):
    predefined_dashboard__isnull = django_filters.BooleanFilter(
        field_name='predefined_dashboard', lookup_expr='isnull'
    )

    class Meta:
        model = blapi_models.PredefinedMetric
        fields = '__all__'


class OwnerSpecificFilterBackend(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(**view.get_owner_filter_kwargs(request))


class ShopifySelectedStoreFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        store_filter = {}
        is_shopify = 'shopify' in request.path or 'shopify' in getattr(
            view, 'route_name', "") or getattr(view, 'main_timeline', None) is True
        not_address = 'address' not in request.path
        selected_shop = None
        if is_shopify and not_address:
            shopify_accounts = SocialAccount.objects.filter(
                provider='shopify', user_id=request.user.id)

            shops = list(
                filter(
                    lambda tuple: tuple[1] == True,
                    map(
                        lambda shop: (shop, shop.extra_data.get(
                            'is_selected', None)),
                        shopify_accounts
                    )
                )
            )
            inactive = list(
                filter(
                    lambda tuple: tuple[1] != True,
                    map(
                        lambda shop: (shop, shop.extra_data.get(
                            'is_selected', None)),
                        shopify_accounts
                    )
                )
            )

            if len(shops) == 1:
                def remove_unselected(queryset):
                    for shop in inactive:

                        field = getattr(
                            view, 'social_account_field', None) + "_id"
                        fltr = {field: shop[0].id}
                        queryset = queryset.filter(~Q(**fltr))

                    return queryset

            # elif len(shops) == 0:
            #     pass

            else:
                logger.log(msg=f'{len(shops)} SHOPS ARE CURRENTLY SELECTED, \
                        AUTO SELECTING MOST RECENT', level=50)
                with transaction.atomic():
                    shopify_accounts = SocialAccount.objects.filter(
                        provider='shopify', user_id=request.user.id)

                    for shop in shopify_accounts:
                        shop.extra_data['is_selected'] = False
                        shop.save()

                    most_recent_account = shopify_accounts.last()
                    if not most_recent_account:
                        return queryset
                    most_recent_account.extra_data['is_selected'] = True
                    most_recent_account.save()
                    store_filter[getattr(view, 'social_account_field', None) +
                                 '_id'] = most_recent_account.id

            return remove_unselected(queryset)

        return queryset


class InAllFilterBackend(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """

    def filter_queryset(self, request, queryset, view):

        inall_params = list(filter(
            lambda k: k.endswith('__inall'),
            request.query_params
        ))

        if not inall_params:
            return queryset

        filtered_by_counts = reduce(
            lambda qs, k: qs.annotate(
                _cnt=Count(k[:-7])
            ).filter(
                _cnt__lte=len(request.query_params[k].split(','))
            ),
            inall_params,
            queryset
        )

        # make iterable of tuples of ((lookup_expressin, value), ...),
        # so all lookup_expressions and values can be later used in one reduce
        # operation. (for this "inall" filter, the chain of filters needs to be
        # used)
        inall_params_flat = [
            (k[:-7], v)
            for k in inall_params
            for v in request.query_params[k].split(',')
        ]

        return reduce(
            lambda qs, k_v: qs.filter(**{k_v[0]: k_v[1]}),
            inall_params_flat,
            filtered_by_counts
        )


class DatasetFilterBackend(filters.BaseFilterBackend):

    field_type_mappings = {
        "CharField": 'text',
        "TextField": 'text',
        "GenericIPAddressField": 'text',
        "DateTimeField": 'datetime',
        # (models.BooleanField),
        # (models.DateTimeField),
        # (models.EmailField),
    }

    def filter_queryset(self, request, queryset, view):
        # Eg: /?filter=((user_iden=61)and(total_price__gt=0))
        #     /?filter=((user_iden=61)and(total_price__gt=0)and(created_at__gt="2019-09-01 00:00:00-0000")and(created_at__lt="2019-12-31 00:00:00-0000"))  # noqa

        if not request.query_params.get('filter', None):
            return queryset

        fltrs_parsed = dict(filter(
            lambda kv: not kv[0].endswith('__inall'),
            view.parse_filters_param().items()
        ))

        queryset = queryset.filter(**fltrs_parsed).all()

        return queryset

    def to_html(self, request, queryset, view):
        vs = view.serializer_class()

        fields = tuple(map(
            lambda f: (
                f,
                self.field_type_mappings[
                    vs.Meta.model._meta.get_field(f).get_internal_type()
                ]
                if vs.Meta.model._meta.get_field(f).get_internal_type()
                in self.field_type_mappings
                else
                'text'
            ),
            vs.fields
        ))

        if view.action == 'chart_data':

            context = {
                'filter_fields': fields,
                'groupby_fields': (
                    'hour_dynamic',
                    'day_dynamic',
                    'week_dynamic',
                    'month_dynamic',
                    'year_dynamic',
                    'timerange_dynamic'
                ) + tuple(map(lambda ft: ft[0], fields)),
                "agg_fields_csv": ",".join(vs.fields),
                # TODO: get from view
                'supported_aggs': ('count', 'avg', 'sum', 'min', 'max', 'stddev')
                # 'since_field_name': 'created_at'
            }
            return render_to_string('blocklight_api/form_chart_data.html', context=context)

        return render_to_string('blocklight_api/form_list.html', context={'filter_fields': fields})

class ListFilter(Filter):
    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs
        value_list = value.split(",")
        qs = super().filter(qs, value_list)
        return qs

class InsightListFilter(FilterSet):
    insight = ListFilter(field_name="insight", lookup_expr="in")
    # other fields
