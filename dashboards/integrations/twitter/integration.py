from __future__ import print_function

from ...integrations.integration import Integration
from . import mentionsHandler, sync

from allauth.socialaccount.models import SocialAccount
from celery import shared_task
from dashboards.integrations.utils.dashboard_sync_complete import dashboard_sync_complete
from dashboards.models import Integrations_Twitter_Mentions
from django.contrib.auth.models import User as DjangoUser
import logging
from ...enums.CoreEnums import Master_Blocklight_User



logger = logging.getLogger(__name__)


class TwitterIntegration(Integration):

    def get_task(self, user):
        task = initialize_twitter_syncworker_task
        tcount = SocialAccount.objects.filter(provider='twitter', user_id=user.id).count()
        return task, tcount

    def get_params(self, auth_params):

        mentions = {
            'model': Integrations_Twitter_Mentions,
            'handler': mentionsHandler.MentionsHandler
        }

        apis = [
            {'name': 'mentions', 'data': mentions}
        ]

        return apis

    def set_sync_state(self, user_id, integration_name, celery_id):
        return super().set_sync_state(user_id, integration_name, celery_id)

    def build_auth_params(self, integration_name, user):
        return super().build_auth_params(integration_name, user)


@shared_task(time_limit=36000, name="initialize_twitter_syncworker_task")
def initialize_twitter_syncworker_task(integration=None, user=None):

    if not integration or not user:
        user, integration = DjangoUser.objects.get(id=Master_Blocklight_User.USER_ID), TwitterIntegration()

    task_id = initialize_twitter_syncworker_task.request.id
    result = sync.save_twitter(integration=integration, user=user, task_id=task_id)
    dashboard_sync_complete('twitter', user.id)
    
    return result

