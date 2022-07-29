from . import shopifyHandler
from dashboards.models import Integrations_Shopify_Customer, Integrations_Shopify_Customer_Address, Integrations_Shopify_Address, Integrations_Shopify_Shop
from django.db import transaction


class CustomerHandler(shopifyHandler.ShopifyHandler):

    def __init__(self, data, integration_id, user_iden,shop_id):

        self.customers = []
        self.customer_addresses = []
        super(CustomerHandler, self).__init__(data, integration_id, user_iden,shop_id,"customer")


    def _Handler__save_independent_objects(self):
        with transaction.atomic():
            # self.save_addresses()
            self.save_customers()




    def _Handler__save_dependent_objects(self):
        with transaction.atomic():
            self.save_customer_addresses()

    def _Handler__parse_data(self):
        for obj in self.data:
            customer_id=getattr(obj, "id", getattr(obj, "customer_id", None))
            if not customer_id:
                CustomerHandler.logger.info(dir(obj))
                CustomerHandler.logger.warn("Customer Id not found")
            if customer_id:
                customer = Integrations_Shopify_Customer(
                    integration_id=self.integration_id,
                    customer_id=getattr(obj, "id", None),
                    user_iden=self.user_iden,
                    email=getattr(obj, "email", None),
                    accepts_marketing=getattr(obj, "accepts_marketing", None),
                    created_at=getattr(obj, "created_at", None),
                    updated_at=getattr(obj, "updated_at", None),
                    first_name=getattr(obj, "first_name", None),
                    last_name=getattr(obj, "last_name", None),
                    orders_count=getattr(obj, "orders_count",None),
                    state=getattr(obj, "state",None),
                    total_spent=getattr(obj, "total_spent",None),
                    last_order_id=getattr(obj, "last_order_id",None), tax_exempt=getattr(obj, "tax_exempt",None),
                    phone=getattr(obj, "phone",None),
                    tags=getattr(obj, "tags",None),
                    last_order_name=getattr(obj, "last_order_name",None),
                    currency=getattr(obj, "currency",None),
                    default_address_1 = getattr(getattr(obj, "default_address", None), "address_1", None),
                    default_address_2 = getattr(getattr(obj, "default_address", None), "address_2", None),
                    default_address_city = getattr(getattr(obj, "default_address", None), "city", None),
                    default_address_company = getattr(getattr(obj, "default_address", None), "company", None),
                    default_address_first_name = getattr(getattr(obj, "default_address", None),"first_name", None),
                    default_address_last_name = getattr(getattr(obj, "default_address", None), "last_name", None),
                    default_address_phone = getattr(getattr(obj, "default_address", None), "phone", None),
                    default_address_province = getattr(getattr(obj, "default_address", None), "province", None),
                    default_address_zip = getattr(getattr(obj, "default_address", None), "zip", None),
                    default_address_name = getattr(getattr(obj, "default_address", None), "name", None),
                    default_address_province_code = getattr(getattr(obj, "default_address", None), "province_code", None),
                    default_address_country_code = getattr(getattr(obj, "default_address", None), "country_code", None),
                    default_address_latitude = getattr(getattr(obj, "default_address", None), "latitude", None),
                    default_address_longitude = getattr(getattr(obj, "default_address", None), "longitude", None),
                    )
                self.customers.append(customer)
                # if customer.default_address:
                #     self.grab_address(getattr(obj, "default_address", None))
                #     self.grab_customer_address(customer.id, customer.default_address, True)
                #
                # for addr in getattr(obj, "addresses", []):
                #     address =self.grab_address(addr)
                #     if address:
                #         self.grab_customer_address(customer.id, address.address_id, False)


    def save_customers(self):
        shop = Integrations_Shopify_Shop.objects.get(shop_id=self.shop_id)
        for customer in self.customers:
            customer.shop = shop
            self.update_or_save_instance(Integrations_Shopify_Customer, customer, "customer_id")


    def save_customer_addresses(self):
        for cust_addr in self.customer_addresses:
            address = self.get_instances_if_exists(
                Integrations_Shopify_Address,
                Integrations_Shopify_Address(address_id=cust_addr["address_id"]),
                unique_attr="address_id")

            customer = self.get_instances_if_exists(
                Integrations_Shopify_Customer,
                Integrations_Shopify_Customer(customer_id=cust_addr["customer_id"]),
                unique_attr="id")

            default = cust_addr["isDefault"]

            if customer and address and getattr(address[0], "address_id", None):
                customer, address = customer[0], address[0]
                self.update_or_save_instance(
                    Integrations_Shopify_Customer_Address,
                    Integrations_Shopify_Customer_Address(
                        address=address,
                        customer=customer,
                        customer_address_id=address.address_id,
                        default=default
                    ),
                    unique_attr={
                        "customer_address_id":address.address_id,
                        "customer_id":customer.customer_id
                    }
                )


    def grab_customer_address(self, customer_id, address_id, isDefault):

        self.customer_addresses.append({
            "customer_id":customer_id,
            "address_id":address_id,
            "isDefault":isDefault
        })
