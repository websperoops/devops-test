from . import shopifyHandler, customerHandler
from .utils import shopify_api_request

from dashboards.models import Integrations_Shopify_Order, Integrations_Shopify_Customer, \
                              Integrations_Shopify_Discount_Application, Integrations_Shopify_Discount_Code, Integrations_Shopify_Fulfillment, \
                              Integrations_Shopify_Line_Item,Integrations_Shopify_Abandoned_Checkouts, Integrations_Shopify_Shipping_Line,\
                              Integrations_Shopify_Product, Integrations_Shopify_Shop

from django.db import transaction
from pyactiveresource.connection import ClientError
from shopify.resources.transaction import Transaction
import time


class OrderHandler(shopifyHandler.ShopifyHandler):

    def __init__(self, data, integration_id, user_iden,shop_id):

        self.addresses=[]
        self.cart_tkns_to_check=[]
        self.customers={}
        self.orders=[]
        self.order_id_of_discount_apps_to_del=set()
        self.discount_apps_to_save=[]
        self.order_id_of_discount_codes_to_del=set()
        self.discount_codes_to_save=[]
        self.fulfillments={}
        self.line_items={}
        self.shipping_lines={}
        super(OrderHandler, self).__init__(data, integration_id, user_iden,shop_id,"order")

    def _Handler__save_independent_objects(self):

        cHandler = customerHandler.CustomerHandler(self.customers.values(), self.integration_id, self.user_iden, self.shop_id)
        cHandler.save_all_objects()
        with transaction.atomic():
            self.remove_converted_checkouts()
            self.save_orders()


    def _Handler__save_dependent_objects(self):

        def save_dep_1():
            with transaction.atomic():
                self.save_discount_applications()
                self.save_discount_codes()
                self.save_fulfillments()
                self.save_shipping_lines()
                self.save_line_items()

        save_dep_1()


    def _Handler__parse_data(self):

        for obj in self.data:
            shopify_order = Integrations_Shopify_Order(
                order_id=obj.id,
                integration_id=self.integration_id,
                user_iden=self.user_iden,
                browser_ip=getattr(obj, "browser_ip", None),
                buyer_accepts_marketing=getattr(obj, "buyer_accepts_marketing", None),
                shipping_address_1 = getattr(getattr(obj, "shipping_address", None), "address_1", None),
                shipping_address_2 = getattr(getattr(obj, "shipping_address", None), "address_2", None),
                shipping_address_city = getattr(getattr(obj, "shipping_address", None), "city", None),
                shipping_address_company = getattr(getattr(obj, "shipping_address", None), "company", None),
                shipping_address_first_name = getattr(getattr(obj, "shipping_address", None),"first_name", None),
                shipping_address_last_name = getattr(getattr(obj, "shipping_address", None), "last_name", None),
                shipping_address_phone = getattr(getattr(obj, "shipping_address", None), "phone", None),
                shipping_address_province = getattr(getattr(obj, "shipping_address", None), "province", None),
                shipping_address_zip = getattr(getattr(obj, "shipping_address", None), "zip", None),
                shipping_address_name = getattr(getattr(obj, "shipping_address", None), "name", None),
                shipping_address_province_code = getattr(getattr(obj, "shipping_address", None), "province_code", None),
                shipping_address_country_code = getattr(getattr(obj, "shipping_address", None), "country_code", None),
                shipping_address_latitude = getattr(getattr(obj, "shipping_address", None), "latitude", None),
                shipping_address_longitude = getattr(getattr(obj, "shipping_address", None), "longitude", None),
                billing_address_1 = getattr(getattr(obj, "billing_address", None), "address_1", None),
                billing_address_2 = getattr(getattr(obj, "billing_address", None), "address_2", None),
                billing_address_city = getattr(getattr(obj, "billing_address", None), "city", None),
                billing_address_company = getattr(getattr(obj, "billing_address", None), "company", None),
                billing_address_first_name = getattr(getattr(obj, "billing_address", None),"first_name", None),
                billing_address_last_name = getattr(getattr(obj, "billing_address", None), "last_name", None),
                billing_address_phone = getattr(getattr(obj, "billing_address", None), "phone", None),
                billing_address_province = getattr(getattr(obj, "billing_address", None), "province", None),
                billing_address_zip = getattr(getattr(obj, "billing_address", None), "zip", None),
                billing_address_name = getattr(getattr(obj, "billing_address", None), "name", None),
                billing_address_province_code = getattr(getattr(obj, "billing_address", None), "province_code", None),
                billing_address_country_code = getattr(getattr(obj, "billing_address", None), "country_code", None),
                billing_address_latitude = getattr(getattr(obj, "billing_address", None), "latitude", None),
                billing_address_longitude = getattr(getattr(obj, "billing_address", None), "longitude", None),
                cancel_reason= getattr(obj, "cancel_reason", None),
                cancelled_at=getattr(obj, "cancelled_at", None),
                closed_at=getattr(obj, "closed_at", None),
                created_at=getattr(obj, "created_at", None),
                currency=getattr(obj, "currency", None),
                customer_locale=getattr(obj, "customer_locale", None),
                gateway=getattr(obj, "gateway", None),
                landing_site=getattr(obj, "landing_site", None),
                location_id=getattr(obj, "location_id", None),
                name=getattr(obj, "name", None),
                order_number=getattr(obj, "order_number", None),
                phone=getattr(obj, "phone", None),
                presentment_currency=getattr(obj, "presentment_currency", None),
                processed_at=getattr(obj, "processed_at", None),
                processing_method=getattr(obj, "processing_method", None),
                referring_site=getattr(obj, "referring_site", None),
                source_name=getattr(obj, "source_name", None),
                subtotal_price=getattr(obj, "subtotal_price", None),
                tags=getattr(obj, "tags", None),
                total_price=getattr(obj, "total_price", None),
                total_tax=getattr(obj, "total_tax", None),
                total_discounts=getattr(obj, "total_discounts", None),
                total_line_items_price=getattr(obj, "total_line_items_price", None),
                total_weight=getattr(obj, "total_weight", None),
                total_tip_received=getattr(obj, "total_tip_received", None),
                updated_at=getattr(obj, "updated_at", None)
            )      

            shopify_order.cart_token = self.grab_token(obj)


            self.grab_customer(obj)


            self.orders.append(shopify_order)

            for disc_app in getattr(obj, "discount_applications", []):
                self.grab_discount_application(shopify_order, disc_app)

            for disc_code in getattr(obj, "discount_codes", []):
                self.grab_discount_code(shopify_order, disc_code)

            for line_item in getattr(obj, "line_items", []):
                self.grab_line_item(shopify_order, line_item)

            for fulfillment in getattr(obj, "fulfillments", []):
                self.grab_fulfillment(shopify_order, fulfillment)

            for shipping_line in getattr(obj, "shipping_lines", []):
                self.grab_shipping_line(shopify_order, shipping_line)



    def remove_converted_checkouts(self):
        for tkn in self.cart_tkns_to_check:
            existing = Integrations_Shopify_Abandoned_Checkouts.objects.filter(cart_token=tkn)
            existing.delete()

    def save_orders(self):
        shop = Integrations_Shopify_Shop.objects.get(shop_id=self.shop_id)
        for order in self.orders:
            order.shop = shop
            c_id = getattr(self.customers.get(order.order_id,None),"id",None)
            customers = []
            if c_id:
                customers = Integrations_Shopify_Customer.objects.filter(customer_id=c_id)
            if len(customers) > 0:
                customer = customers[0]
                order.customer_ref = customer
                # billing_address = self.get_instances_if_exists(Integrations_Shopify_Address, order.billing_address)
                # order.billing_address = None if not billing_address else billing_address[0]
                # shipping_address = self.get_instances_if_exists(Integrations_Shopify_Address, order.shipping_address)
                # order.shipping_address = None if not shipping_address else shipping_address[0]
                self.update_or_save_instance(Integrations_Shopify_Order, order, "order_id")
            else:
                self.update_or_save_instance(Integrations_Shopify_Order, order, "order_id")
                OrderHandler.logger.error(f"Customer for order {order.order_id}  not synced!")


    def save_discount_applications(self):
        for order_id in self.order_id_of_discount_apps_to_del:
            existing=Integrations_Shopify_Discount_Application.objects.filter(order_id=order_id)
            existing.delete()

        for disc_app in self.discount_apps_to_save:
            self.update_or_save_instance(Integrations_Shopify_Discount_Application, disc_app, unique_attr=None)


    def save_discount_codes(self):
        for order_id in self.order_id_of_discount_codes_to_del:
            existing=Integrations_Shopify_Discount_Code.objects.filter(order_id=order_id)
            existing.delete()

        for disc_code in self.discount_codes_to_save:
            self.update_or_save_instance(Integrations_Shopify_Discount_Code, disc_code, unique_attr=None)

    def save_fulfillments(self):
        for oid, fulfillments in self.fulfillments.items():
            orders=Integrations_Shopify_Order.objects.filter(order_id=oid)
            if len(orders) > 0:
                order=orders[0]
                for fulfillment in fulfillments:
                    fulfillment.order = order
                    self.update_or_save_instance(Integrations_Shopify_Fulfillment, fulfillment, "fulfillment_id")

    def save_shipping_lines(self):
        for oid, lines in self.shipping_lines.items():
            orders=Integrations_Shopify_Order.objects.filter(order_id=oid)
            if len(orders) > 0:
                order=orders[0]
                for line in lines:
                    line.order=order
                    self.update_or_save_instance(Integrations_Shopify_Shipping_Line, line)

    def save_line_items(self):
        for oid, items in self.line_items.items():
            orders=Integrations_Shopify_Order.objects.filter(order_id=oid)
            if len(orders) > 0:
                order=orders[0]
                for item in items:
                    item.order=order

                    products = self.get_instances_if_exists(
                        Integrations_Shopify_Product,
                        Integrations_Shopify_Product(product_id=item.product_id),
                        "product_id"
                    )
                    if products:
                        item.product_ref=products[0]

                    self.update_or_save_instance(Integrations_Shopify_Line_Item, item, "line_item_id")



    def grab_token(self, obj):
        tkn = getattr(obj, "cart_token", None)
        if tkn:
            self.cart_tkns_to_check.append(tkn)
        return tkn

    def grab_customer(self, order):
        cust = getattr(order, "customer", None)
        o_id = getattr(order, "id", None)
        c_id=getattr(cust, "id", None)
        if not c_id:
            return None

        ## NOTE: API reponse data comes MOST RECENT first, so if we recive repeat customer data within a reponse,
        ## we only care about saving the first one (i.e. the most recent one) along with it's related addresses

        # each order should only have one customer, so we can use it as a unique key in out dictionary
        if o_id not in self.customers:
            self.customers[o_id]=cust

        return self.customers[o_id]


    def grab_discount_application(self, order, disc_app):
        order_id = getattr(order, "id", None)
        if order_id:
            discount_application = Integrations_Shopify_Discount_Application(
                order=order,
                allocation_method=getattr(disc_app, "allocation_method", None),
                code=getattr(disc_app, "code", None),
                description=getattr(disc_app, "description", None),
                target_selection=getattr(disc_app, "target_selection", None),
                target_type=getattr(disc_app, "target_type", None),
                title=getattr(disc_app, "title", None),
                type=getattr(disc_app, "type", None),
                value=getattr(disc_app, "value", None),
                value_type=getattr(disc_app, "value_type", None)
                )
            self.order_id_of_discount_apps_to_del.add(getattr(order, "id", None))
            self.discount_apps_to_save.append(discount_application)


    def grab_discount_code(self, order, disc_code):
        order_id =getattr(order, "id", None)
        if order_id:
            discount_code = Integrations_Shopify_Discount_Code(
                order=order,
                code = getattr(disc_code, "code", None),
                amount=getattr(disc_code, "amount", None),
                type=getattr(disc_code, "type", None)
                )
            self.order_id_of_discount_codes_to_del.add(getattr(order, "id",None))
            self.discount_codes_to_save.append(discount_code)


    def grab_line_item(self, order, line_item, fulfillment=None):
        order_id = getattr(order, "order_id", None)
        if order_id:
            line_item = Integrations_Shopify_Line_Item(
                order=order,
                line_item_id=getattr(line_item, "id", None),
                fulfillment=fulfillment,
                fulfillable_quantity=getattr(line_item, "fulfillment_quantity", None),
                fulfillment_service=getattr(line_item, "fulfillment_service", None),
                fulfillment_status=getattr(line_item, "fulfillment_status", None),
                grams=getattr(line_item, "grams", None),
                price=getattr(line_item, "price", None),
                product_id=getattr(line_item, "product_id", None),
                quantity=getattr(line_item, "quantity", None),
                requires_shipping=getattr(line_item, "requires_shipping", None),
                sku=getattr(line_item, "sku", None),
                title=getattr(line_item, "title", None),
                variant_id=getattr(line_item, "variant_id", None),
                variant_title=getattr(line_item, "variant_title", None),
                vendor=getattr(line_item, "vendor", None),
                name=getattr(line_item, "name", None),
                gift_card=getattr(line_item, "gift_card", None),
                taxable=getattr(line_item, "taxable", None),
                )
            if order_id in self.line_items:
                self.line_items[order_id].append(line_item)
            else:
                self.line_items[order_id]=[line_item]

    def grab_shipping_line(self, order, shipping_line):
        order_id=getattr(order,"order_id",None)
        if order_id:
            line = Integrations_Shopify_Shipping_Line(
                order = order,
                code = getattr(shipping_line,"code",None),
                price = getattr(shipping_line,"price",None),
                discounted_price = getattr(shipping_line,"discounted_price",None),
                source=getattr(shipping_line,"source",None),
                title=getattr(shipping_line,"title",None)
                )
            if order_id in self.shipping_lines:
                self.shipping_lines[order_id].append(line)
            else:
                self.shipping_lines[order_id] = [line]

    def grab_fulfillment(self, order, fulfillment):
        receipt=getattr(fulfillment, "receipt", {})
        order_id=getattr(order, "order_id", None)
        if order_id is not None:
            fulfillment = Integrations_Shopify_Fulfillment(
                order=order,
                fulfillment_id=getattr(fulfillment, "id", None),
                created_at=getattr(fulfillment, "created_at", None),
                location_id=getattr(fulfillment, "location_id", None),
                name=getattr(fulfillment, "name", None),
                status=getattr(fulfillment, "status", None),
                shipment_status=getattr(fulfillment, "shipment_status", None),
                service=getattr(fulfillment, "service", None),
                tracking_company=getattr(fulfillment, "tracking_company", None),
                tracking_number=getattr(fulfillment, "tracking_number", None),
                updated_at=getattr(fulfillment, "updated_at", None),
                receipt_testcase=getattr(receipt, "testcase", False),
                receipt_authorization=getattr(receipt, "authorization", None)
                )
            if order_id in self.fulfillments:
                self.fulfillments[order_id].append(fulfillment)
            else:
                self.fulfillments[order_id] = [fulfillment]
            for line_item in getattr(fulfillment, "line_items", []):
                self.grab_line_item(order, line_item, fulfillment=fulfillment)
            
