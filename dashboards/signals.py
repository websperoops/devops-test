from allauth.account.app_settings import EmailVerificationMethod
from allauth.account.signals import user_signed_up
from allauth.account.utils import perform_login
from allauth.socialaccount.models import SocialAccount, SocialToken, SocialApp, SocialLogin
from allauth.socialaccount.signals import social_account_added, pre_social_login

from blocklight import settings
from blocklight_api import models as blapi_models

from dashboards.models import UserProfile
from dashboards.tasks import sync_users_integrations, user_sync_on_integration
from celery import group, chain, chord
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.shortcuts import redirect
from django.db import transaction

from layout.views import mailchimp_signup
import logging
from mixpanel import Mixpanel
import requests


logger = logging.getLogger(__name__)


@receiver(pre_social_login)
def link_to_local_user(sender, request, sociallogin, **kwargs):
    '''
    Django all-auth creates a new account if you sign up via socials (ie. Shopify), even if the email address associated
    with the account is in use with our app (it prompts a new email).  Catching the following signal allows us to link the
    social account to an existing user if the email address is already in use with Blocklight.
    '''

    if request.path == '/shopify/login/callback/' and not (request.user.is_authenticated):
        email_address = sociallogin.account.extra_data['shop']['email']
        users = User.objects.filter(email=email_address)
        if users:
            UserProfile.objects.get_or_create(user_id=users[0].id)
            try:
                sociallogin.connect(request, users[0])
                social_account_added.send(sender=SocialLogin,
                                          request=request,
                                          sociallogin=sociallogin)
            except:
                messages.error(
                    request, "This Shopify store is already associated with a blocklight account.")
                return redirect('/dashboards/integrations')

            perform_login(
                request, users[0], email_verification=EmailVerificationMethod.NONE)

            return redirect('/dashboards/integrations')
    else:
        pass


@receiver(user_signed_up)
def complete_signup(request, user, **kwargs):
    '''
    When a user signs up via shopify we need to do some processing with their information.
    Catching the following signal allows us to create the user profile and favorites dashboards
    before they reach the app.
    '''
    request.user = user

    if kwargs['sociallogin'] is not None:
        social_account_added.send(sender=SocialLogin,
                                  request=request,
                                  sociallogin=kwargs['sociallogin'])

    # Update User Info
    user.username = user.email
    user.first_name = 'shopify_signup'
    user.save()

    # Add user to mailchimp lists
    mailchimp_signup(user)

    # Create User Profile
    UserProfile.objects.create(user_id=user.id, signed_via_shopify=True)

    # Create Favorites Dashboard
    blapi_models.BLDashboard(
        name='Favorite',
        user=user,
        is_favorite=True
    ).save()


def safe_request1(url, key, tries=3):
    logger.info("MAKING URL REQUEST FOR {}".format(url))
    found_key = False
    while not found_key and tries > 0:
        resp = requests.get(url).json()
        data = resp['data']
        for i in data:
            if key in i:
                return i
            else:
                tries -= 1
    return None


def safe_request2(url, key, tries=3):
    found_key = False
    while not found_key and tries > 0:
        resp = requests.get(url).json()

        if key in resp:
            return resp[key]
        else:
            tries -= 1
    return None


@receiver(social_account_added)
def create_additional_social_accounts(signal, sender, request, sociallogin, **kwargs):
    """
        In case of adding Facebook integration, we want to create records for Instagram integration as well.
    """
    if sociallogin.account.provider == 'facebook':
        logger.info("CHECKING FOR IG")

        # Check if we can get an ig token
        fb_acc = SocialAccount.objects.filter(
            provider="facebook", user_id=request.user.id).first()
        logger.info("FB ACC QUERY FIRED")
        acc_id = fb_acc.id
        fb_token_row = SocialToken.objects.filter(account_id=acc_id).first()
        fb_token = fb_token_row.token
        logger.info("TOKEN: {}".format(fb_token))
        logger.info("SOCIAL TOKEN QUERY FIRED")
        fb_id = fb_acc.uid
        fb_url = "https://graph.facebook.com/v8.0/{}/accounts?fields=id,name&access_token={}".format(
            fb_id, fb_token)
        page_id = safe_request1(fb_url, "id")
        page_id = page_id['id']

        # if we can get a page id, then see if an instagram business account is linked to it
        logger.info("ACCESS-TOKEN-URL: {}".format(fb_url))
        logger.info("PAGE_ID: {}".format(page_id))

        if page_id:
            page_url = "https://graph.facebook.com/v8.0/{}?fields=instagram_business_account,access_token&access_token={}".format(
                page_id, fb_token)
            ig_acc = safe_request2(page_url, "instagram_business_account")
            logger.info("IG_ACC: {}".format(ig_acc))

            if ig_acc:
                model_entry, created = SocialAccount.objects.get_or_create(
                    provider='instagram', user_id=request.user.id)
                social_app = SocialApp.objects.get(provider='facebook')

                try:

                    existing_ig_token = SocialToken.objects.get(
                        account=model_entry)
                    existing_ig_token.token = fb_token_row.token
                    existing_ig_token.token_secret = fb_token_row.token_secret
                    existing_ig_token.expires_at = fb_token_row.expires_at
                    existing_ig_token.save()
                except SocialToken.DoesNotExist:

                    token_entry = SocialToken(
                        token=fb_token_row.token,
                        token_secret=fb_token_row.token_secret,
                        expires_at=fb_token_row.expires_at,
                        account_id=model_entry.id,
                        app_id=social_app.id
                    )
                    token_entry.save()

                if created:
                    model_entry.provider = 'instagram'
                    model_entry.user_id = request.user.id
                    model_entry.uid = sociallogin.account.uid
                    model_entry.date_joined = sociallogin.account.date_joined
                    model_entry.last_login = sociallogin.account.last_login
                    model_entry.extra_data = sociallogin.account.extra_data
                    model_entry.save()


def add_syncing_flag(provider, uid):
    soc_acc = SocialAccount.objects.filter(
        provider=provider, user_id=uid).last()
    soc_acc.extra_data['Syncing'] = True
    soc_acc.save()


@receiver(social_account_added)
def toggle_shopify_store(signal, sender, request, sociallogin, **kwargs):
    '''
    When adding a new shopify store, the most recently added will then be selected
    '''
    added_integration = sociallogin.account.provider
    if added_integration == 'shopify':

        with transaction.atomic():
            shopify_accounts = SocialAccount.objects.filter(
                provider='shopify', user_id=request.user.id)

            for shop in shopify_accounts:
                shop.extra_data['is_selected'] = False
                shop.save()

            most_recent_account = shopify_accounts.last()
            most_recent_account.extra_data['is_selected'] = True
            most_recent_account.save()


@receiver(social_account_added)
def sync_new_integration(signal, sender, request, sociallogin, **kwargs):
    added_integration = sociallogin.account.provider

    # NOTE: Google is special case because we cannot run integration inmediately on this signal
    #       The integration will be run in connect_google view
    if added_integration == 'google':
        return

    if added_integration == 'facebook':
        ig_acc = SocialAccount.objects.filter(
            provider="instagram", user_id=request.user.id)
        if len(ig_acc) > 0:
            add_syncing_flag(added_integration, request.user.id)
            user_sync_on_integration(
                request.user.id, ['facebook', 'instagram'])
            logger.info("User (id={}) add new integration (provider=facebook AND instagram). Running sync.".format(
                request.user.id))
            return

    add_syncing_flag(added_integration, request.user.id)

    logger.info("User (id={}) add new integration (provider={}). Running sync.".format(
        request.user.id, added_integration))
    user_sync_on_integration(request.user.id, [added_integration])

    # Send Integration to Mixpanel
    current_host = request.get_host()
    if current_host == 'blocklight.io':
        mp = Mixpanel(settings.MIXPANEL_TOKEN)
        mp.track(request.user.id, 'Integration Sync', {
            'Integration': added_integration,
            'Email': request.user.email
        })


@receiver(user_logged_in)
def login_to_mixpanel(sender, user, request, **kwargs):
    # Send Login to Mixpanel
    current_host = request.get_host()
    if current_host == 'blocklight.io':
        mp = Mixpanel(settings.MIXPANEL_TOKEN)
        mp.track(user.id, 'Login', {
            'Email': user.email
        })


@receiver(user_logged_out)
def logout_to_mixpanel(sender, user, request, **kwargs):
    # Send Logout to Mixpanel
    current_host = request.get_host()
    if current_host == 'blocklight.io':
        mp = Mixpanel(settings.MIXPANEL_TOKEN)
        mp.track(user.id, 'Logout', {
            'Email': user.email
        })


# @receiver(pre_delete, sender=Integrations_Shopify_Order)
# def order_pre_delete(sender, instance, **kwargs):
#     if instance.billing_address is not None:
#         instance.billing_address.delete()
#
#     if instance.shipping_address is not None:
#         instance.shipping_address.delete()
#
#     line_items = instance.integrations_shopify_line_item_set.all()
#     for line_item in line_items:
#         line_item.price_set.delete()
#         line_item.total_discount_set.delete()
