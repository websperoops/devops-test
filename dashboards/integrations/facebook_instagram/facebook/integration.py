from __future__ import print_function

from ....integrations.integration import Integration
from . import facebookInsightHandler, facebookPagePostHandler
from . import sync

from allauth.socialaccount.models import SocialAccount, SocialToken
from celery import shared_task

from dashboards.integrations.facebook_instagram.facebook import fb_api
from dashboards.integrations.utils.dashboard_sync_complete import dashboard_sync_complete
from dashboards.models import Integrations_FacebookInsights_Views, \
    Integrations_FacebookInsights_Impressions, Integrations_FacebookInsights_Engagements, \
    Integrations_FacebookInsights_Reactions, Integrations_FacebookInsights_Demographics, \
    Integrations_FacebookInsights_Posts, \
    Integrations_Facebook_Page_Posts

from django.contrib.auth.models import User as DjangoUser
import logging
import requests

from ....enums.CoreEnums import Master_Blocklight_User



logger = logging.getLogger(__name__)


class FacebookIntegration(Integration):

    def get_task(self, user):
        task = initialize_facebook_syncworker_task
        tcount = SocialAccount.objects.filter(
            provider='facebook', user_id=user.id).count()
        return task, tcount

    def get_params(self, auth_params):
        user_iden = auth_params['user_iden']
        url = "https://graph.facebook.com/v7.0/" + str(SocialAccount.objects.get(user_id=int(user_iden),
                                                                                 provider='facebook').uid) + "/accounts?fields=id,name&access_token="
        access_token = SocialToken.objects.get(
            account__user=auth_params['user'], account__provider='facebook')
        url = url + str(access_token)
        response_body = requests.get(url).json()

        page_posts = {
            'model': Integrations_Facebook_Page_Posts,
            'handler': facebookPagePostHandler.FacebookPagePostHandler,
            'API': fb_api.FB_API.get_fb_page_published_posts,
            'integration_name': 'facebook',
            'key': 'facebook_page_views',
            'api-type': 'post',
            'page-key': 'manual',
            'timestamp_field': 'created_time'
        }

        # FACEBOOK PAGE VIEWS | api endpoint params
        views = {'model': Integrations_FacebookInsights_Views,
                 'handler': facebookInsightHandler.FacebookInsightHandler,
                 'API': fb_api.FB_API.get_fb_page_views,
                 'integration_name': 'facebook',
                 'key': 'facebook_page_views',
                 'api-type': 'insight',
                 'page-key': 'previous',
                 'timestamp_field': 'end_time'}

        # FACEBOOK PAGE IMPRESSIONS | api endpoint params
        impressions = {'model': Integrations_FacebookInsights_Impressions,
                       'handler': facebookInsightHandler.FacebookInsightHandler,
                       'API': fb_api.FB_API.get_fb_page_impressions,
                       'integration_name': 'facebook',
                       'key': 'facebook_page_impressions',
                       'api-type': 'insight',
                       'page-key': 'previous',
                       'timestamp_field': 'end_time'}

        # FACEBOOK PAGE ENGAGEMENTS | api endpoint params
        engagements = {'model': Integrations_FacebookInsights_Engagements,
                       'handler': facebookInsightHandler.FacebookInsightHandler,
                       'API': fb_api.FB_API.get_fb_page_engagements,
                       'integration_name': 'facebook',
                       'key': 'facebook_page_engagements',
                       'api-type': 'insight',
                       'page-key': 'previous',
                       'timestamp_field': 'end_time'}

        # FACEBOOK PAGE REACTIONS | api endpoint params
        reactions = {'model': Integrations_FacebookInsights_Reactions,
                     'handler': facebookInsightHandler.FacebookInsightHandler,
                     'API': fb_api.FB_API.get_fb_page_reactions,
                     'integration_name': 'facebook',
                     'key': 'facebook_page_reactions',
                     'api-type': 'insight',
                     'page-key': 'previous',
                     'timestamp_field': 'end_time'}

        # FACEBOOK PAGE FANS / DEMOGRAPHICS | api endpoint params
        demographics = {'model': Integrations_FacebookInsights_Demographics,
                        'handler': facebookInsightHandler.FacebookInsightHandler,
                        'API': fb_api.FB_API.get_fb_page_demographics,
                        'integration_name': 'facebook',
                        'key': 'facebook_page_demographics',
                        'api-type': 'insight',
                        'page-key': 'previous',
                        'timestamp_field': 'end_time'}

        # FACEBOOK PAGE POSTS | api endpoint params
        posts = {'model': Integrations_FacebookInsights_Posts,
                 'handler': facebookInsightHandler.FacebookInsightHandler,
                 'API': fb_api.FB_API.get_fb_page_posts,
                 'integration_name': 'facebook',
                 'key': 'facebook_post_impressions',
                 'api-type': 'insight',
                 'page-key': 'previous',
                 'timestamp_field': 'end_time'}

        apis = [
            {'name': 'page_posts', 'data': page_posts},
            {'name': 'views', 'data': views},
            {'name': 'impressions', 'data': impressions},
            {'name': 'engagements', 'data': engagements},
            {'name': 'reactions', 'data': reactions},
            {'name': 'demographics', 'data': demographics},
            {'name': 'posts', 'data': posts}
        ]
        return {'apis': apis, 'response_body': response_body, 'access_token': access_token}

    def set_sync_state(self, user_id, integration_name, celery_id):
        return super().set_sync_state(user_id, integration_name, celery_id)

    def build_auth_params(self, integration_name, user):
        return super().build_auth_params(integration_name, user)


@shared_task(time_limit=36000, name="initialize_facebook_syncworker_task")
def initialize_facebook_syncworker_task(integration=None, user=None):

    if not integration or not user:
        user, integration = DjangoUser.objects.get(
            id=Master_Blocklight_User.User_Id), FacebookIntegration()
    result = sync.save_facebook(integration, user)
    dashboard_sync_complete('facebook', user.id)

    return result
