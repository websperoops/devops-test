from .base_views import BaseDatasourceViewSet
from blocklight_api.serializers import mailchimp_serializers
from blocklight_api.serializers.core_serializers import ChartDataSerializer

from dashboards.models import(
    Integrations_MailChimp_CampaignReports,Integrations_MailChimp_Campaigns,
    Integrations_MailChimp_ListMembers, Integrations_MailChimp_Lists,
    Integrations_MailChimp_ListStats, Integrations_MailChimp_Campaigns_Bl_Insights
)


class MailchimpCampaignReportsViewSet(BaseDatasourceViewSet):
    queryset = Integrations_MailChimp_CampaignReports.objects.all()
    serializer_class = mailchimp_serializers.MailChimpCampaignReportsSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'campaign_ref__user_iden'
    since_until_field = 'create_time'


class MailchimpCampaignsViewSet(BaseDatasourceViewSet):
    queryset = Integrations_MailChimp_Campaigns.objects.all()
    serializer_class = mailchimp_serializers.MailChimpCampaignsSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'date_created'


class MailchimpListMembersViewSet(BaseDatasourceViewSet):
    queryset = Integrations_MailChimp_ListMembers.objects.all()
    serializer_class = mailchimp_serializers.MailChimpListMemebersSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'member_ref__user_iden'
    since_until_field = 'member_ref__date_created'


class MailchimpListsViewSet(BaseDatasourceViewSet):
    queryset = Integrations_MailChimp_Lists.objects.all()
    serializer_class = mailchimp_serializers.MailChimpListsSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'date_created'


class MailchimpListStatsViewSet(BaseDatasourceViewSet):
    queryset = Integrations_MailChimp_ListStats.objects.all()
    serializer_class = mailchimp_serializers.MailChimpListStatsSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'stats_ref__user_iden'
    since_until_field = 'date_created'

class MailchimpBlInsightsCampaignsViewSet(BaseDatasourceViewSet):
    queryset = Integrations_MailChimp_Campaigns_Bl_Insights.objects.all()
    serializer_class = mailchimp_serializers.MailChimpBlInsightsCampaignsSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'date_created'