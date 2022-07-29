from .mock_util import create_mock_from_json, get_decimal

from allauth.socialaccount.models import SocialAccount

from dashboards.models import Integrations_UserSettings, Integrations_User_LastSync, Integrations_Shopify_Order, \
    Integrations_Shopify_Customer, Integrations_Shopify_Discount_Application, Integrations_Shopify_Discount_Code, \
    Integrations_Shopify_Fulfillment, Integrations_Shopify_Line_Item, Integrations_Shopify_Address, \
    Integrations_Shopify_Product, Integrations_Shopify_Product_Variant, Integrations_Shopify_Product_Option, \
    Integrations_Shopify_Product_Tag, Integrations_Shopify_Product_Option_Value, Integrations_Shopify_Customer_Address, \
    Integrations_Shopify_Shop, Integrations_Shopify_Refund, Integrations_Shopify_Refund_Line_Item

from dashboards.sync import checkLastSync, SaveOrder, SaveCustomer, SaveProduct
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase, tag, TransactionTestCase
from django.utils import timezone
from django.utils.dateparse import parse_datetime

import os
from unittest import skip


resource_path = os.path.join(os.path.dirname(__file__), "resources")


class CheckLastSyncTestCase(TestCase):

    # create a user and a user profile
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="test12345")
        self.socialaccount = SocialAccount.objects.create(user=self.user, provider='openid', uid='123')

    def tearDown(self):
        self.user.delete()
        self.socialaccount.delete()
        Integrations_User_LastSync.objects.all().delete()
        Integrations_UserSettings.objects.all().delete()

    @tag("sync")
    def testKeyValues(self):
        # Create user profile settings first
        Integrations_UserSettings.objects.create(integration=self.socialaccount, user=self.user)
        Integrations_User_LastSync.objects.create(user=self.user, integration=self.socialaccount)

        output = checkLastSync(self.user.id, self.socialaccount.provider, None)

        # check the keys in the output
        self.assertTrue('should_sync' in output, 'checkLastSync did not return a dictionary with key \'should_sync\'')
        self.assertTrue('initialize' in output, 'checkLastSync did not return a dictionary with key \'initialize\'')
        self.assertTrue('sync_is_active' in output,
                        'checkLastSync did not return a dictionary with key \'sync_is_active\'')
        self.assertTrue('last_sync_time' in output,
                        'checkLastSync did not return a dictionary with key \'last_sync_time\'')

    @tag("sync")
    def testNeverSyncedBefore(self):
        # Create user profile settings first
        Integrations_UserSettings.objects.create(integration=self.socialaccount, user=self.user)
        output = checkLastSync(self.user.id, self.socialaccount.provider, None)

        self.assertTrue(output["initialize"])
        self.assertTrue(output["should_sync"])
        self.assertFalse(output['sync_is_active'])
        self.assertEqual(output['last_sync_time'], 'Never')

    @skip("Unknown reason why checkpoint exists or its use")
    def testHasSyncedBefore(self):
        Integrations_UserSettings.objects.create(integration=self.socialaccount, user=self.user)
        Integrations_User_LastSync.objects.create(user=self.user, integration=self.socialaccount)

        output = checkLastSync(self.user.id, self.socialaccount.provider, None)
        print(output)
        self.assertFalse(output["initialize"])
        self.assertFalse(output["should_sync"])


class SaveShopifyOrderTestCase(TransactionTestCase):
    # create a user and a user profile
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="test12345")
        self.socialaccount = SocialAccount.objects.create(user=self.user, provider='shopify', uid='123')

    def check_address(self, address, addr_obj):
        self.assertEqual(address.address1, addr_obj.address1)
        self.assertEqual(address.address2, addr_obj.address2)
        self.assertEqual(address.city, addr_obj.city)
        if addr_obj.company is not None:
            self.assertEqual(address.company, addr_obj.company)
        else:
            self.assertEqual(address.company, "")
        self.assertEqual(address.country, addr_obj.country)
        self.assertEqual(address.country_code, addr_obj.country_code)
        self.assertEqual(address.first_name, addr_obj.first_name)
        self.assertEqual(address.last_name, addr_obj.last_name)
        self.assertEqual(address.latitude, get_decimal(addr_obj.latitude, 4))
        self.assertEqual(address.longitude, get_decimal(addr_obj.longitude, 4))
        self.assertEqual(address.name, addr_obj.name)
        self.assertEqual(address.phone, addr_obj.phone)
        self.assertEqual(address.province, addr_obj.province)
        self.assertEqual(address.province, addr_obj.province)

    def check_money_set(self, money_set, row):
        if money_set is None:
            return
        money_set.shop_money_amount = get_decimal(float(row.shop_money.amount), 2)
        money_set.shop_money_currency_code = row.shop_money.currency_code
        money_set.presentment_money_amount = get_decimal(float(row.presentment_money.amount), 2)
        money_set.presentment_money_currency_code = row.presentment_money.currency_code

    def check_refund_line_item(self, refund, row):
        item = Integrations_Shopify_Refund_Line_Item.objects.get(refund_line_item_id=row.id)
        self.assertIsNotNone(item.line_item_ref)

    def check_refund(self, order, row):
        refund = Integrations_Shopify_Refund.objects.get(refund_id=row.id)
        self.assertEqual(refund.created_at, parse_datetime(row.created_at))
        for item in row.refund_line_items:
            self.check_refund_line_item(refund, item)

    @tag("Sync", "Shopify")
    def testSaveOrder1(self):
        new_order = create_mock_from_json("dashboards/tests/resources/shopify/order2.json").order
        new_order.customer.addresses = []
        pk = self.socialaccount.id
        now_time = timezone.now()
        user_id = self.user.id
        SaveOrder(row=new_order, integration_id=pk, now_time=now_time, user_iden=user_id)

        self.assertEqual(Integrations_Shopify_Order.objects.count(), 1)
        order = Integrations_Shopify_Order.objects.first()
        self.assertEqual(Integrations_Shopify_Address.objects.count(), 2)
        self.check_address(order.billing_address, new_order.billing_address)
        self.check_address(order.shipping_address, new_order.shipping_address)
        self.assertEqual(order.browser_ip, new_order.browser_ip)
        self.assertEqual(order.cancel_reason, new_order.cancel_reason)
        self.assertEqual(order.cancelled_at, parse_datetime(new_order.cancelled_at))
        self.assertEqual(order.cart_token, new_order.cart_token)
        self.assertEqual(order.closed_at, parse_datetime(new_order.closed_at))
        self.assertEqual(order.created_at, parse_datetime(new_order.created_at))
        self.assertEqual(order.currency, new_order.currency)

        self.assertEqual(Integrations_Shopify_Customer.objects.count(), 1)
        self.assertEqual(Integrations_Shopify_Customer.objects.first().customer_id, str(new_order.customer.id))

        self.assertEqual(order.customer_locale, new_order.customer_locale)
        self.assertEqual(order.email, new_order.email)
        self.assertEqual(order.financial_status, new_order.financial_status)

        self.assertEqual(Integrations_Shopify_Discount_Application.objects.count(), 1)
        self.assertEqual(Integrations_Shopify_Discount_Code.objects.count(), 1)
        self.assertEqual(Integrations_Shopify_Line_Item.objects.count(), 3)

        self.assertEqual(order.fulfillment_status, new_order.fulfillment_status)
        self.assertEqual(order.landing_site, new_order.landing_site)
        self.assertEqual(order.location_id, new_order.location_id)
        self.assertEqual(order.name, new_order.name)
        self.assertEqual(order.order_number, new_order.order_number)
        self.assertEqual(order.phone, new_order.phone)
        self.assertEqual(order.presentment_currency, new_order.presentment_currency)
        self.assertEqual(order.processed_at, parse_datetime(new_order.processed_at))
        self.assertEqual(order.processing_method, new_order.processing_method)
        self.assertEqual(order.referring_site, new_order.referring_site)
        self.assertEqual(order.source_name, new_order.source_name)
        self.assertEqual(order.subtotal_price, get_decimal(float(new_order.subtotal_price), 2))
        self.check_money_set(order.subtotal_price_set, new_order.subtotal_price_set)
        self.assertEqual(order.tags, new_order.tags)

        self.assertEqual(order.total_price, get_decimal(float(new_order.total_price), 2))
        self.check_money_set(order.total_price_set, new_order.total_price_set)

        self.assertEqual(order.total_tax, get_decimal(float(new_order.total_tax), 2))
        self.check_money_set(order.total_tax_set, new_order.total_tax_set)

        self.assertEqual(order.total_discounts, get_decimal(float(new_order.total_discounts), 2))
        self.check_money_set(order.total_discounts_set, new_order.total_discounts_set)

        self.assertEqual(order.total_line_items_price, get_decimal(float(new_order.total_line_items_price), 2))
        self.check_money_set(order.total_line_items_set, new_order.total_line_items_price_set)

        self.assertEqual(order.total_weight, get_decimal(float(new_order.total_weight), 2))
        self.assertEqual(order.total_tip_received, get_decimal(float(new_order.total_tip_received), 2))
        self.assertEqual(order.updated_at, parse_datetime(new_order.updated_at))

        self.assertEqual(Integrations_Shopify_Refund.objects.count(), 1)
        for refund in new_order.refunds:
            self.check_refund(order, refund)
        self.assertEqual(Integrations_Shopify_Refund_Line_Item.objects.count(), 2)

    @tag("Sync", "Shopify")
    def testDeleteOrder1(self):
        new_order = create_mock_from_json("dashboards/tests/resources/shopify/order2.json").order
        new_order.customer.addresses = []
        pk = self.socialaccount.id
        now_time = timezone.now()
        user_id = self.user.id
        SaveOrder(row=new_order, integration_id=pk, now_time=now_time, user_iden=user_id)

        order = Integrations_Shopify_Order.objects.first()
        order.delete()

        self.assertEqual(Integrations_Shopify_Order.objects.count(), 0)
        self.assertEqual(Integrations_Shopify_Line_Item.objects.count(), 0)
        self.assertEqual(Integrations_Shopify_Fulfillment.objects.count(), 0)
        self.assertEqual(Integrations_Shopify_Discount_Code.objects.count(), 0)
        self.assertEqual(Integrations_Shopify_Discount_Application.objects.count(), 0)


@tag("Shopify", "Sync")
class SaveShopifyCustomerTestCase(TransactionTestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="test12345")
        self.socialaccount = SocialAccount.objects.create(user=self.user, provider='shopify', uid='123')
        self.shop = Integrations_Shopify_Shop.objects.create(shop_id="12334", integration=self.socialaccount,
                                                             iana_timezone="America/Chicago")

    def testSaveCustomer1(self):
        new_order = create_mock_from_json("dashboards/tests/resources/shopify/customer.json").customer
        now_time = timezone.now()
        SaveCustomer(new_order, self.socialaccount.id, now_time, self.user.id)

        self.assertEqual(Integrations_Shopify_Customer.objects.count(), 1)
        customer = Integrations_Shopify_Customer.objects.first()

        self.assertEqual(customer.customer_id, '207119551')
        self.assertEqual(customer.email, "bob.norman@hostmail.com")
        self.assertEqual(customer.user_iden, str(self.user.id))
        self.assertEqual(customer.integration, self.socialaccount)
        self.assertEqual(customer.last_sync_time, now_time)
        self.assertEqual(customer.accepts_marketing, False)
        self.assertEqual(customer.currency, "USD")
        # self.assertEqual(customer.created_at, ) #TODO have to implement shop timezone
        self.assertEqual(customer.default_address, '207119551')
        self.assertEqual(customer.first_name, "Bob")
        self.assertEqual(customer.last_name, "Norman")
        self.assertEqual(customer.last_order_id, '450789469')
        self.assertEqual(customer.last_order_name, "#1001")
        self.assertEqual(customer.orders_count, 2)
        self.assertEqual(customer.phone, "555-625-1199")
        self.assertEqual(customer.state, "disabled")
        self.assertEqual(customer.tags, "tags")
        self.assertEqual(customer.tax_exempt, False)
        self.assertEqual(customer.total_spent, Decimal("199.65"))
        # self.assertEqual(customer.updated_at, ) #TODO have to implement shop timezone

        self.assertEqual(Integrations_Shopify_Customer_Address.objects.count(), 1)
        self.assertEqual(Integrations_Shopify_Address.objects.count(), 1)
        customer_address = Integrations_Shopify_Customer_Address.objects.first()
        self.assertEqual(customer_address.default, True)
        self.assertEqual(customer_address.customer, customer)
        self.assertEqual(customer_address.customer_address_id, '207119551')

        address = customer_address.address

        self.assertEqual(address.address1, "Chestnut Street 92")
        self.assertEqual(address.address2, "")
        self.assertEqual(address.city, "Louisville")
        self.assertEqual(address.country, "United States")
        self.assertEqual(address.country_code, "US")
        self.assertEqual(address.company, "Blocklight")
        self.assertEqual(address.province, "Kentucky")
        self.assertEqual(address.zip, "40202")
        self.assertEqual(address.phone, "555-625-1199")


@tag("Shopify", "Sync")
class SaveShopifyProductTestCase(TransactionTestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="test12345")
        self.socialaccount = SocialAccount.objects.create(user=self.user, provider='shopify', uid='123')

    def check_product_option(self, product, expected):
        actual = Integrations_Shopify_Product_Option.objects.get(option_id=expected.id, product=product)
        self.assertEqual(actual.option_id, expected.id)
        self.assertEqual(actual.product.id, expected.product_id)
        self.assertEqual(actual.name, expected.name)
        self.assertEqual(actual.position, expected.position)
        self.assertEqual(Integrations_Shopify_Product_Option_Value.objects.count(), len(expected.values))

    def check_product_variant(self, product, expected):
        actual = Integrations_Shopify_Product_Variant.objects.get(product=product, variant_id=expected.id)
        self.assertEqual(actual.barcode, expected.barcode)
        self.assertEqual(actual.compare_at_price, get_decimal(expected.compare_at_price, 2))
        self.assertEqual(actual.created_at, parse_datetime(expected.created_at))
        self.assertEqual(actual.fulfillment_service, expected.fulfillment_service)
        self.assertEqual(actual.grams, expected.grams)
        self.assertEqual(actual.inventory_item_id, str(expected.inventory_item_id))
        self.assertEqual(actual.inventory_management, expected.inventory_management)
        self.assertEqual(actual.inventory_policy, expected.inventory_policy)
        self.assertEqual(actual.inventory_quantity, expected.inventory_quantity)
        self.assertEqual(actual.option1, expected.option1)
        self.assertEqual(actual.option2, expected.option2)
        self.assertEqual(actual.option3, expected.option3)
        self.assertEqual(actual.position, expected.position)
        self.assertEqual(actual.price, get_decimal(expected.price, 2))
        self.assertEqual(actual.sku, expected.sku)
        self.assertEqual(actual.taxable, expected.taxable)
        self.assertEqual(actual.tax_code, expected.tax_code)
        self.assertEqual(actual.title, expected.title)
        self.assertEqual(actual.updated_at, parse_datetime(expected.updated_at))
        self.assertEqual(actual.weight, get_decimal(expected.weight, 2))
        self.assertEqual(actual.weight_unit, expected.weight_unit)

    def testSaveProduct1(self):
        new_product = create_mock_from_json("dashboards/tests/resources/shopify/product.json").product
        pk = self.socialaccount.id
        now_time = timezone.now()
        user_id = self.user.id
        SaveProduct(row=new_product, integration_id=pk, now_time=now_time, user_iden=user_id)

        self.assertEqual(Integrations_Shopify_Product.objects.count(), 1)
        product = Integrations_Shopify_Product.objects.first()

        self.assertEqual(product.last_sync_time, now_time)
        self.assertEqual(product.created_at, parse_datetime(new_product.created_at))
        self.assertEqual(product.created_at, parse_datetime(new_product.created_at))
        self.assertEqual(product.product_id, str(new_product.id))
        self.assertEqual(product.product_type, new_product.product_type)
        self.assertEqual(product.published_at, parse_datetime(new_product.published_at))
        self.assertEqual(product.published_scope, new_product.published_scope)
        self.assertEqual(product.title, new_product.title)
        self.assertEqual(product.updated_at, parse_datetime(new_product.updated_at))
        self.assertEqual(product.vendor, new_product.vendor)

        self.assertEqual(Integrations_Shopify_Product_Tag.objects.count(), 4)
        for tag in new_product.tags.split(", "):
            self.assertEqual(Integrations_Shopify_Product_Tag.objects.filter(tag=tag).count(), 1)

        self.assertEqual(Integrations_Shopify_Product_Option.objects.count(), 1)
        self.assertEqual(Integrations_Shopify_Product_Variant.objects.count(), 4)

        for variant in new_product.variants:
            self.check_product_variant(product, variant)
