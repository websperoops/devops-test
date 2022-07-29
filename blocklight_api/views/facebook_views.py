from .base_views import BaseDatasourceViewSet
from blocklight_api.serializers import facebook_serializers
from blocklight_api.serializers.core_serializers import ChartDataSerializer

from dashboards.models import(
    Integrations_FacebookInsights_Impressions,
    Integrations_FacebookInsights_Posts, Integrations_FacebookInsights_Views,
    Integrations_FacebookInsights_Reactions,
    Integrations_FacebookInsights_Demographics,
    Integrations_FacebookInsights_Engagements,
    Integrations_Facebook_Page_Posts,
    Integrations_Facebook_Page_Post_Impressions,
)


class FacebookDemographicsViewSet(BaseDatasourceViewSet):
    queryset = Integrations_FacebookInsights_Demographics.objects.all()
    serializer_class = facebook_serializers.FacebookDemographicsSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'end_time'


class FacebookEngagementsViewSet(BaseDatasourceViewSet):
    queryset = Integrations_FacebookInsights_Engagements.objects.all()
    serializer_class = facebook_serializers.FacebookEngagementsSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'end_time'


class FacebookImpressionsViewSet(BaseDatasourceViewSet):
    queryset = Integrations_FacebookInsights_Impressions.objects.all()
    serializer_class = facebook_serializers.FacebookImpressionsSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'end_time'


class FacebookPostsViewSet(BaseDatasourceViewSet):
    queryset = Integrations_FacebookInsights_Posts.objects.all()
    serializer_class = facebook_serializers.FacebookPostsSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'end_time'


class FacebookReactionsViewSet(BaseDatasourceViewSet):
    queryset = Integrations_FacebookInsights_Reactions.objects.all()
    serializer_class = facebook_serializers.FacebookReactionsSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'end_time'


class FacebookViewsViewSet(BaseDatasourceViewSet):
    queryset = Integrations_FacebookInsights_Views.objects.all()
    serializer_class = facebook_serializers.FacebookViewsSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'end_time'


class FacebookPagePostsViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Facebook_Page_Posts.objects.all()
    serializer_class = facebook_serializers.FacebookPagePostsSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'created_time'


class FacebookPagePostImpressionsViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Facebook_Page_Post_Impressions.objects.all()
    serializer_class = facebook_serializers.FacebookPagePostImpressionsSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'end_time'


class FacebookPagePostEngagementsViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Facebook_Page_Post_Impressions.objects.all()
    serializer_class = facebook_serializers.FacebookPagePostImpressionsSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'end_time'


class FacebookPagePostReactionsViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Facebook_Page_Post_Impressions.objects.all()
    serializer_class = facebook_serializers.FacebookPagePostImpressionsSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'end_time'
