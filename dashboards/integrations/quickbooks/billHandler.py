from . import quickbooksHandler
from dashboards.models import Integrations_Quickbooks_Bills, Integrations_Quickbooks_Bill_Line_Items
from django.db import transaction
import logging


class BillHandler(quickbooksHandler.QuickbooksHandler):

    logger = logging.getLogger(__name__)

    def __init__(self, data, integration_id, user_iden, integration_name, name):
        self.bills = []
        self.line_items = {}

        self.index_container = {
            'AccountBasedExpenseLineDetail': 'AccountRef',
            'ItemBasedExpenseLineDetail': 'ItemRef'
        }

        super(BillHandler, self).__init__(data, integration_id, user_iden, "quickbooks", name)

    def _Handler__save_independent_objects(self):
        with transaction.atomic():
            self.save_bills()
    
    def _Handler__save_dependent_objects(self):
        with transaction.atomic():
            self.save_line_items()
    
    def _Handler__parse_data(self):
        self.data = self.data.get('QueryResponse', {}).get('Bill', [])
        for obj in self.data:
            meta_data = obj.get('MetaData', {})
            bill_id = obj.get('Id', None)
            bill = Integrations_Quickbooks_Bills(
                integration_name = self.name,
                integration_id = self.integration_id,
                vendor_name = obj.get('VendorRef', {}).get('name', None),
                account_name = obj.get('APAccountRef', {}).get('name', None),
                user_iden=self.user_iden,
                due_date = obj.get('DueDate', None),
                balance = obj.get('Balance', None),
                bill_id = bill_id,
                create_time = meta_data.get('CreateTime', None),
                last_update_time = meta_data.get('LastUpdatedTime', None)
            )
            lines = obj.get('Line', [])
            self.grab_line_items(lines, bill_id)
            self.bills.append(bill)

    def save_bills(self):
        for bill in self.bills:
            self.update_or_save_instance(Integrations_Quickbooks_Bills, bill, "bill_id")
    
    def save_line_items(self):
        for bill_id, l_items in self.line_items.items():
            line_item = self.get_instances_if_exists(
                Integrations_Quickbooks_Bills,
                Integrations_Quickbooks_Bills(bill_id=bill_id),
                "bill_id"
            )
            if line_item:
                for items in l_items:
                    items.bill_ref = line_item[0]
                    self.update_or_save_instance(Integrations_Quickbooks_Bill_Line_Items, items, unique_attr="item_id")
    
    def grab_line_items(self, lines, bill_id):
        if lines:
            for line in lines:
                detail_type = line.get('DetailType', None)
                index = self.index_container.get(detail_type, None)
                item_container = line.get(detail_type, {})
                detail_ref = item_container.get(index, {})

                line_item = Integrations_Quickbooks_Bill_Line_Items(
                    integration_id   = self.integration_id,
                    integration_name = self.integration_name,
                    user_iden = self.user_iden,
                    item_id = detail_ref.get('value', None),
                    item_name = detail_ref.get('name', None),
                    description = line.get('Description', None),
                    amount = line.get('Amount', None),
                    detail_type = detail_type,
                    quantity = item_container.get('Qty', None),
                    unit_price = item_container.get('UnitPrice', None)
                )
                if bill_id not in self.line_items:
                    self.line_items[bill_id] = [line_item]
                else:
                    self.line_items[bill_id].append(line_item)
