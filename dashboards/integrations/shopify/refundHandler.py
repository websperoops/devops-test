from . import shopifyHandler

from dashboards.models import Integrations_Shopify_Refund, Integrations_Shopify_Refund_Line_Item, Integrations_Shopify_Refund_Order_Adjustment,\
                              Integrations_Shopify_Order,Integrations_Shopify_Line_Item, Integrations_Shopify_Transaction

from django.db import transaction


class RefundHandler(shopifyHandler.ShopifyHandler):

    def __init__(self, data, integration_id, user_iden,shop_id):

        '''
        NOTE:
        When passing in data to this handler you MUST set all refunds with an attribute refund.order_id = order_id
        from the order id you queried the endpoint you called. That data is not guaranteed to be in the response data
        '''

        self.refunds = {}
        self.refund_line_items = {}
        self.adjustments = []
        self.transaction_ids = {}
        super(RefundHandler, self).__init__(data, integration_id, user_iden,shop_id,"refund")

    def _Handler__save_independent_objects(self):
        with transaction.atomic():
            self.save_refunds()

    def _Handler__save_dependent_objects(self):
        with transaction.atomic():
            self.save_refund_line_items()
            self.save_adjustments()
            self.link_transactions()

    def _Handler__parse_data(self):
        print(self.data)
        for obj in self.data:
            refund = Integrations_Shopify_Refund(
                 refund_id=getattr(obj, "id", None),
                 created_at=getattr(obj, "created_at", None),
                 processed_at=getattr(obj, "processed_at", None),
                 note=getattr(obj, "note", None),
                 restock=getattr(obj, "restock", None),
                 user_id=getattr(obj, "user_id", None)
             )

            line_items = getattr(obj, "refund_line_items",[])
            order_adjustments =  getattr(obj,"order_adjustments",[])
            transactions = getattr(obj,"transactions",[])
            self.transaction_ids[obj.id] = map(
                lambda txn : txn.id,transactions
            )

            order_id = obj.order_id

            if order_id in self.refunds:
                self.refunds[order_id].append(refund)
            else:
                self.refunds[order_id] = [refund]

            self.grab_refund_line_items(obj, line_items)
            print(line_items)
            self.grab_adjustments(obj, order_adjustments)


    def save_refunds(self):
        for oid, refunds in self.refunds.items():
            orders = self.get_instances_if_exists(Integrations_Shopify_Order,
                                                  Integrations_Shopify_Order(order_id=oid),
                                                  "order_id"
                                                  )
            if orders:
                order = orders[0]
                for refund in refunds:
                    refund.order = order
                    self.update_or_save_instance(Integrations_Shopify_Refund, refund, "refund_id")


    def save_refund_line_items(self):
        for r_id, items in self.refund_line_items.items():
            refunds = self.get_instances_if_exists(
                Integrations_Shopify_Refund,
                Integrations_Shopify_Refund(refund_id=r_id),
                "refund_id"
                )

            for line_item in items:
                if refunds:
                    line_item.refund=refunds[0]

                regular_line_items = self.get_instances_if_exists(
                    Integrations_Shopify_Line_Item,
                    Integrations_Shopify_Line_Item(line_item_id=line_item.line_item_id),
                    'line_item_id'
                )
                if regular_line_items:
                    line_item.line_item_ref=regular_line_items[0]

                self.update_or_save_instance(Integrations_Shopify_Refund_Line_Item, line_item, "refund_line_item_id")


    def save_adjustments(self):
        for adj in self.adjustments:
            order_id = adj.order_id
            refund_id = adj.order_id
            refunds = self.get_instances_if_exists(
                Integrations_Shopify_Refund,
                Integrations_Shopify_Refund(refund_id=refund_id),
                "refund_id"
                )
            orders = self.get_instances_if_exists(
                Integrations_Shopify_Order,
                Integrations_Shopify_Refund(order_id=order_id),
                "order_id"
                )
            if orders:
                adj.order_ref = orders[0]
            if refunds:
                adj.refund_ref = refunds[0]

            self.update_or_save_instance(Integrations_Shopify_Refund_Order_Adjustment,
                                         adj,
                                         "order_adjustment_id")


    def link_transactions(self):
        for r_id, txn_ids in self.transaction_ids.items():
            refunds = self.get_instances_if_exists(Integrations_Shopify_Refund, Integrations_Shopify_Refund(refund_id=r_id),"refund_id")
            if refunds:
                refund = refunds[0]
                for id in txn_ids:
                    txns = self.get_instances_if_exists(Integrations_Shopify_Transaction, Integrations_Shopify_Transaction(transaction_id=id),"transaction_id")
                    if txns:
                        for txn in txns:
                            txn.refund_ref = refund
                            txn.refund_id = r_id
                            txn.save()


    def grab_refund_line_items(self, refund, line_items):
        refund_id = getattr(refund, "id", None)
        for line_item in line_items:
            refund_line_item = Integrations_Shopify_Refund_Line_Item(
                refund_line_item_id = getattr(line_item,"id",None),
                line_item_id = getattr(line_item,"line_item_id",None),
                quantity= getattr(line_item,"quantity",None),
                location_id=getattr(line_item,"location_id",None),
                restock_type=getattr(line_item,"restock_type",None),
                subtotal = getattr(line_item,"subtotal",None),
                total_tax = getattr(line_item,"total_tax",None),
                )

            if refund_id in self.refund_line_items:
                self.refund_line_items[refund_id].append(refund_line_item)
            else:
                self.refund_line_items[refund_id] = [refund_line_item]


    def grab_adjustments(self, refund,adjustments):
        refund_id = getattr(refund, "id", None)
        for adj in adjustments:
            adj = Integrations_Shopify_Refund_Order_Adjustment(
                order_adjustment_id=getattr(adj,"id",None),
                order_id=getattr(adj,"order_id",None),
                refund_id=getattr(adj,"refund_id",None),
                amount=getattr(adj,"amount",None),
                tax_amount=getattr(adj,"tax_amount",None),
                kind=getattr(adj,"kind",None),
                reason=getattr(adj,"reason",None)
            )
            self.adjustments.append(adj)
