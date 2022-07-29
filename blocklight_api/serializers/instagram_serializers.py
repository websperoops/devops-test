from dashboards.models import(
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

from rest_framework import serializers


class InstagramFollowersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_InstagramInsights_Followers
        fields = [
            'user_iden',
            'record_id',
            'period',
            'description',
            'title',
            'name',
            'end_time',
            'value',
            'lookup',
            'all_data',
            'account_name'
        ]


class InstagramImpressionsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_InstagramInsights_Impressions
        fields = [
            'user_iden',
            'record_id',
            'period',
            'description',
            'title',
            'name',
            'end_time',
            'value',
            'lookup',
            'all_data',
            'account_name'
        ]


class InstagramReachesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_InstagramInsights_Reach
        fields = [
            'user_iden',
            'record_id',
            'period',
            'description',
            'title',
            'name',
            'end_time',
            'value',
            'lookup',
            'all_data',
            'account_name'
        ]


class InstagramMediaObjectsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Instagram_Media_Objects
        exclude = [
            'integration',
            'url']


class InstagramMediaInsightsEngagementsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Instagram_Media_Insights_Engagements
        exclude = [
            'integration',
            'url']


class InstagramMediaInsightsImpressionsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Instagram_Media_Insights_Impressions
        exclude = [
            'integration',
            'url']


class InstagramMediaInsightsReachSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Instagram_Media_Insights_Reach
        exclude = [
            'integration',
            'url']


class InstagramMediaInsightsSavedSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Instagram_Media_Insights_Saved
        exclude = [
            'integration',
            'url']


class InstagramMediaInsightsVideoViewsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Instagram_Media_Insights_Video_Views
        exclude = [
            'integration',
            'url']


class InstagramMediaInsightsStoryExitsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Instagram_Media_Insights_Story_Exits
        exclude = [
            'integration',
            'url']


class InstagramMediaInsightsStoryRepliesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Instagram_Media_Insights_Story_Replies
        exclude = [
            'integration',
            'url']


class InstagramMediaInsightsStoryTapsFwdSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Instagram_Media_Insights_Story_Taps_Fwd
        exclude = [
            'integration',
            'url']


class InstagramMediaInsightsStoryTapsBackSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Instagram_Media_Insights_Story_Taps_Back
        exclude = [
            'integration',
            'url']

