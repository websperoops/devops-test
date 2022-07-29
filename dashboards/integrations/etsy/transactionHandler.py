from . import etsyAPI
from . import etsyHandler

from dashboards.models import Integrations_Etsy_Transaction, Integrations_Etsy_Transaction_BuyerFeedback, Integrations_Etsy_Transaction_Material, \
                              Integrations_Etsy_Transaction_Tag, Integrations_Etsy_Shop

from django.db import transaction


class TransactionHandler(etsyHandler.EtsyHandler):

    def __init__(self, data, integration_id, user_iden, shop_id, request):
        self.transactions = []
        self.tags = {}
        self.materials = {}
        self.feedback =[]
        self.shop_id = shop_id
        self.request = request
        super(TransactionHandler, self).__init__(data, integration_id, user_iden, shop_id, "receipt")

    def _Handler__save_independent_objects(self):
        with transaction.atomic():
            self.save_transactions()

    def _Handler__save_dependent_objects(self):
        with transaction.atomic():
            self.save_tags()
            self.save_materials()
            self.save_feedback()

    def _Handler__parse_data(self):
        for obj in self.data:
            transaction = Integrations_Etsy_Transaction(
                integration_id = self.integration_id,
                shop_id = self.shop_id,
                user_iden = self.user_iden,
                transaction_id = obj.get("transaction_id", None),
                title = obj.get("title", None),
                description = obj.get("description", None),
                seller_user_id = obj.get("seller_user_id", None),
                buyer_user_id = obj.get("buyer_user_id", None),
                creation_tsz = etsyAPI.unix2UTC(obj.get("creation_tsz", None)),
                paid_tsz = etsyAPI.unix2UTC(obj.get("paid_tsz", None)),
                shipped_tsz = etsyAPI.unix2UTC(obj.get("shipped_tsz", None)),
                price = obj.get("price", None),
                currency_code = obj.get("currency_code", None),
                quantity = obj.get("quantity", None),
                image_listing_id = obj.get("image_listing_id", None),
                receipt_id = obj.get("receipt_id", None),
                shipping_cost = obj.get("shipping_cost", None),
                is_digital = etsyAPI.etsyBool(obj.get("is_digital", None)),
                file_data = obj.get("file_data", None),
                listing_id = obj.get("listing_id", None),
                is_quick_sale = etsyAPI.etsyBool(obj.get("is_quick_sale", None)),
                seller_feedback_id = obj.get("seller_feedback_id", None),
                buyer_feedback_id = obj.get("buyer_feedback_id", None),
                transaction_type = obj.get("transaction_type", None),
                url = obj.get("url", None)
            )
            self.transactions.append(transaction)

            tags = obj.get("tags", None)
            materials = obj.get("materials", None)
            
            self.grab_tags(transaction.transaction_id, tags)
            self.grab_materials(transaction.transaction_id, materials)

            feedback = etsyAPI.getFeedback(self.request, transaction.seller_user_id)
            self.grab_feedback(feedback)

    def save_transactions(self):
        for transaction in self.transactions:
            shop = self.get_instances_if_exists(
                Integrations_Etsy_Shop,
                Integrations_Etsy_Shop(shop_id=transaction.shop_id),
                "shop_id"
            )
            transaction.shop_ref = None if not shop else shop[0]
            self.update_or_save_instance(Integrations_Etsy_Transaction, transaction, unique_attr="transaction_id")    

    def grab_tags(self, transaction_id, tags):
        self.tags[transaction_id] = []
        for tag in tags:
            self.tags[transaction_id].append(Integrations_Etsy_Transaction_Tag(tag=tag))

    def grab_materials(self, transaction_id, materials):
        self.materials[transaction_id] = []
        for material in materials:
            self.materials[transaction_id].append(Integrations_Etsy_Transaction_Material(material=material))

    def save_tags(self):
        for t_id, tags in self.tags.items():
            transaction = self.get_instances_if_exists(
                Integrations_Etsy_Transaction,
                Integrations_Etsy_Transaction(transaction_id=t_id),
                "transaction_id"
            )
            for tag in tags:
                tag.transaction_ref = None if not transaction else transaction[0]
                self.update_or_save_instance(Integrations_Etsy_Transaction_Tag, tag, unique_attr=None)

    def save_materials(self):
        for t_id, materials in self.materials.items():
            transaction = self.get_instances_if_exists(
                Integrations_Etsy_Transaction,
                Integrations_Etsy_Transaction(transaction_id=t_id),
                "transaction_id"
            )
            for material in materials:
                material.transaction_ref = None if not transaction else transaction[0]
                self.update_or_save_instance(Integrations_Etsy_Transaction_Material, material, unique_attr=None)

    def grab_feedback(self, feedbacks):
        for obj in feedbacks:
            feedback = Integrations_Etsy_Transaction_BuyerFeedback(
                transaction_id = obj.get("transaction_id", None),
                user_iden = self.user_iden,
                feedback_id = obj.get("feedback_id", None),
                creator_user_id = obj.get("creator_user_id", None),
                target_user_id = obj.get("target_user_id", None),
                seller_user_id = obj.get("seller_user_id", None),
                buyer_user_id = obj.get("buyer_user_id", None),
                creation_tsz = etsyAPI.unix2UTC(obj.get("creation_tsz", None)),
                #message = obj.get("message", None),
                value = obj.get("value", None),
                image_feedback_id = obj.get("image_feedback_id", None),
                image_url_25x25 = obj.get("image_url_25x25", None),
                image_url_155x125 = obj.get("image_url_155x125", None),
                image_url_fullxfull = obj.get("image_url_fullxfull", None)
            )
            self.feedback.append(feedback)

    def save_feedback(self):
        for fb in self.feedback:
            transaction = self.get_instances_if_exists(
                Integrations_Etsy_Transaction,
                Integrations_Etsy_Transaction(transaction_id=fb.transaction_id),
                "transaction_id"
            )
            fb.transaction_ref = None if not transaction else transaction[0]
            self.update_or_save_instance(Integrations_Etsy_Transaction_BuyerFeedback, fb, unique_attr="feedback_id") 
