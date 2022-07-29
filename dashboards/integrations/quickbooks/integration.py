from __future__ import print_function

from ...integrations.integration import Integration
from . import sync, companyHandler, billHandler, ledgerHandler, accountHandler

from allauth.socialaccount.models import SocialAccount
from celery import shared_task
from dashboards.integrations.utils.dashboard_sync_complete import dashboard_sync_complete
from dashboards.models import Integrations_Quickbooks_Company_Info, Integrations_Quickbooks_Bills, Integrations_Quickbooks_Ledger_Reports, Integrations_Quickbooks_Account_Info
from django.contrib.auth.models import User as DjangoUser
import logging
from ...enums.CoreEnums import Master_Blocklight_User


logger = logging.getLogger(__name__)


class QuickbooksIntegration(Integration):

    def get_task(self, user):
        task = initialize_quickbooks_syncworker_task
        tcount = SocialAccount.objects.filter(provider='quickbooks', user_id=user.id).count()
        return task, tcount

    def get_params(self, auth_params):
        company = {
            'model': Integrations_Quickbooks_Company_Info,
            'key': 'CompanyInfo',
            'handler': companyHandler.CompanyHandler
        }
        account = {
            'model': Integrations_Quickbooks_Account_Info,
            'key': 'Account',
            'handler': accountHandler.AccountHandler
        }
        bill = {
            'model': Integrations_Quickbooks_Bills,
            'key': 'Bill',
            'handler': billHandler.BillHandler
        }
        ledger = {
            'model': Integrations_Quickbooks_Ledger_Reports,
            'key': 'Ledger',
            'handler': ledgerHandler.LedgerHandler
        }

        apis = [
            {'name': 'companyinfo', 'data': company},
            {'name': 'accountinfo', 'data': account},
            {'name': 'bill', 'data': bill},
            {'name': 'ledger', 'data': ledger}
        ]

        return apis

    def set_sync_state(self, user_id, integration_name, celery_id):
        return super().set_sync_state(user_id, integration_name, celery_id)

    def build_auth_params(self, integration_name, user):
        return super().build_auth_params(integration_name, user)


@shared_task(time_limit=36000, name="initialize_quickbooks_syncworker_task")
def initialize_quickbooks_syncworker_task(integration=None, user=None):

    if not integration or not user:
        user, integration = DjangoUser.objects.get(id=Master_Blocklight_User.User_Id), QuickbooksIntegration()

    task_id = initialize_quickbooks_syncworker_task.request.id
    
    try:
        result = sync.save_quickbooks(integration=integration, user=user, task_id=task_id)
        dashboard_sync_complete('quickbooks', user.id)
        return result    
        
    except Exception as e:
        logger.debug("Sync Failed - Quickbooks")
        dashboard_sync_complete('quickbooks', user.id)
        raise e