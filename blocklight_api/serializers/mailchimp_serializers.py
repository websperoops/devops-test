from dashboards.models import(
    Integrations_MailChimp_CampaignReports,Integrations_MailChimp_Campaigns,
    Integrations_MailChimp_ListMembers, Integrations_MailChimp_Lists,
    Integrations_MailChimp_ListStats, Integrations_MailChimp_Campaigns_Bl_Insights
)

from rest_framework import serializers


class MailChimpCampaignReportsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_MailChimp_CampaignReports
        fields = [
            'user_iden',
            'create_time',
            'open_rate',
            'click_rate',
            'subscriber_clicks',
            'total_spent',
            'total_revenue',
            'total_orders',
            'clicks',
            'opens',
            'unique_opens',
        ]


class MailChimpCampaignsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_MailChimp_Campaigns
        fields = [
            'user_iden',
            'from_name',
            'subject_line',
            'campaign_id',
            'type',
            'date_created',
            'archive_url',
            'long_archive_url',
            'status',
            'emails_sent',
            'send_time',
            'content_type',
            'recipients',
            'settings',
            'tracking',
            'report_summary',
            'delivery_status'
        ]


class MailChimpListMemebersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_MailChimp_ListMembers
        fields = [
            'user_iden',
            'member_id',
            'email_address',
            'unique_email_id',
            'email_type',
            'status',
            'stats',
            'ip_signup',
            'timestamp_signup',
            'member_rating',
            'vip',
            'email_client',
            'location',
            'list_id'
        ]


class MailChimpListsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_MailChimp_Lists
        fields = [
            'user_iden',
            'list_id',
            'web_id',
            'name',
            'contact',
            'date_created',
            'list_rating',
            'stats'
        ]


class MailChimpListStatsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_MailChimp_ListStats
        fields = [
            'user_iden',
            'list_name',
            'date_created',
            'stats_id',
            'avg_sub_rate',
            'open_rate',
            'member_count',
            'click_rate',
            'cleaned_count_since_send',
            'member_count_since_send',
            'target_sub_rate',
            'last_sub_date',
            'merge_field_count',
            'avg_unsub_rate',
            'unsubscribe_count',
            'campaign_count',
            'campaign_last_sent',
            'unsubscribe_count_since_send',
            'campaign_count',
            'last_unsub_date'
        ]


class MailChimpBlInsightsCampaignsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_MailChimp_Campaigns_Bl_Insights
        fields = [
            'campaign_id',
            'date_created',
            'type',
            'status',
            'archive_url',
            'long_archive_url',
            'campaign_creation_time',
            'send_time',
            'from_name',
            'title',
            'subject_line',
            'preview_text',
            'emails_sent',
            'opens',
            'unique_opens',
            'open_rate',
            'clicks',
            'subscriber_clicks',
            'click_rate',
            'total_orders',
            'total_revenue',
            'total_spent',
            'campaign_aov'
        ]