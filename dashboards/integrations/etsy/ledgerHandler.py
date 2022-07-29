from . import etsyAPI
from . import etsyHandler
from dashboards.models import Integrations_Etsy_Ledger, Integrations_Etsy_Ledger_Entry, Integrations_Etsy_Shop
from django.db import transaction


class LedgerHandler(etsyHandler.EtsyHandler):

    def __init__(self, data, integration_id, user_iden, shop_id, request):
        self.ledgers = []
        self.entries = []
        self.shop_id = shop_id
        self.request = request
        super(LedgerHandler, self).__init__(data, integration_id, user_iden, shop_id, "listing")

    def _Handler__save_independent_objects(self):
        with transaction.atomic():
            self.save_ledgers()

    def _Handler__save_dependent_objects(self):
        with transaction.atomic():
            self.save_ledger_entries()

    def _Handler__parse_data(self):
        for obj in self.data:
            entry = Integrations_Etsy_Ledger_Entry(
                ledger_id = obj.get("ledger_id", None),
                user_iden = self.user_iden,
                ledger_entry_id = obj.get("ledger_entry_id", None),
                sequence = obj.get("sequence", None),
                credit_amount = etsyAPI.etsyDollars(obj.get("credit_amount", None)),
                debit_amount = etsyAPI.etsyDollars(obj.get("debit_amount", None)),
                entry_type = obj.get("entry_type", None),
                reference_id = obj.get("reference_id", None),
                running_balance = etsyAPI.etsyDollars(obj.get("running_balance", None)),
                create_date = etsyAPI.unix2UTC(obj.get("create_date", None))
            )
            
            self.entries.append(entry)

            ledger = etsyAPI.getLedger(self.request, self.shop_id)

            self.grab_ledgers(ledger)

    def save_ledger_entries(self):
        for entry in self.entries:
            ledger = self.get_instances_if_exists(
                Integrations_Etsy_Ledger,
                Integrations_Etsy_Ledger(ledger_id=entry.ledger_id),
                "ledger_id"
            )
            entry.ledger_ref = None if not ledger else ledger[0]
            self.update_or_save_instance(Integrations_Etsy_Ledger_Entry, entry, unique_attr="ledger_entry_id")    

    def grab_ledgers(self, ledgers):
        for obj in ledgers:
                ledger = Integrations_Etsy_Ledger(
                    integration_id = self.integration_id,
                    shop_id = obj.get("shop_id", None),
                    user_iden = self.user_iden,
                    ledger_id = obj.get("ledger_id", None),
                    currency = obj.get("currency", None),
                    create_date = etsyAPI.unix2UTC(obj.get("create_date", None)),
                    update_date = etsyAPI.unix2UTC(obj.get("update_date", None)),
                )
                self.ledgers.append(ledger)

    def save_ledgers(self):
        for ledger in self.ledgers:
            shop = self.get_instances_if_exists(
                Integrations_Etsy_Shop,
                Integrations_Etsy_Shop(shop_id=ledger.shop_id),
                "shop_id"
            )
            ledger.shop_ref = None if not shop else shop[0]
            self.update_or_save_instance(Integrations_Etsy_Ledger, ledger, unique_attr="ledger_id") 
