from django.core.management.base import BaseCommand

from dashboards.models import (
    Integrations_Shopify_Order,
    Integrations_Shopify_Product,
    Integrations_Shopify_Customer,
    Integrations_Shopify_Abandoned_Checkouts,
    Integrations_Shopify_Shop_Price_Rule)

from shopify.resources.customer import Customer
from shopify.resources.order import Order
from shopify.resources.product import Product
from shopify.resources.checkout import Checkout
from shopify.resources.price_rule import PriceRule


from dashboards.integrations.shopify import integration
from django.contrib.auth.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user_id = options["user_id"][0]

        shopify_integration = integration.ShopifyIntegration()

        auth_params = shopify_integration.build_auth_params(
            'shopify', User.objects.get(id=user_id))

        for shopify_shop_auth in auth_params:
            shopify_integration.get_params(shopify_shop_auth)
            print(shopify_shop_auth["shopify_account"].extra_data)
            table_endpoint_pairs = [
                (Integrations_Shopify_Order, Order),
                (Integrations_Shopify_Customer, Customer),
                (Integrations_Shopify_Product, Product),
                (Integrations_Shopify_Abandoned_Checkouts, Checkout),
                (Integrations_Shopify_Shop_Price_Rule, PriceRule)
            ]
            for (model, api) in table_endpoint_pairs:
                self.validate(model, api, user_id)

    def add_arguments(self, parser):
        parser.add_argument("--uid", nargs=1, type=int,
                            help="user id of user", dest="user_id")

    def validate(self, model, api, user_id):

        db_count = model.objects.filter(user_iden=user_id).count()
        if api == Order:
            api_count = api.count(status='any')
        else:
            api_count = api.count()

        percent_data_ingested_from_api = 100 * (db_count / api_count)
        self.stdout.write(self.style.SUCCESS(f'{model}\nDBCOUNT:'
                                             f'{db_count}\nAPICOUNT:'
                                             f'{api_count}\n'
                                             f'Percent Data Ingested: {percent_data_ingested_from_api} % \n'))
