from .base_views import BaseDatasourceViewSet
from blocklight_api.serializers import twitter_serializers
from blocklight_api.serializers.core_serializers import ChartDataSerializer

from dashboards.models import(
    Integrations_Twitter_Mentions
)


class TwitterMentionsViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Twitter_Mentions.objects.all()
    serializer_class = twitter_serializers.TwitterMentionsSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'timestamp'
