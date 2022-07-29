from __future__ import print_function

from . import instagramInsightHandler, instagramMediaObjectHandler
from . import sync

from ....enums.CoreEnums import Master_Blocklight_User

from allauth.socialaccount.models import SocialAccount, SocialToken
from celery import shared_task

from dashboards.integrations.facebook_instagram.instagram import ig_api
from dashboards.integrations.integration import Integration
from dashboards.models import Integrations_InstagramInsights_Impressions, \
    Integrations_InstagramInsights_Reach, Integrations_InstagramInsights_Followers, Integrations_Instagram_Media_Objects

from django.contrib.auth.models import User as DjangoUser
import logging
import requests


logger = logging.getLogger(__name__)


class InstagramIntegration(Integration):

    def get_task(self, user):
        task = initialize_instagram_syncworker_task
        tcount = SocialAccount.objects.filter(
            provider='instagram', user_id=user.id).count()
        return task, tcount

    def get_params(self, auth_params):
        user_iden = auth_params['user_iden']
        url = "https://graph.facebook.com/v8.0/" + str(SocialAccount.objects.get(user_id=int(user_iden),
                                                                                 provider='instagram').uid) + "/accounts?fields=id,name&access_token="
        access_token = SocialToken.objects.get(
            account__user=auth_params['user'], account__provider='instagram')
        url = url + str(access_token)
        response_body = requests.get(url).json()

        ####################################################
        # INSTAGRAM BUSINESS ACCOUNT | api endpoint params
        #####################################################
        ig_media = {'model': Integrations_Instagram_Media_Objects,
                    'handler': instagramMediaObjectHandler.InstagramMediaObjectHandler,
                    'API': ig_api.IG_API.get_ig_account_media_ids,
                    'integration_name': 'instagram',
                    'key': 'instagram_media',
                    'timestamp_field': 'timestamp',
                    'api-type': 'media',
                    'page-key': 'next'}

        ig_stories = {'model': Integrations_Instagram_Media_Objects,
                      'handler': instagramMediaObjectHandler.InstagramMediaObjectHandler,
                      'API': ig_api.IG_API.get_ig_account_story_ids,
                      'integration_name': 'instagram',
                      'key': 'instagram_story',
                      'timestamp_field': 'timestamp',
                      'api-type': 'story',
                      'page-key': 'next'}

        ig_impressions = {'model': Integrations_InstagramInsights_Impressions,
                          'handler': instagramInsightHandler.InstagramInsightHandler,
                          'API': ig_api.IG_API.get_ig_account_impressions,
                          'integration_name': 'instagram',
                          'key': 'instagram_impressions',
                          'timestamp_field': 'end_time',
                          'api-type': 'insight',
                          'page-key': 'previous'}

        ig_reach = {'model': Integrations_InstagramInsights_Reach,
                    'handler': instagramInsightHandler.InstagramInsightHandler,
                    'API': ig_api.IG_API.get_ig_account_reach,
                    'integration_name': 'instagram',
                    'key': 'instagram_reach',
                    'timestamp_field': 'end_time',
                    'api-type': 'insight',
                    'page-key': 'previous'}

        ig_followers = {'model': Integrations_InstagramInsights_Followers,
                        'handler': instagramInsightHandler.InstagramInsightHandler,
                        'API': ig_api.IG_API.get_ig_account_followers,
                        'integration_name': 'instagram',
                        'key': 'instagram_followers',
                        'timestamp_field': 'end_time',
                        'api-type': 'insight',
                        'page-key': 'previous'}
                        
        ig_follower_count = {
            'model': Integrations_InstagramInsights_Followers,
            'handler': instagramInsightHandler.InstagramInsightHandler,
            'API': ig_api.IG_API.get_ig_account_follower_count,
            'integration_name': 'instagram',
            'key': 'instagram_followers',
            'timestamp_field': 'end_time',
            'api-type': 'insight',
            'page-key': 'previous'
        }

        apis = [
            {'name': 'ig_media', 'data': ig_media},
            {'name': 'ig_stories', 'data': ig_stories},
            {'name': 'ig_impressions', 'data': ig_impressions},
            {'name': 'ig_reach', 'data': ig_reach},
            {'name': 'ig_followers', 'data': ig_followers},
            {'name': 'ig_follower_count', 'data': ig_follower_count}
        ]

        return {'apis': apis, 'response_body': response_body, 'access_token': access_token}

    def set_sync_state(self, user_id, integration_name, celery_id):
        return super().set_sync_state(user_id, integration_name, celery_id)

    def build_auth_params(self, integration_name, user):
        return super().build_auth_params(integration_name, user)


@shared_task(time_limit=36000, name="initialize_instagram_syncworker_task")
def initialize_instagram_syncworker_task(integration=None, user=None):

    if not integration or not user:
        user, integration = DjangoUser.objects.get(Master_Blocklight_User.User_Id), InstagramIntegration()
    result = sync.save_instagram(integration, user)
    return result
