from ...integrations.integration import Integration
from . import campaignHandler, listHandler
from . import sync

from allauth.socialaccount.models import SocialAccount
from celery import shared_task

from dashboards.integrations.utils.dashboard_sync_complete import dashboard_sync_complete, token_failure
from dashboards.models import Integrations_MailChimp_Campaigns, Integrations_MailChimp_Lists, \
    Integrations_MailChimp_ListMembers, Integrations_MailChimp_CampaignReports, Integrations_MailChimp_ListStats, \
    Integrations_MailChimp_Campaigns_Bl_Insights

from django.contrib.auth.models import User as DjangoUser
from django.db import transaction

import logging
from mailchimp3 import MailChimp
from ...enums.CoreEnums import Master_Blocklight_User



logger = logging.getLogger(__name__)


class MailchimpIntegration(Integration):
    def get_task(self, user):
        logger.debug('INTEGRATION -----------------------------')
        logger.debug(user)
        task = initialize_mailchimp_syncworker_task
        logger.debug(SocialAccount.objects.filter(
            provider='mailchimp', user_id=user.id))
        tcount = SocialAccount.objects.filter(
            provider='mailchimp', user_id=user.id).count()
        return task, tcount

    def get_params(self, auth_params):

        access_token = auth_params['access_token']
        client = MailChimp(access_token=access_token)

        campaigns = {
            'model': Integrations_MailChimp_Campaigns,
            'API': client.campaigns,
            'handler': campaignHandler.CampaignHandler,
            'key': 'campaigns'
        }

        lists = {
            'model': Integrations_MailChimp_Lists,
            'API': client.lists,
            'handler': listHandler.ListHandler,
            'key': 'lists'
        }

        apis = [
            {'name': 'campaigns', 'data': campaigns},
            {'name': 'lists', 'data': lists},
        ]
        return apis

    def set_sync_state(self, user_id, integration_name, celery_id):
        return super().set_sync_state(user_id, integration_name, celery_id)

    def build_auth_params(self, integration_name, user):
        logger.debug('AUTH PARAMS ------------------------------------------')
        logger.debug(user)

        return super().build_auth_params(integration_name, user)


@shared_task(time_limit=36000, name="initialize_mailchimp_syncworker_task")
def initialize_mailchimp_syncworker_task(integration=None, user=None):
    logger.debug('MAILCHIMP USER ID -------------------------------------------')
    logger.debug(user)
    if not integration or not user:
        integration, user = MailchimpIntegration(), DjangoUser.objects.get(id=Master_Blocklight_User.User_Id)
    logger.debug('MAILCHIMP USER ID -------------------------------------------')
    logger.debug(user)
    task_id = initialize_mailchimp_syncworker_task.request.id

    try:
        result = sync.save_mailchimp(
            integration=integration,
            user=user,
            task_id=task_id
        )
        dashboard_sync_complete('mailchimp', user.id)
        return result
    except Exception as e:
        logger.debug("Sync Failed - MailChimp")
        token_failure('mailchimp', user.id)
        dashboard_sync_complete('mailchimp', user.id)
        raise e


@shared_task(time_limit=36000, name='delete_mailchimp_user_data_task')
def delete_mailchimp_user_data_task(integration=None, user=None):
    with transaction.atomic():
        if not integration or not user:
            integration, user = MailchimpIntegration(), DjangoUser.objects.get(id=Master_Blocklight_User.User_Id)

        models = [
            Integrations_MailChimp_CampaignReports,
            Integrations_MailChimp_ListMembers,
            Integrations_MailChimp_ListStats,
            Integrations_MailChimp_Campaigns,
            Integrations_MailChimp_Lists,
            Integrations_MailChimp_Campaigns_Bl_Insights
        ]

        try:
            for model in models:
                model.objects.filter(user_iden=user.id).delete()
        except Exception as e:
            logger.warn(e)
            raise e
        return 'success'
