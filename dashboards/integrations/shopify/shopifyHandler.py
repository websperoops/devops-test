from dashboards.integrations.utils import Handler
from dashboards.models import Integrations_Shopify_Address, Integrations_Shopify_Shop

import logging


class ShopifyHandler(Handler):

    logger = logging.getLogger(__name__)

    def __init__(self, data, integration_id, user_iden, shop_id, name):

        '''
        This class is meant to be inherited to sync shopify objects/resources from the
        python shopify API wrapper library.


        Args:
            data (dict): API response data from the shopify wrapper library.
            integration_id (int): the id for the integraion
            user_iden (int): the user's id
            shop_id (int): the associated shops id
            name (str): hardcoded name specifying the core object/resource
        '''



        self.addresses=[]
        self.shop_id = shop_id
        super(ShopifyHandler, self).__init__(data, integration_id, user_iden, "shopify", name)
        Handler.log_behavior(f"successfully read in {self.name}, API response data into handler of length {self.batch_size}")



    @staticmethod
    def save_shop(row, integration_id, now_time, user_iden):
        shop, created = Integrations_Shopify_Shop.objects.get_or_create(integration_id=integration_id, shop_id=row.id)
        shop.address1 = getattr(row, "address1", None)
        shop.address2 = getattr(row, "address2", None)
        shop.city = getattr(row, "city", None)
        shop.country = getattr(row, "country", None)
        shop.country_code = getattr(row, "country_code", None)
        shop.country_name = getattr(row, "country_name", None)
        shop.created_at = getattr(row, "created_at", None)
        shop.customer_email = getattr(row, "customer_email", None)
        shop.currency = getattr(row, "currency", "USD")
        shop.domain = getattr(row, "domain", None)
        shop.eligible_for_payments = getattr(row, "eligible_for_payments", False)
        shop.email = getattr(row, "email", None)
        shop.force_ssl = getattr(row, "force_ssl", False)
        shop.has_discounts = getattr(row, "has_discounts", False)
        shop.has_gift_cards = getattr(row, "has_gift_cards", False)
        shop.has_storefront = getattr(row, "has_storefront", False)
        shop.iana_timezone = getattr(row, "iana_timezone", "UTC")
        shop.latitude = getattr(row, "latitude", None)
        shop.longitude = getattr(row, "longitude", None)
        shop.money_format = getattr(row, "money_format", None)
        shop.name = getattr(row, "name", None)
        shop.phone = getattr(row, "phone", None)
        shop.plan_display_name = getattr(row, "plan_display_name", None)
        shop.plan_name = getattr(row, "plan_name", None)
        shop.primary_locale = getattr(row, "primary_locale", None)
        shop.province = getattr(row, "province", None)
        shop.province_code = getattr(row, "province_code", None)
        shop.shop_owner = getattr(row, "shop_owner", None)
        shop.source = getattr(row, "source", None)
        shop.tax_shipping = getattr(row, "tax_shipping", True)
        shop.updated_at = getattr(row, "updated_at", None)
        shop.weight_unit = getattr(row, "weight_unit", None)
        shop.zip = getattr(row, "zip", None)
        shop.user_iden = user_iden
        shop.last_sync_time = now_time
        shop.save()

        return shop


    def __save_independent_objects(self):
        return


    def __save_dependent_objects(self):
        return

    def __parse_data(self):
        return

    def save_addresses(self):
        for addr in self.addresses:
            self.update_or_save_instance(Integrations_Shopify_Address, addr, unique_attr=None)

    def grab_address(self, obj, key=None):
        # If no key is passed in, the assumption the object itself is an address,
        # Otherwise, the obj is indexed by the key to obtain the address
        addr = None
        if key:
            address = getattr(obj, key, None)
        else:
            address = obj


        if address:
            addr = Integrations_Shopify_Address(
            address_id = getattr(address, "id", None),
            address1=getattr(address, "address1", None),
            address2=getattr(address, "address2", None),
            city=getattr(address, "city", None),
            company=getattr(address, "company", None),
            country=getattr(address, "country", None),
            country_code=getattr(address, "country_code", None),
            first_name=getattr(address, "first_name", None),
            last_name=getattr(address, "last_name", None),
            name=getattr(address, "name", None),
            phone=getattr(address, "phone", None),
            province=getattr(address, "province", None),
            zip=getattr(address, "zip", None)
            )
            self.addresses.append(addr)
        return addr
