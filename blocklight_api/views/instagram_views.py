from .base_views import BaseDatasourceViewSet
from blocklight_api.serializers import instagram_serializers
from blocklight_api.serializers.core_serializers import ChartDataSerializer

from dashboards.models import (
    Integrations_InstagramInsights_Reach,
    Integrations_InstagramInsights_Followers,
    Integrations_InstagramInsights_Impressions,
    Integrations_Instagram_Media_Objects,
    Integrations_Instagram_Media_Insights_Engagements,
    Integrations_Instagram_Media_Insights_Impressions,
    Integrations_Instagram_Media_Insights_Reach,
    Integrations_Instagram_Media_Insights_Saved,
    Integrations_Instagram_Media_Insights_Video_Views,
    Integrations_Instagram_Media_Insights_Story_Exits,
    Integrations_Instagram_Media_Insights_Story_Replies,
    Integrations_Instagram_Media_Insights_Story_Taps_Fwd,
    Integrations_Instagram_Media_Insights_Story_Taps_Back
)


class InstagramFollowersViewSet(BaseDatasourceViewSet):
    queryset = Integrations_InstagramInsights_Followers.objects.all()
    serializer_class = instagram_serializers.InstagramFollowersSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'end_time'


class InstagramImpressionsViewSet(BaseDatasourceViewSet):
    queryset = Integrations_InstagramInsights_Impressions.objects.all()
    serializer_class = instagram_serializers.InstagramImpressionsSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'end_time'


class InstagramReachesViewSet(BaseDatasourceViewSet):
    queryset = Integrations_InstagramInsights_Reach.objects.all()
    serializer_class = instagram_serializers.InstagramReachesSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'end_time'


class InstagramMediaObjectsViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Instagram_Media_Objects.objects.all()
    serializer_class = instagram_serializers.InstagramMediaObjectsSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'timestamp'


class InstagramMediaInsightsEngagementsViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Instagram_Media_Insights_Engagements.objects.all()
    serializer_class = instagram_serializers.InstagramMediaInsightsEngagementsSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'end_time'


class InstagramMediaInsightsImpressionsViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Instagram_Media_Insights_Impressions.objects.all()
    serializer_class = instagram_serializers.InstagramMediaInsightsImpressionsSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'end_time'


class InstagramMediaInsightsReachViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Instagram_Media_Insights_Reach.objects.all()
    serializer_class = instagram_serializers.InstagramMediaInsightsReachSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'end_time'


class InstagramMediaInsightsSavedViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Instagram_Media_Insights_Saved.objects.all()
    serializer_class = instagram_serializers.InstagramMediaInsightsSavedSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'end_time'


class InstagramMediaInsightsVideoViewsViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Instagram_Media_Insights_Video_Views.objects.all()
    serializer_class = instagram_serializers.InstagramMediaInsightsVideoViewsSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'end_time'


class InstagramMediaInsightsStoryExitsViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Instagram_Media_Insights_Story_Exits.objects.all()
    serializer_class = instagram_serializers.InstagramMediaInsightsStoryExitsSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'end_time'


class InstagramMediaInsightsStoryRepliesViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Instagram_Media_Insights_Story_Replies.objects.all()
    serializer_class = instagram_serializers.InstagramMediaInsightsStoryRepliesSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'end_time'


class InstagramMediaInsightsStoryTapsFwdViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Instagram_Media_Insights_Story_Taps_Fwd.objects.all()
    serializer_class = instagram_serializers.InstagramMediaInsightsStoryTapsFwdSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'end_time'


class InstagramMediaInsightsStoryTapsBackViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Instagram_Media_Insights_Story_Taps_Back.objects.all()
    serializer_class = instagram_serializers.InstagramMediaInsightsStoryTapsBackSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'end_time'
