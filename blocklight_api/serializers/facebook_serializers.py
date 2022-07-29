from dashboards.models import(
    Integrations_FacebookInsights_Impressions,
    Integrations_FacebookInsights_Posts, Integrations_FacebookInsights_Views,
    Integrations_FacebookInsights_Reactions,
    Integrations_FacebookInsights_Demographics,
    Integrations_FacebookInsights_Engagements,
    Integrations_Facebook_Page_Posts,
    Integrations_Facebook_Page_Post_Impressions,
    Integrations_Facebook_Page_Post_Engagements,
    Integrations_Facebook_Page_Post_Reactions
)

from rest_framework import serializers


class FacebookDemographicsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_FacebookInsights_Demographics
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


class FacebookEngagementsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_FacebookInsights_Engagements
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


class FacebookImpressionsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_FacebookInsights_Impressions
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


class FacebookPostsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_FacebookInsights_Posts
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


class FacebookReactionsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_FacebookInsights_Reactions
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


class FacebookViewsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_FacebookInsights_Views
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


class FacebookPagePostsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Facebook_Page_Posts
        exclude = ['integration',
                   'url']


class FacebookPagePostImpressionsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Facebook_Page_Post_Impressions
        exclude = ['integration',
                   'url']


class FacebookPagePostEngagementsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Facebook_Page_Post_Engagements
        exclude = ['integration',
                   'url']


class FacebookPagePostReactionsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Facebook_Page_Post_Reactions
        exclude = ['integration',
                   'url']
