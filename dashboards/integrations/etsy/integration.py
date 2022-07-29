from ...integrations.integration import Integration
from . import listingHandler, receiptHandler, ledgerHandler, transactionHandler
from . import sync
from .etsyAPI import getActiveListings, getInactiveListings, getDraftListings, getExpiredListings, getReceipts, getTransactions, getLedgerEntries
from allauth.socialaccount.models import SocialAccount,  SocialApp, SocialToken
from celery import shared_task
from dashboards.models import Integrations_Etsy_Listing, Integrations_Etsy_Receipt, Integrations_Etsy_Transaction, Integrations_Etsy_Ledger_Entry
from dashboards.integrations.utils.dashboard_sync_complete import dashboard_sync_complete, token_failure
from django.contrib.auth.models import User as DjangoUser
import logging
from requests_oauthlib import OAuth1Session
from ...enums.CoreEnums import Master_Blocklight_User


logger = logging.getLogger(__name__)


class EtsyIntegration(Integration):
    def get_task(self, user):
        task = initialize_etsy_syncworker_task
        tcount = SocialAccount.objects.filter(provider='etsy', user_id=user.id).count()
        return task, tcount

    @staticmethod
    def genOAuthSession(uid):
        account_id = SocialAccount.objects.get(provider='etsy', user_id=uid).id
        etsyApp = SocialApp.objects.get(provider='etsy')
        etsyToken = SocialToken.objects.get(app_id=etsyApp.id, account_id=account_id)
        oauth1Session = OAuth1Session(etsyApp.client_id,
                            client_secret=etsyApp.secret,
                            resource_owner_key=etsyToken.token,
                            resource_owner_secret=etsyToken.token_secret)

        return oauth1Session

    def get_params(self, uid):
        etsy_id = SocialAccount.objects.get(provider='etsy', user_id=uid).extra_data["user_id"]
        request = EtsyIntegration.genOAuthSession(uid)
        
        active_listings = {
            'model': Integrations_Etsy_Listing,
            'API': getActiveListings,
            'handler': listingHandler.ListingHandler
        }

        inactive_listings = {
            'model': Integrations_Etsy_Listing,
            'API': getInactiveListings,
            'handler': listingHandler.ListingHandler
        }

        draft_listings = {
            'model': Integrations_Etsy_Listing,
            'API': getDraftListings,
            'handler': listingHandler.ListingHandler
        }

        expired_listings = {
            'model': Integrations_Etsy_Listing,
            'API': getExpiredListings,
            'handler': listingHandler.ListingHandler
        }

        receipts = {
            'model': Integrations_Etsy_Receipt,
            'API': getReceipts,
            'handler': receiptHandler.ReceiptHandler
        }

        transactions = {
            'model': Integrations_Etsy_Transaction,
            'API': getTransactions,
            'handler': transactionHandler.TransactionHandler
        }

        ledger = {
            'model': Integrations_Etsy_Ledger_Entry,
            'API': getLedgerEntries,
            'handler': ledgerHandler.LedgerHandler
        }

        apis = {
            'active_listings': active_listings,
            'inactive_listings': inactive_listings,
            'draft_listings': draft_listings,
            'expired_listings': expired_listings,
            'receipts': receipts,
            'transactions': transactions,
            'ledger': ledger
        }

        return request, etsy_id, apis

    def set_sync_state(self, user_id, integration_name, celery_id):
        return super().set_sync_state(user_id, integration_name, celery_id)

    def build_auth_params(self, integration_name, user):
        return super().build_auth_params(integration_name, user)


@shared_task(time_limit=36000, name="initialize_etsy_syncworker_task")
def initialize_etsy_syncworker_task(integration=None, user=None):

    if not integration or not user:
        user = DjangoUser.objects.get(id=Master_Blocklight_User.User_Id)
        integration = EtsyIntegration()

    task_id = initialize_etsy_syncworker_task.request.id

    try:
        result = sync.save_etsy(integration=integration, user=user, task_id=task_id)
        dashboard_sync_complete('etsy', user.id)
        return result

    except Exception as e:
        logger.debug("Sync Failed - Etsy")
        token_failure('etsy', user.id)
        dashboard_sync_complete('etsy', user.id)
        raise e
