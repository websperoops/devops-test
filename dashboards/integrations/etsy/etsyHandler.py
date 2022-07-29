from . import etsyAPI
from dashboards.integrations.utils import Handler
from dashboards.models import Integrations_Etsy_User, Integrations_Etsy_UserAddress, Integrations_Etsy_Shop, Integrations_Etsy_Shop_Language
import logging


class EtsyHandler(Handler):

    logger = logging.getLogger(__name__)

    def __init__(self, data, pk, user_iden, integration_name, name):
        super(EtsyHandler, self).__init__(data, pk, user_iden, integration_name, name)
    
    @staticmethod
    def save_user(row, avatar, integration_id, now_time, user_iden):
        user, created = Integrations_Etsy_User.objects.get_or_create(integration_id=integration_id, user_iden=user_iden)
        user.avatar_id = row.get("avatar_id", None)
        user.avatar_src_url = avatar.get("src", None)
        user.user_profile_id = row.get("user_profile_id", None)
        user.login_name = row.get("login_name", None)
        user.bio = row.get("bio", None)
        user.gender = row.get("gender", None)
        user.birth_month = row.get("birth_month", None)
        user.birth_day = row.get("birth_day", None)
        user.birth_year = row.get("birth_year", None)
        user.join_tsz = etsyAPI.unix2UTC(row.get("join_tsz", None))
        user.materials = row.get("materials", None)
        user.country_id = row.get("country_id", None)
        user.region = row.get("region", None)
        user.city = row.get("city", None)
        user.location = row.get("location", None)
        user.lat = row.get("lat", None)
        user.lon = row.get("lon", None) 
        user.transaction_buy_count = row.get("transaction_buy_count", None)                 
        user.transaction_sold_count = row.get("transaction_sold_count", None)
        user.is_seller = row.get("is_seller", None)
        user.image_url_75x75 = row.get("image_url_75x75", None)
        user.first_name = row.get("first_name", None)
        user.last_name = row.get('last_name', None)
        user.user_iden = user_iden
        user.last_sync_time = now_time
        user.save()
        return user

    @staticmethod
    def save_user_addresses(rows, integration_id, now_time, user_iden, key):
        for u_address in rows:
            addr, created = Integrations_Etsy_UserAddress.objects.get_or_create(user_address_id=u_address.get("user_address_id"),integration_id=integration_id, user_iden=user_iden)
            addr.user_ref = key
            addr.last_sync_time = now_time
            addr.user_id = u_address.get("user_id", None)
            addr.address_name = u_address.get("name", None)
            addr.first_line = u_address.get("first_line", None) 
            addr.second_line = u_address.get("second_line", None)
            addr.city = u_address.get("city", None)
            addr.state = u_address.get("state", None)
            addr.zip = u_address.get("zip", None)
            addr.country_id = u_address.get("country_id", None)
            addr.country_name = u_address.get("country_name", None)
            addr.is_default_shipping = u_address.get("is_default_shipping", False)
            addr.save()
        return addr

    @staticmethod
    def save_shops(rows, integration_id, now_time, user_iden, key):
        shop_ids = []
        for row in rows:
            shop, created = Integrations_Etsy_Shop.objects.get_or_create(shop_id=row.get("shop_id"),integration_id=integration_id, user_iden=user_iden)    
            shop.user_ref = key
            shop.user_id = row.get("user_id", None)
            shop.last_sync_time = now_time
            shop.shop_name = row.get("shop_name", None)
            shop.first_line = row.get("first_line", None)
            shop.second_line = row.get("second_line", None)
            shop.city = row.get("city", None)
            shop.state = row.get("state", None)
            shop.zip = row.get("zip", None)
            shop.country_id = row.get("country_id", None)
            shop.creation_tsz = etsyAPI.unix2UTC(row.get("creation_tsz", None))
            shop.title =  row.get("title", None)
            shop.announcement = row.get("announcement", None)
            shop.currency_code = row.get("currency_code", None)
            shop.is_vacation = row.get("is_vacation", None)
            shop.vacation_message =row.get("vacation_message", None)
            shop.sale_message = row.get("sale_message", None)
            shop.digital_sale_message = row.get("digital_sale_message", None)
            shop.last_updated_tsz = etsyAPI.unix2UTC(row.get("last_updated_tsz", None))
            shop.listing_active_count = row.get("listing_active_count", None)
            shop.digital_listing_count = row.get("digital_listing_count", None)
            shop.login_name = row.get("login_name", None)
            shop.lat = row.get("lat", None)
            shop.lon = row.get("lon", None)
            shop.accepts_custom_requests = row.get("accepts_custom_requests", None)
            shop.policy_welcome = row.get("policy_welcome", None)
            shop.policy_payment = row.get("policy_payment", None)
            shop.policy_shipping = row.get("policy_shipping", None)
            shop.policy_refunds = row.get("policy_refunds", None)
            shop.policy_additional = row.get("policy_additional", None)
            shop.policy_seller_info = row.get("policy_seller_info", None)
            shop.policy_updated_tsz = etsyAPI.unix2UTC(row.get("policy_updated_tsz", None))
            shop.policy_has_private_receipt_info = row.get("policy_has_private_receipt_info", None)
            shop.vacation_autoreply = row.get("vacation_autoreply", None)
            shop.ga_code = row.get("ga_code", None)
            shop.name = row.get("name", None)
            shop.url = row.get("url", None)
            shop.image_url_760x100 = row.get("image_url_760x100", None)
            shop.num_favorers = row.get("num_favorers", None)
            shop.upcoming_local_event_id = row.get("upcoming_local_event_id", None)
            shop.icon_url_fullxfull = row.get("icon_url_fullxfull", None)
            shop.is_using_structured_policies = row.get("is_using_structured_policies", None)
            shop.has_onboarded_structured_policies = row.get("has_onboarded_structured_policies", None)
            shop.has_unstructured_policies = row.get("has_unstructured_policies", None)
            shop.policy_privacy = row.get("policy_privacy", None)
            shop.use_new_inventory_endpoints = row.get("use_new_inventory_endpoints", None)
            shop.include_dispute_form_link = row.get("include_dispute_form_link", None)
            shop.save()
            shop_ids.append(shop.shop_id)
        
            for lang in row.get("languages", None):
                language, created = Integrations_Etsy_Shop_Language.objects.get_or_create(language = lang, shop_ref = shop)
                language.save()

        return shop_ids

    def __save_independent_objects(self):
        return

    def __save_dependent_objects(self):
        return

    def __parse_data(self):
        return
