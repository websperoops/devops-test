from user_tiers.models import ( UserTier, Tier )
from allauth.socialaccount.models import SocialAccount
from rest_framework import views, generics, mixins, viewsets
from blocklight_api import serializers as blapi_serializers
from blocklight_api.filters import InAllFilterBackend, PredefinedMetricFilterSet
from blocklight_api.mixins import UserSpecificFilteringMixin
from blocklight_api.models import (
    Integration, Chart, BLDashboard, DashboardLayout, PredefinedIntegration,
    TimeRange, Metric, ChartType, PredefinedMetric, PredefinedMetricType,
    PredefinedChartType, PredefinedTimeRange, DataSource,
    SummaryIntegration, SummaryMetric, SummaryTimeRange, LoyaltyCode,
    TopSocialMetric, TopSocialIntegration, TopSocialTimeRange, 
)
from datetime import date
from dashboards.models import UserProfile
from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.settings import api_settings


class UserViewSet(UserSpecificFilteringMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    filterset_fields = '__all__'
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = blapi_serializers.UserSerializer
    owner_field_reference = 'id'
    http_method_names = ['get', 'update', 'patch']


class UserProfileViewSet(UserSpecificFilteringMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows user ptofiles to be viewed or edited.
    """
    filterset_fields = '__all__'
    queryset = UserProfile.objects.all().order_by('user_id')
    serializer_class = blapi_serializers.UserProfileSerializer
    owner_field_reference = 'user_id'
    http_method_names = ['get', 'update', 'patch']


class LoyaltyCodeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows loyalty codes to be viewed or edited.
    """
    filterset_fields = '__all__'
    queryset = LoyaltyCode.objects.all()
    serializer_class = blapi_serializers.LoyaltyCodeSerializer

class IntegrationViewSet(UserSpecificFilteringMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows integrations to be viewed or edited.
    """
    filterset_fields = '__all__'
    queryset = Integration.objects.all()
    serializer_class = blapi_serializers.IntegrationSerializer
    owner_field_reference = 'user'


class ChartsViewSet(UserSpecificFilteringMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows charts to be viewed or edited.
    """
    filterset_fields = '__all__'
    queryset = Chart.objects.all()
    serializer_class = blapi_serializers.ChartSerializer
    owner_field_reference = 'dashboard__user'

    @action(detail=False, methods=['POST'])
    def add_chart(self, request):

        # TODO: Implement backwards removing of objects when some object
        #       doesn't pass

        # Save TimeRange
        if request.data['metric']['time_range']:
            tr_s = blapi_serializers.TimeRangeSerializer(
                data=request.data['metric']['time_range']
            )
            if tr_s.is_valid():
                time_range = tr_s.save()
            else:
                # print(tr_s.errors)
                return Response('TimeRange not valid.', status=400)
        else:
            time_range = None

        # Save ChartType
        try:
            chart_type = ChartType.objects.get(
                name=request.data['metric']['chart_type']
            )
        except ChartType.DoesNotExist:
            return Response('ChartType does not exists.', status=400)

        # Save Metric
        metric_data = {
            **request.data['metric'],
            'datasource_id': request.data['metric']['datasource'],
            'chart_type_id': chart_type.id,
            'time_range_id': time_range.id if time_range else None,
        }

        metric_s = blapi_serializers.MetricSerializer(data=metric_data)
        if metric_s.is_valid():
            metric = metric_s.save()
        else:
            # print(metric_s.errors)
            return Response('Metric not valid.', status=400)

        chart_data = {
            'dashboard_id': request.data['dashboard'],
            'metric_id': metric.id,
            'predefined_metric_id': request.data['predefined_metric'],
        }

        chart_s = blapi_serializers.ChartSerializer(data=chart_data)
        if chart_s.is_valid():
            chart = chart_s.save()
        else:
            # print(chart_s.errors)
            return Response('Chart not valid.', status=400)

        dashboard_layout_s = blapi_serializers.DashboardLayoutSerializer(
            data={
                **request.data['dashboard_layout'],
                'dashboard_id': request.data['dashboard'],
                'chart_id': chart.id
            }
        )

        if dashboard_layout_s.is_valid():
            dashboard_layout = dashboard_layout_s.save()
        else:
            return Response('DashboardLayout not valid.', status=400)

        return Response({'id': chart.id})


class PredefinedIntegrationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows predefined integrations to be viewed or edited.
    """
    filterset_fields = '__all__'
    queryset = PredefinedIntegration.objects.all()
    serializer_class = blapi_serializers.PredefinedIntegrationSerializer


class PredefinedChartTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows predefined chart types to be viewed or edited.
    """
    filterset_fields = '__all__'
    queryset = PredefinedChartType.objects.all()
    serializer_class = blapi_serializers.PredefinedIntegrationSerializer


class PredefinedMetricViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows predefined metrics to be viewed or edited.
    """
    filter_backends = api_settings.DEFAULT_FILTER_BACKENDS \
        + [InAllFilterBackend]
    filterset_class = PredefinedMetricFilterSet
    filterset_fields = '__all__'
    queryset = PredefinedMetric.objects.all()
    serializer_class = blapi_serializers.PredefinedMetricSerializer


class PredefinedMetricTypesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows predefined metric types to be viewed or edited.
    """
    filterset_fields = '__all__'
    queryset = PredefinedMetricType.objects.all()
    serializer_class = blapi_serializers.PredefinedMetricTypeSerializer


class PredefinedChartTypesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows predefined chart types to be viewed or edited.
    """
    filterset_fields = '__all__'
    queryset = PredefinedChartType.objects.all()
    serializer_class = blapi_serializers.PredefinedChartTypeSerializer


class PredefinedTimeRangeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows predefined time ranges to be viewed or edited.
    """
    filterset_fields = '__all__'
    queryset = PredefinedTimeRange.objects.all()
    serializer_class = blapi_serializers.PredefinedTimeRangeSerializer


class ChartTypeViewSet(viewsets.ModelViewSet):
    filterset_fields = '__all__'
    queryset = ChartType.objects.all()
    serializer_class = blapi_serializers.ChartTypeSerializer


class TimeRangeViewSet(UserSpecificFilteringMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows time ranges to be viewed or edited.
    """
    filterset_fields = '__all__'
    queryset = TimeRange.objects.all()
    serializer_class = blapi_serializers.TimeRangeSerializer
    owner_field_reference = 'metric__chart__dashboard__user'


class MetricViewSet(UserSpecificFilteringMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows metrics to be viewed or edited.
    """
    filter_backends = api_settings.DEFAULT_FILTER_BACKENDS \
        + UserSpecificFilteringMixin.filter_backends \
        + [InAllFilterBackend]
    filterset_fields = '__all__'
    queryset = Metric.objects.all()
    serializer_class = blapi_serializers.MetricSerializer
    owner_field_reference = 'chart__dashboard__user'


class DashboardsViewSet(UserSpecificFilteringMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows dashboards to be viewed or edited.
    """
    filterset_fields = '__all__'
    queryset = BLDashboard.objects.all()
    serializer_class = blapi_serializers.DashboardSerializer
    owner_field_reference = 'user'


class DashboardsLayoutsViewSet(UserSpecificFilteringMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows dashboard layouts to be viewed or edited.
    """
    filterset_fields = '__all__'
    queryset = DashboardLayout.objects.all().order_by('dashboard', 'chart')
    serializer_class = blapi_serializers.DashboardLayoutSerializer
    owner_field_reference = 'dashboard__user'


class DataSourcesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows data sources to be viewed or edited.
    """
    filterset_fields = '__all__'
    queryset = DataSource.objects.all()
    serializer_class = blapi_serializers.DataSourceSerializer


class SummaryIntegrationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows summary metric integrations to be viewed or edited.
    """
    filterset_fields = '__all__'
    queryset = SummaryIntegration.objects.all()
    serializer_class = blapi_serializers.SummaryIntegrationSerializer


class SummaryMetricViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows summary metrics to be viewed or edited.
    """
    filterset_fields = '__all__'
    queryset = SummaryMetric.objects.all()
    serializer_class = blapi_serializers.SummaryMetricSerializer


class SummaryTimeRangeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows summary metric time ranges to be viewed or edited.
    """
    filterset_fields = '__all__'
    queryset = SummaryTimeRange.objects.all()
    serializer_class = blapi_serializers.SummaryTimeRangeSerializer


class SocialAccountViewSet(UserSpecificFilteringMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows social accounts to be viewed or edited.
    """
    filterset_fields = '__all__'
    queryset = SocialAccount.objects.all()
    serializer_class = blapi_serializers.SocialAccountSerializer
    owner_field_reference = 'user'


# Top Posts & Stories views
class TopSocialMetricViewSet(viewsets.ModelViewSet):
    filterset_fields = '__all__'
    queryset = TopSocialMetric.objects.all()
    serializer_class = blapi_serializers.TopSocialMetricSerializer

class TopSocialIntegrationViewSet(viewsets.ModelViewSet):
    filterset_fields = '__all__'
    queryset = TopSocialIntegration.objects.all()
    serializer_class = blapi_serializers.TopSocialIntegrationSerializer

class TopSocialTimeRangeViewSet(viewsets.ModelViewSet):
    filterset_fields = '__all__'
    queryset = TopSocialTimeRange.objects.all()
    serializer_class = blapi_serializers.TopSocialTimeRangeSerializer

class ActiveSubViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    basename = "active_subscription"
    route_name = "data"
    queryset = []

    @classmethod
    def get_extra_actions(cls):
        return []
    
    def list(self, request, *args, **kwargs):
        #tier_list = Tier.objects.all()
        current_tier_list = UserTier.objects.filter(user_id=request.user.id)

        for user in current_tier_list:
            '''
            if user.tier == 'free':
                data={"active_sub": False}
            else:
                if user.valid_until > date.today():
                    data={"active_sub": False}
                else:
                    data={"active_sub": True}
            '''
            data={"active_sub": True}

        
        serializer = blapi_serializers.ActiveSubscription(data=data)
        if serializer.is_valid():
            return Response(serializer.data)
        
