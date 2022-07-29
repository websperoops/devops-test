from . import quickbooksHandler
from dashboards.models import Integrations_Quickbooks_Ledger_Reports, Integrations_Quickbooks_Ledger_Expenses, Integrations_Quickbooks_Account_Info
from django.db import transaction
import logging


class LedgerHandler(quickbooksHandler.QuickbooksHandler):

    logger = logging.getLogger(__name__)

    def __init__(self, data, integration_id, user_iden, integration_name, name):
        self.ledgers = []
        self.ledger_lines = {}

        super(LedgerHandler, self).__init__(data, integration_id, user_iden, "quickbooks", name)

    def _Handler__save_independent_objects(self):
        with transaction.atomic():
            self.save_ledgers()
    
    def _Handler__save_dependent_objects(self):
        with transaction.atomic():
            self.save_expenses()

    def _Handler__parse_data(self):
        overall_container = self.data.get('Header', {})
        data_container = self.data.get('Rows', {}).get('Row', [])
        for obj in data_container:
            # empty expenses list to pass to grab_expenses function
            expenses = list()

            # Container creation to simplify indexing
            header_data_container = obj.get('Header', {})
            row_data_container = obj.get('Rows', {}).get('Row', [])
            summary_container = obj.get('Summary', {})

            if summary_container.get('ColData', [])[6].get('value', 0) == '':
                transaction_balance = 0
            else:
                transaction_balance = float(summary_container.get('ColData')[6].get('value', 0))

            try: 
                row_data_container[0].get('ColData', [])[7].get('value', 0)
            except:
                continue

            if row_data_container[0].get('ColData', [])[7].get('value', 0) == '':
                beginning_balance = 0
            else:
                beginning_balance = float(row_data_container[0].get('ColData', [])[7].get('value', 0))
            
            ending_balance = float(beginning_balance + transaction_balance)

            account_id = header_data_container.get('ColData', [])[0].get('id', None)
            ledger = Integrations_Quickbooks_Ledger_Reports(
                integration_name = self.name,
                integration_id = self.integration_id,
                user_iden = self.user_iden,
                account_id = account_id,
                account_name = header_data_container.get('ColData', [])[0].get('value', None),
                beginning_balance = beginning_balance,
                ending_balance = ending_balance,
                transaction_balance = transaction_balance,
                start_period = overall_container.get('StartPeriod', None),
                end_period = overall_container.get('EndPeriod', None),
                create_time = overall_container.get('Time', None)
            )
            self.ledgers.append(ledger)
            for expense_obj in row_data_container:
                if expense_obj.get('ColData', [])[0].get('value', None) != 'Beginning Balance':
                    expenses.append(expense_obj)

            self.grab_expenses(expenses, account_id)

    def save_ledgers(self):
        for ledger in self.ledgers:
            self.update_or_save_instance(Integrations_Quickbooks_Ledger_Reports, ledger, "account_id")

    def save_expenses(self):
        for account_id, ledger_items in self.ledger_lines.items():
            line_item = self.get_instances_if_exists(
                Integrations_Quickbooks_Account_Info,
                Integrations_Quickbooks_Account_Info(account_id=account_id),
                "account_id"
            )
            if line_item:
                for items in ledger_items:
                    items.ledger_ref = line_item[0]
                    self.update_or_save_instance(Integrations_Quickbooks_Ledger_Expenses, items, unique_attr="transaction_id")

    def grab_expenses(self, expenses, account_id):
        for expense in expenses:
            col_data = expense.get('ColData', [])
            item = Integrations_Quickbooks_Ledger_Expenses(
                integration_name = self.name,
                integration_id = self.integration_id,
                user_iden = self.user_iden,
                date = col_data[0].get('value', None),
                transaction_type = col_data[1].get('value', None),
                transaction_id = col_data[1].get('id', None),
                vendor = col_data[3].get('value', None),
                description = col_data[4].get('value', None),
                category = col_data[5].get('value', None),
                amount = col_data[6].get('value', None),
                current_ledger_value = col_data[7].get('value', None)
            )

            if account_id not in self.ledger_lines:
                self.ledger_lines[account_id] = [item]
            else:
                self.ledger_lines[account_id].append(item)