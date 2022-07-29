from . import customerHandler, shopifyHandler

from dashboards.models import Integrations_Shopify_Abandoned_Checkouts, Integrations_Shopify_Abandoned_Checkout_Line_Items, \
    Integrations_Shopify_Product, Integrations_Shopify_Product_Variant, Integrations_Shopify_Customer, Integrations_Shopify_Shop

from django.db import transaction


class CheckoutHandler(shopifyHandler.ShopifyHandler):

    def __init__(self, data, integration_id, user_iden, shop_id):

        self.checkouts = []
        self.line_items = {}
        self.customers = {}
        super(CheckoutHandler, self).__init__(data, integration_id, user_iden,shop_id,"checkout")

    def _Handler__save_independent_objects(self):

        cHandler = customerHandler.CustomerHandler(self.customers.values(), self.integration_id, self.user_iden, self.shop_id)
        cHandler.save_all_objects()

        with transaction.atomic():
            self.save_checkouts()

    def _Handler__save_dependent_objects(self):
        with transaction.atomic():
            self.save_line_items()

    def _Handler__parse_data(self):
        for obj in self.data:
            checkout_id=getattr(obj, "id", None)
            sh_lines = getattr(obj, "shipping_lines", None)
            if len(sh_lines) > 0:
                shipping_price = getattr(sh_lines[0], "price", 0)
            else:
                shipping_price=0

            checkout = Integrations_Shopify_Abandoned_Checkouts(integration_id=self.integration_id,
                user_iden=self.user_iden,
                checkout_id=checkout_id,
                created_at=getattr(obj, "created_at", None),
                closed_at=getattr(obj, "closed_at", None),
                completed_at=getattr(obj, "completed_at", None),
                landing_site=getattr(obj, "landing_site", None),
                abandoned_checkout_url=getattr(obj, "abandoned_checkout_url", None),
                subtotal_price = getattr(obj, "subtotal_price", None),
                total_price = getattr(obj, "total_price", None),
                shipping_price = shipping_price,
                total_tax=getattr(obj, "total_tax", None),
                cart_token = getattr(obj, "cart_token", None),
                buyer_accepts_marketing=getattr(obj, "buyer_accepts_marketing", None),
                taxable=getattr(obj, "taxes_included", None),
                customer=getattr(obj, "customer", None),
                discount_codes=getattr(obj, "discount_codes", None),
                total_discounts=getattr(obj, "total_discounts", 0),
                total_line_items_price=getattr(obj, "total_line_items_price",0),
                gateway=getattr(obj, "gateway", None),
            )
            self.checkouts.append(checkout)
            line_items = getattr(obj, "line_items", [])
            self.grab_line_items(checkout.checkout_id, line_items)


    def save_checkouts(self):
        shop = Integrations_Shopify_Shop.objects.get(shop_id=self.shop_id)
        for checkout in self.checkouts:
            checkout.shop=shop
            c_id = checkout.customer.id

            customers = self.get_instances_if_exists(
                Integrations_Shopify_Customer,
                Integrations_Shopify_Customer(customer_id=c_id),
                "customer_id"
            )

            if customers:
                checkout.customer_ref = customers[0]


            self.update_or_save_instance(Integrations_Shopify_Abandoned_Checkouts, checkout, "checkout_id")


    def save_line_items(self):
        for c_id, items in self.line_items.items():
            checkouts = self.get_instances_if_exists(
                Integrations_Shopify_Abandoned_Checkouts,
                Integrations_Shopify_Abandoned_Checkouts(checkout_id=c_id),
                "checkout_id"
            )
            if checkouts:
                for item in items:
                    item.checkout = checkouts[0]
                    p_id, v_id = item.product_id, item.variant_id
                    item.p_id = p_id
                    item.v_id = v_id
                    item.product_id = None
                    item.variant_id = None
                    if p_id:
                        products = self.get_instances_if_exists(
                            Integrations_Shopify_Product,
                            Integrations_Shopify_Product(product_id=p_id),
                            "product_id"
                        )
                        if products:
                            item.product_ref = products[0]
                    if v_id:
                        variants = self.get_instances_if_exists(
                            Integrations_Shopify_Product_Variant,
                            Integrations_Shopify_Product_Variant(variant_id=v_id),
                            "variant_id"
                        )
                        if variants:
                            item.variant_ref = variants[0]
                    self.update_or_save_instance(Integrations_Shopify_Abandoned_Checkout_Line_Items, item, unique_attr=None)


    def grab_line_items(self, checkout_id, line_items):
        for line_item in line_items:
            c_line_item = Integrations_Shopify_Abandoned_Checkout_Line_Items(
                fulfillment_service=getattr(line_item, "fulfillment_service",None),
                grams=getattr(line_item, "grams",None),
                price=getattr(line_item, "price",None),
                product_id=getattr(line_item, "product_id",None),
                quantity=getattr(line_item, "quantity",None),
                requires_shipping=getattr(line_item, "requires_shipping",None),
                sku=getattr(line_item, "sku",None),
                title=getattr(line_item, "title",None),
                variant_id=getattr(line_item, "variant_id",None),
                variant_title=getattr(line_item, "variant_title",None),
                vendor=getattr(line_item, "vendor",None)
            )

            if checkout_id not in self.line_items:
                self.line_items[checkout_id] = [c_line_item]
            else:
                self.line_items[checkout_id].append(c_line_item)


    def grab_customer(self, checkout):
        cust = getattr(checkout, "customer", None)
        c_id=getattr(cust, "id", None)
        if not c_id:
            return None
        customer = Integrations_Shopify_Customer(
            integration_id=self.integration_id,
            customer_id =c_id,
            user_iden=self.user_iden,
            email= getattr(cust, "email", None),
            accepts_marketing=getattr(cust, "accepts_marketing", None),
            created_at=getattr(cust, "created_at", None),
            updated_at=getattr(cust, "updated_at", None),
            first_name=getattr(cust, "first_name", None),
            last_name=getattr(cust, "last_name", None),
            orders_count=getattr(cust, "orders_count", None),
            state=getattr(cust, "state", None),
            total_spent=getattr(cust, "total_spent", None),
            last_order_id=getattr(cust, "last_order_id", None),
            tax_exempt=getattr(cust, "tax_exempt", None),
            phone= getattr(cust, "phone", None),
            tags=getattr(cust, "tags", None),
            last_order_name=getattr(cust, "last_order_name", None),
            currency=getattr(cust, "currency", "USD"),
            default_address=getattr(cust, "default_address",None)
        )

        ## NOTE: API reponse data comes MOST RECENT first, so if we recive repeat customer data within a reponse,
        ## we only care about saving the first one (i.e. the most recent one) along with it's related addresses
        if c_id not in self.customers:
            self.customers[c_id]=customer

        return self.customers[c_id]
