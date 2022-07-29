from . import quickbooksHandler
from dashboards.models import Integrations_Quickbooks_Account_Info
from django.db import transaction
import logging


class AccountHandler(quickbooksHandler.QuickbooksHandler):

    logger = logging.getLogger(__name__)

    def __init__(self, data, integration_id, user_iden, integration_name, name):
        self.accounts = []

        super(AccountHandler, self).__init__(data, integration_id, user_iden, "quickbooks", name)

    def _Handler__save_independent_objects(self):
        with transaction.atomic():
            self.save_accounts()
            
    def _Handler__save_dependent_objects(self):
        with transaction.atomic():
            pass

    def _Handler__parse_data(self):
        
        self.data = self.data.get('QueryResponse', {}).get('Account', [])
        for obj in self.data:
            meta_data = obj.get('MetaData')
            account = Integrations_Quickbooks_Account_Info(
                integration_name = self.name,
                integration_id = self.integration_id,
                user_iden = self.user_iden,
                account_id = obj.get('Id', None),
                name = obj.get('Name', None),
                current_balance = obj.get('CurrentBalance', None),
                active = obj.get('Active', None),
                create_time = meta_data.get('CreateTime', None),
                last_update_time = meta_data.get('LastUpdatedTime', None)
            )
            self.accounts.append(account)

    def save_accounts(self):
        for account in self.accounts:
            self.update_or_save_instance(Integrations_Quickbooks_Account_Info, account, "account_id")