from . import shopifyHandler
from dashboards.models import Integrations_Shopify_Shop_Price_Rule, Integrations_Shopify_Shop_Discount_Code, Integrations_Shopify_Shop
from django.db import transaction
from pyactiveresource.connection import ClientError
from shopify.resources.discount_code import DiscountCode
import time


class RuleHandler(shopifyHandler.ShopifyHandler):

    def __init__(self, data, integration_id, user_iden, shop_id):

        self.rules = []
        self.codes = {}
        super(RuleHandler, self).__init__(data, integration_id, user_iden,shop_id,"rule")


    def _Handler__save_independent_objects(self):
        with transaction.atomic():
            self.save_rules()

    def _Handler__save_dependent_objects(self):
        with transaction.atomic():
            self.save_codes()

    def _Handler__parse_data(self):
        for obj in self.data:
            rule_id = getattr(obj, "id", None)
            rule = Integrations_Shopify_Shop_Price_Rule(
                rule_id=rule_id,
                user_iden = self.user_iden,
                integration_id=self.integration_id,
                allocation_method=getattr(obj, "allocation_method", None),
                created_at=getattr(obj, "created_at", None),
                updated_at=getattr(obj, "updated_at", None),
                customer_selection=getattr(obj, "customer_selection", None),
                ends_at=getattr(obj, "end_at", None),
                entitled_collection_ids=getattr(obj, "entitiled_collection_ids", str([])),
                entitled_country_ids=getattr(obj, "entitiled_country_ids", str([])),
                entitled_product_ids=getattr(obj, "entitled_product_ids", str([])),
                entitled_variant_ids=getattr(obj, "entitiled_product_ids", str([])),
                once_per_customer=getattr(obj, "once_per_customer", None),
                prerequisite_customer_ids=getattr(obj, "prerequisite_customer_ids", str([])),
                min_prerequisite_quantity_range=getattr(
                    getattr(obj, "prerequisite_quantity_range", object()),
                    "greater_than_or_equal_to",
                    None
                ),
                prerequisite_saved_search_ids=getattr(obj, "prerequisite_saved_search_ids", str([])),
                max_prerequisite_shipping_price_range=getattr(
                    getattr(obj, "prerequisite_shipping_price_range", object()),
                    "less_than_or_equal_to",
                    None
                ),
                min_prerequisite_subtotal_range=getattr(
                    getattr(obj, "prerequisite_subtotal_range", object()),
                    "greater_than_or_equal_to",
                    None
                ),
                starts_at=getattr(obj, "starts_at", None),
                target_selection=getattr(obj, "target_selection", None),
                target_type=getattr(obj, "target_type", None),
                title=getattr(obj, "title", None),
                usage_limit=getattr(obj, "usage_limit", None),
                prerequisite_product_ids=getattr(obj, "prerequisite_product_ids", str([])),
                prerequisite_variant_ids=getattr(obj, "prerequisite_variant_ids", str([])),
                prerequisite_collection_ids=getattr(obj, "prerequisite_collection_ids", str([])),
                value=getattr(obj, "value", None),
                value_type=getattr(obj,"value_type", None),
                prerequisite_quantity=getattr(obj, "prerequisite_quantity",None),
                entitled_quantity=getattr(obj, "entitled_quantity", None),
                allocation_limit=getattr(obj, "allocation_limit", None)
            )
            self.rules.append(rule)
            self.grab_codes(rule_id)


    def save_rules(self):
        shop = Integrations_Shopify_Shop.objects.get(shop_id=self.shop_id)
        for rule in self.rules:
            rule.shop=shop
            self.update_or_save_instance(Integrations_Shopify_Shop_Price_Rule, rule, "rule_id")

    def save_codes(self):
        for r_id, codes in self.codes.items():
            rules = self.get_instances_if_exists(
                Integrations_Shopify_Shop_Price_Rule,
                Integrations_Shopify_Shop_Price_Rule(rule_id="r_id"),
                "rule_id"
            )
            if rules:
                for code in codes:
                    code.price_rule = rules[0]
                    self.update_or_save_instance(Integrations_Shopify_Shop_Discount_Code, code, "discount_id")

    def grab_codes(self, rule_id):
        SLEEPTIME = 0
        while True:
            try:
                codes = DiscountCode.find(price_rule_id=rule_id)
                SLEEPTIME = 0
                break
            except ClientError as e:
                SLEEPTIME = 1 if SLEEPTIME == 0 else SLEEPTIME*2
                time.sleep(SLEEPTIME)

        for code in codes:
            discount_id=getattr(code, "id", None)
            tuple = Integrations_Shopify_Shop_Discount_Code(
                price_rule_id=rule_id,
                discount_id=discount_id,
                code=getattr(code, "code", None),
                created_at=getattr(code, "created_at", None),
                updated_at=getattr(code, "updated_at", None),
                usage_count=getattr(code, "usage_count", None)
            )
            if rule_id not in self.codes:
                self.codes[rule_id] = [code]
            else:
                self.codes[rule_id].append(code)
