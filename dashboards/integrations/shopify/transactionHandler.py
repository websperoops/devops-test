from . import shopifyHandler

from dashboards.models import Integrations_Shopify_Refund, Integrations_Shopify_Refund_Line_Item, Integrations_Shopify_Refund_Order_Adjustment,\
                              Integrations_Shopify_Order,Integrations_Shopify_Line_Item, Integrations_Shopify_Transaction

from django.db import transaction


class TransactionHandler(shopifyHandler.ShopifyHandler):
    
    def __init__(self, data, integration_id, user_iden,shop_id):


       self.transactions = []
       super(TransactionHandler,self).__init__(data, integration_id, user_iden, shop_id, "transaction")
       
        
    
    def _Handler__save_independent_objects(self):
        with transaction.atomic():
            self.save_transactions()

    def _Handler__save_dependent_objects(self):
        with transaction.atomic():
            pass
    
    def _Handler__parse_data(self):
        for obj in self.data:
            transaction_model = Integrations_Shopify_Transaction(
                transaction_id=getattr(obj,"id",None),
                order_id=obj.order_id,
                amount=getattr(obj,"amount",None),
                authorization=getattr(obj,"authorization",None),
                created_at=getattr(obj,"created_at",None),
                currency=getattr(obj,"currency",None),
                device_id=getattr(obj,"device_id",None),
                error_code=getattr(obj,"error_code",None),
                gateway=getattr(obj,"obj",None),
                kind=getattr(obj,"kind",None),
                location_id=getattr(obj,"location_id",None),
                message=getattr(obj,"message",None),
                receipt=getattr(obj,"receipt",None),
                parent_id=getattr(obj,"parent_id",None),
                processed_at=getattr(obj,"processed_at",None),
                source_name=getattr(obj,"source_name",None),
                status=getattr(obj,"status",None),
                test=getattr(obj,"test",None),
                user_id=getattr(obj,"user_id",None),
            )
            self.transactions.append(transaction_model)
    
    def save_transactions(self):
        for txn in self.transactions:

            orders=Integrations_Shopify_Order.objects.filter(order_id=txn.order_id)
            if len(orders) > 0:
                order=orders[0]
                txn.order_ref_id = order.id
                self.update_or_save_instance(Integrations_Shopify_Transaction,
                                             txn,
                                             "transaction_id")

