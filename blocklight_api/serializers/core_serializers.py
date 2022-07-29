from allauth.socialaccount.models import SocialAccount

from blocklight_api.models import (
    Integration, DataSource, ChartType, TimeRange,
    Metric, BLDashboard, Chart, DashboardLayout,
    PredefinedIntegration, PredefinedMetric, PredefinedMetricType,
    PredefinedChartType, PredefinedTimeRange, 
    SummaryIntegration, SummaryMetric, SummaryTimeRange, LoyaltyCode,
    TopSocialMetric, TopSocialIntegration, TopSocialTimeRange
)

from dashboards.models import UserProfile
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'first_name', 'last_name', 'date_joined']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ['forgot_password', 'accept_tos', 'email_verified']


class LoyaltyCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoyaltyCode
        fields = '__all__'


class ChartDataSerializer(serializers.Serializer):

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super(ChartDataSerializer, self).__init__(*args, **kwargs)
        if fields:
            for f in fields:
                self.fields[f] = serializers.CharField(max_length=100)


class DataSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSource
        fields = '__all__'


class ChartTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChartType
        fields = '__all__'


class PredefinedIntegrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = PredefinedIntegration
        fields = '__all__'


class PredefinedMetricSerializer(serializers.ModelSerializer):

    chart_type_icon = ChartTypeSerializer()

    class Meta:
        model = PredefinedMetric
        fields = '__all__'


class PredefinedMetricTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PredefinedMetricType
        fields = '__all__'


class PredefinedChartTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PredefinedChartType
        fields = '__all__'


class PredefinedTimeRangeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PredefinedTimeRange
        fields = '__all__'


class IntegrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Integration
        fields = '__all__'


class TimeRangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeRange
        fields = '__all__'


class MetricSerializer(serializers.ModelSerializer):
    # Note: Combinations of read_only and write_only is tu allow automatic
    #       functionality of Serializer to save ForeignKey instead of creating
    #       new nested object
    datasource = serializers.SlugRelatedField(slug_field='url', read_only=True)
    datasource_id = serializers.IntegerField(write_only=True)
    chart_type = ChartTypeSerializer(read_only=True)
    chart_type_id = serializers.IntegerField(write_only=True)

    time_range = TimeRangeSerializer(read_only=True)
    time_range_id = serializers.IntegerField(write_only=True, allow_null=True)

    class Meta:
        model = Metric
        fields = '__all__'


class DashboardSerializer(serializers.ModelSerializer):
    charts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = BLDashboard
        fields = '__all__'


class ChartSerializer(serializers.ModelSerializer):
    dashboard = DashboardSerializer(read_only=True)
    dashboard_id = serializers.IntegerField(write_only=True)
    metric = MetricSerializer(read_only=True)
    metric_id = serializers.IntegerField(write_only=True)
    predefined_metric = PredefinedMetricSerializer(read_only=True)
    predefined_metric_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Chart
        fields = '__all__'


class DashboardLayoutSerializer(serializers.ModelSerializer):
    chart_id = serializers.IntegerField()
    dashboard_id = serializers.IntegerField()

    class Meta:
        model = DashboardLayout
        exclude = ['chart', 'dashboard']


class SummaryMetricSerializer(serializers.ModelSerializer):

    class Meta:
        model = SummaryMetric
        fields = '__all__'


class SummaryTimeRangeSerializer(serializers.ModelSerializer):

    class Meta:
        model = SummaryTimeRange
        fields = '__all__'


class SummaryIntegrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = SummaryIntegration
        fields = '__all__'


class SummaryIntegrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = SummaryIntegration
        fields = '__all__'


class SocialAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = SocialAccount
        fields = '__all__'


class TopSocialMetricSerializer(serializers.ModelSerializer):

    class Meta:
        model = TopSocialMetric
        fields = '__all__'


class TopSocialIntegrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = TopSocialIntegration
        fields = '__all__'


class TopSocialTimeRangeSerializer(serializers.ModelSerializer):

    class Meta:
        model = TopSocialTimeRange
        fields = '__all__'

class ActiveSubscription(serializers.Serializer):
    active_sub = serializers.BooleanField()

