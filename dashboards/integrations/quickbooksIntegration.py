from __future__ import print_function

from ..integrations.integration import Integration
from allauth.socialaccount.models import SocialAccount
from celery import shared_task
import logging


logger = logging.getLogger(__name__)


class QuickbooksIntegration(Integration):

    def get_task(self, user):
        task = initialize_quickbooks_syncworker_task
        tcount = SocialAccount.objects.filter(provider='quickbooks', user_id=user.id).count()
        return task, tcount

    def get_params(self):
        pass

    def set_sync_state(self, user_id, integration_name, celery_id):
        return super().set_sync_state(user_id, integration_name, celery_id)

    def build_auth_params(self, integration_name, user):
        return super().build_auth_params(integration_name, user)


@shared_task(time_limit=36000, name="initialize_quickbooks_syncworker_task")
def initialize_quickbooks_syncworker_task(integration, user):
    try:
        print("SYNC - QUICKBOOKS - {}".format(user))
        """placeholder"""
        task_id = initialize_quickbooks_syncworker_task.request.id
        user_iden = user.id
        integration.set_sync_state(user_iden, 'quickbooks', task_id)
    except Exception as e:
        logger.warn("Following exception occurred for QuickBooks integration of user " + str(user) + ": " + str(e))
        return 'failed'

    return 'done'
