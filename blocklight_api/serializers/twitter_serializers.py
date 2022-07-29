from dashboards.models import(
    Integrations_Twitter_Mentions
)

from rest_framework import serializers


class TwitterMentionsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Twitter_Mentions
        fields = [
            'user_iden',
            'mention_id',
            'text',
            'other_user_id',
            'other_user_name',
            'other_user_screen_name',
            'timestamp'
        ]
