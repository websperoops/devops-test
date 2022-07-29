from . import etsyAPI
from . import etsyHandler

from dashboards.models import Integrations_Etsy_Receipt, Integrations_Etsy_Receipt_Shipment, Integrations_Etsy_Shop, \
                              Integrations_Etsy_Receipt_Payment, Integrations_Etsy_Receipt_Payment_Adjustment, \
                              Integrations_Etsy_Receipt_Payment_Adjustment_Item

from django.db import transaction


class ReceiptHandler(etsyHandler.EtsyHandler):

    def __init__(self, data, integration_id, user_iden, shop_id, request):
        self.receipts = []
        self.shipments = []
        self.payments = []
        self.adjustments = []
        self.adj_items =[]
        self.shop_id = shop_id
        self.request = request
        super(ReceiptHandler, self).__init__(data, integration_id, user_iden, shop_id, "receipt")

    def _Handler__save_independent_objects(self):
        with transaction.atomic():
            self.save_receipts()

    def _Handler__save_dependent_objects(self):
        def save_dep_1():
            with transaction.atomic():
                self.save_shipments()
                self.save_payments()
        def save_dep_2():
            with transaction.atomic():
                self.save_adjustments()
        def save_dep_3():
            with transaction.atomic():
                self.save_adjustment_items()

        save_dep_1()
        save_dep_2()
        save_dep_3()

    def _Handler__parse_data(self):
        for obj in self.data:
            rec_id = obj.get("receipt_id", None)
            receipt = Integrations_Etsy_Receipt(
                integration_id = self.integration_id,
                user_iden = self.user_iden,
                shop_id = self.shop_id,
                receipt_id = rec_id,
                receipt_type = obj.get("receipt_type", None),
                order_id = obj.get("order_id", None),
                seller_user_id = obj.get("seller_user_id", None),
                buyer_user_id = obj.get("buyer_user_id", None),
                creation_tsz = etsyAPI.unix2UTC(obj.get("creation_tsz", None)),
                can_refund = etsyAPI.etsyBool(obj.get("can_refund", None)),
                last_modified_tsz = etsyAPI.unix2UTC(obj.get("last_modified_tsz", None)),
                name = obj.get("name", None),
                first_line = obj.get("first_line", None),
                second_line = obj.get("second_line", None),
                city = obj.get("city", None),
                state = obj.get("state", None),
                zip = obj.get("zip", None),
                formatted_address = obj.get("formatted_address", None),
                country_id = obj.get("country_id", None),
                payment_method = obj.get("payment_method", None),
                payment_email = obj.get("payment_email", None),
                message_from_seller = obj.get("message_from_seller", None),
                message_from_buyer = obj.get("message_from_buyer", None),
                was_paid = etsyAPI.etsyBool(obj.get("was_paid", None)),
                total_tax_cost = obj.get("total_tax_cost", None),
                total_vat_cost = obj.get("total_vat_cost", None),
                total_price = obj.get("total_price", None),
                total_shipping_cost = obj.get("total_shipping cost", None),
                currency_code = obj.get("currency_code", None),
                message_from_payment = obj.get("message_from_payment", None),
                was_shipped = etsyAPI.etsyBool(obj.get("was_shipped", None)),
                buyer_email = obj.get("buyer_email", None),
                seller_email = obj.get("seller_email", None),
                is_gift = etsyAPI.etsyBool(obj.get("is_gift", None)),
                needs_gift_wrap = obj.get("needs_gift_wrap", None),
                gift_message = obj.get("gift_message", None),
                gift_wrap_price = obj.get("gift_wrap_price", None),
                discount_amt = obj.get("discount_amt", None),
                subtotal = obj.get("subtotal", None),
                grandtotal = obj.get("grand_total", None),
                adjusted_grandtotal = obj.get("adjusted_grandtotal", None),
                buyer_adjusted_grandtotal = obj.get("buyer_adjusted_grandtotal", None)
            )
            self.receipts.append(receipt)

            shipments = obj.get("shipments", None)
            self.grab_shipments(shipments, rec_id)

            payments = etsyAPI.getPayments(self.request, self.shop_id, rec_id)
            self.grab_payments(payments, rec_id)

    def save_receipts(self):
        for rec in self.receipts:
            shop = self.get_instances_if_exists(
                Integrations_Etsy_Shop,
                Integrations_Etsy_Shop(shop_id=rec.shop_id),
                "shop_id"
            )
            rec.shop_ref = None if not shop else shop[0]
            self.update_or_save_instance(Integrations_Etsy_Receipt, rec, unique_attr="receipt_id")    

    def grab_shipments(self, shipments, rec_id):
        for obj in shipments:
            shipment = Integrations_Etsy_Receipt_Shipment(
                carrier_name = obj.get("carrier_name", None),
                receipt_shipping_id = obj.get("receipt_shipping_id", None),
                tracking_code = obj.get("tracking_code", None),
                tracking_url = obj.get("tracking_url", None),
                buyer_note = obj.get("buyer_note", None),
                notification_date = obj.get("notification_date", None),
                receipt_id = rec_id
            )
            self.shipments.append(shipment)

    def save_shipments(self):
        for ship in self.shipments:
            receipt = self.get_instances_if_exists(
                Integrations_Etsy_Receipt,
                Integrations_Etsy_Receipt(receipt_id=ship.receipt_id),
                "receipt_id"
            )
            ship.receipt_ref = None if not receipt else receipt[0]
            self.update_or_save_instance(Integrations_Etsy_Receipt_Shipment, ship, unique_attr="receipt_shipping_id")   

    def grab_payments(self, payments, rec_id):
        for obj in payments:
            payment = Integrations_Etsy_Receipt_Payment(
                receipt_id = rec_id,
                user_iden = self.user_iden,
                payment_id = obj.get("payment_id", None),
                buyer_user_id = obj.get("buyer_user_id", None),
                shop_id = obj.get("shop_id", None),
                amount_gross = etsyAPI.etsyDollars(obj.get("amount_gross", None)),
                amount_fees = etsyAPI.etsyDollars(obj.get("amount_fees", None)),
                amount_net = etsyAPI.etsyDollars(obj.get("amount_net", None)),
                posted_gross = etsyAPI.etsyDollars(obj.get("posted_gross", None)),
                posted_fees = etsyAPI.etsyDollars(obj.get("posted_fees", None)),
                posted_net = etsyAPI.etsyDollars(obj.get("posted_net", None)),
                adjusted_gross = etsyAPI.etsyDollars(obj.get("adjusted_gross", None)),
                adjusted_fees = etsyAPI.etsyDollars(obj.get("adjusted_fees", None)),
                adjusted_net = etsyAPI.etsyDollars(obj.get("adjusted_net", None)),
                currency = obj.get("currency", None),
                shop_currency = obj.get("shop_currency", None),
                buyer_currency = obj.get("buyer_currency", None),
                shipping_user_id = obj.get("shipping_user_id", None),
                shipping_address_id = obj.get("shipping_address_id", None),
                billing_address_id = obj.get("billing_address_id", None),
                status = obj.get("status", None),
                shipped_date = etsyAPI.unix2UTC(obj.get("shipped_date", None)),
                create_date = etsyAPI.unix2UTC(obj.get("create_date", None)),
                update_date = etsyAPI.unix2UTC(obj.get("update_date", None)),
            )
            self.payments.append(payment)

            adjustments = etsyAPI.getPaymentAdjustments(self.request, payment.payment_id)
            self.grab_adjustments(adjustments)

    def save_payments(self):
        for payment in self.payments:
            receipt = self.get_instances_if_exists(
                Integrations_Etsy_Receipt,
                Integrations_Etsy_Receipt(receipt_id=payment.receipt_id),
                "receipt_id"
            )
            shop = self.get_instances_if_exists(
                Integrations_Etsy_Shop,
                Integrations_Etsy_Shop(shop_id=payment.shop_id),
                "shop_id"
            )
            payment.receipt_ref = None if not receipt else receipt[0]
            payment.shop_ref = None if not shop else shop[0]
            self.update_or_save_instance(Integrations_Etsy_Receipt_Payment, payment, unique_attr="payment_id")   

    def grab_adjustments(self, adjs):
        for obj in adjs:
            adj = Integrations_Etsy_Receipt_Payment_Adjustment(
                payment_id = obj.get("payment_id", None),
                user_iden = self.user_iden,
                payment_adjustment_id = obj.get("payment_adjustment_id", None),
                status = obj.get("status", None),
                is_success = etsyAPI.etsyBool(obj.get("is_success", None)),
                user_id = obj.get("user_id", None),
                reason_code = obj.get("reason_code", None),
                total_adjustment_amount = etsyAPI.etsyDollars(obj.get("total_adjustment_amount", None)),
                shop_total_adjustment_amount = etsyAPI.etsyDollars(obj.get("shop_total_adjustment_amount", None)),
                buyer_total_adjustment_amount = etsyAPI.etsyDollars(obj.get("buyer_total_adjustment_amount", None)),
                total_fee_adjustment_amount = etsyAPI.etsyDollars(obj.get("total_fee_adjustment_amount", None)),
                create_date = etsyAPI.unix2UTC(obj.get("create_date", None)),
                update_date = etsyAPI.unix2UTC(obj.get("update_date", None))
            )
            self.adjustments.append(adj)
            
            items = etsyAPI.getPaymentAdjustmentItems(self.request, adj.payment_id, adj.payment_adjustment_id)
            self.grab_adjustment_items(items)

    def save_adjustments(self):
        for adj in self.adjustments:
            payment = self.get_instances_if_exists(
                Integrations_Etsy_Receipt_Payment,
                Integrations_Etsy_Receipt_Payment(payment_id=adj.payment_id),
                "payment_id"
            )
            adj.payment_ref = None if not payment else payment[0]
            self.update_or_save_instance(Integrations_Etsy_Receipt_Payment_Adjustment, adj, unique_attr="payment_adjustment_id")   

    def grab_adjustment_items(self, items):
        for obj in items:
            item = Integrations_Etsy_Receipt_Payment_Adjustment_Item(
                payment_adjustment_id = obj.get("payment_adjustment_id", None),
                user_iden = self.user_iden,
                payment_adjustment_item_id = obj.get("payment_adjustment_item_id", None),
                adjustment_type = obj.get("adjustment_type", None),
                amount = etsyAPI.etsyDollars(obj.get("amount", None)),
                transaction_id = obj.get("transaction_id", None),
                create_date = etsyAPI.unix2UTC(obj.get("create_date", None)),
            )
            self.adj_items.append(item)

    def save_adjustment_items(self):
        for item in self.adj_items:
            adj = self.get_instances_if_exists(
                Integrations_Etsy_Receipt_Payment_Adjustment,
                Integrations_Etsy_Receipt_Payment_Adjustment(payment_adjustment_id=item.payment_adjustment_id),
                "payment_adjustment_id"
            )
            item.adjustment_ref = None if not adj else adj[0]
            self.update_or_save_instance(Integrations_Etsy_Receipt_Payment_Adjustment_Item, item, unique_attr="payment_adjustment_item_id")   