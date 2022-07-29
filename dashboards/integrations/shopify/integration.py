from ...integrations.integration import Integration
from . import sync, orderHandler, customerHandler, checkoutHandler, productHandler, ruleHandler, refundHandler, transactionHandler

from allauth.socialaccount.models import SocialAccount, SocialToken
from celery import shared_task


from dashboards.models import Integrations_Shopify_Order, Integrations_Shopify_Product, Integrations_Shopify_Customer, \
    Integrations_Shopify_Abandoned_Checkouts, Integrations_Shopify_Shop_Price_Rule, Integrations_Shopify_Refund, \
    Integrations_Shopify_Transaction


from django.contrib.auth.models import User as DjangoUser
import logging

from shopify.base import ShopifyResource
from shopify.resources.customer import Customer
from shopify.resources.order import Order
from shopify.resources.product import Product
from shopify.resources.checkout import Checkout
from shopify.resources.price_rule import PriceRule
from shopify.resources.refund import Refund
from shopify.resources.transaction import Transaction
from shopify.session import Session
from ...enums.CoreEnums import Master_Blocklight_User



logger = logging.getLogger(__name__)


class ShopifyIntegration(Integration):
    API_VERSION = '2022-01'

    def get_task(self, user):
        task = initialize_shopify_syncworker_task
        tcount = SocialAccount.objects.filter(
            provider='shopify', user_id=user.id).count()
        return task, tcount

    def get_params(self, auth_params):
        # of type SocialAccount
        shopify_account = auth_params['shopify_account']
        extra_data = shopify_account.extra_data
        shopname = extra_data['shop']['myshopify_domain']
        newest_token = shopify_account.socialtoken_set.order_by(
            '-id').first()  # of type SocialToken
        session = Session(
            shopname, ShopifyIntegration.API_VERSION, newest_token.token)
        ShopifyResource.activate_session(session)

        refunds = {
            'parent_model': Integrations_Shopify_Order,
            'model': Integrations_Shopify_Refund,
            'API': Refund,
            'handler': refundHandler.RefundHandler,
            'status': [None]
        }
        transactions = {
            'parent_model': Integrations_Shopify_Order,
            'model': Integrations_Shopify_Transaction,
            'API': Transaction,
            'handler': transactionHandler.TransactionHandler,
            'status': [None]
        }
        orders = {
            'model': Integrations_Shopify_Order,
            'API': Order,
            'handler': orderHandler.OrderHandler,
            'status': ['any'],
            'one_off': {
                'refund': refunds,
                'transaction': transactions
            }
        }
        products = {
            'model': Integrations_Shopify_Product,
            'API': Product,
            'handler': productHandler.ProductHandler,
            'status': ['active', 'archived', 'draft']
        }
        customers = {
            'model': Integrations_Shopify_Customer,
            'API': Customer,
            'handler': customerHandler.CustomerHandler,
            'status': [None]
        }
        checkouts = {
            'model': Integrations_Shopify_Abandoned_Checkouts,
            'API': Checkout,
            'handler': checkoutHandler.CheckoutHandler,
            'status': ['open', 'closed']
        }
        rules = {
            'model': Integrations_Shopify_Shop_Price_Rule,
            'API': PriceRule,
            'handler': ruleHandler.RuleHandler,
            'status': [None]
        }
        apis = {
            'product': products,
            'customer': customers,
            'order': orders,
            'rule': rules,
            'checkout': checkouts
        }

        return apis

    def set_sync_state(self, user_id, integration_name, celery_id):
        return super().set_sync_state(user_id, integration_name, celery_id)

    def build_auth_params(self, integration_name, user):

        list_of_account_info = []

        last_sync = self.checkLastSync(user.id, integration_name, 2)
        initialize = last_sync['initialize']
        should_sync = last_sync['should_sync']
        last_sync_time = last_sync['last_sync_time']

        shopify_accounts = SocialAccount.objects.filter(
            user_id=user.id, provider="shopify")
        for shopify_account in shopify_accounts:
            account_id = shopify_account.id
            shop_access_token = SocialToken.objects.get(
                account_id=account_id).token
            account_info = {'access_token': shop_access_token,
                            'account_id': account_id,
                            'shopify_account': shopify_account,
                            'integration_name': integration_name,
                            'user': user,
                            'user_iden': user.id,
                            'initialize': initialize,
                            'last_sync_time': last_sync_time}
            list_of_account_info.append(account_info)

        return list_of_account_info
        # return super().build_auth_params(integration_name, user)


@shared_task(time_limit=36000, name="initialize_shopify_syncworker_task")
def initialize_shopify_syncworker_task(integration=None, user=None):

    if not integration or not user:
        user, integration = DjangoUser.objects.get(
            id=Master_Blocklight_User.User_Id), ShopifyIntegration()

    task_id = initialize_shopify_syncworker_task.request.id

    try:
        print("ABOUT TO SAVE")
        result = sync.save_shopify(
            integration=integration, user=user, task_id=task_id)
        logger.debug("releasing lock")

        return result

    except Exception as e:
        logger.debug("Sync Failed, releasing lock")
        raise e
