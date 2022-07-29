from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.shortcuts import redirect
from django.conf import settings
from django.http.response import HttpResponseNotFound, HttpResponseServerError, HttpResponseBadRequest, HttpResponse

from shopify_payments.signals import shopify_payment_successful
# from shopify_payments.models import ShopifyUserAccessToken
from user_tiers.models import Tier, UserTier
from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken

import shopify

from datetime import datetime
# import binascii
import logging
import os

logger = logging.getLogger(__name__)


class RecurringPaymentView(LoginRequiredMixin, View):

    def get(self, request, tier_name, recurring_period):

        try:
            tier_to_set = Tier.objects.get(name=tier_name, recurring_period=recurring_period)
        except Tier.DoesNotExist:
            logger.info("Requested tier not found tier_name: {}".format(tier_name))
            return HttpResponseNotFound("Tier does not exists.")

        # try:
        #     access_token = ShopifyUserAccessToken.objects.get(user=request.user).access_token
        # except ShopifyUserAccessToken.DoesNotExist:
        #     return redirect('{}/?tier={}&recurring_period={}'.format(
        #             reverse('shopify_payments:login'),
        #             tier_to_set.name,
        #             tier_to_set.recurring_period,
        #     ))

        try:
            social_account = SocialAccount.objects.get(user=request.user, provider='shopify')
            access_token = SocialToken.objects.get(account=social_account).token
            shop_name = social_account.extra_data['shop']['name']
        except:
            return redirect(reverse('integrate-shopify'))
            # return redirect('{}/?tier={}&recurring_period={}'.format(
            #         reverse('shopify_payments:login'),
            #         tier_to_set.name,
            #         tier_to_set.recurring_period,
            # ))
            #

        try:
            user_tier = UserTier.objects.get(user=request.user)
            user_tier.requested_tier_change = tier_to_set
            user_tier.save()
        except UserTier.DoesNotExist:
            UserTier.objects.create(
                tier=tier_to_set,
                requested_tier_change=tier_to_set,
                user=request.user,
                valid_since=datetime.now(),
            )
        shopify_key = SocialApp.objects.get(provider='shopify').client_id
        shopify_secret = SocialApp.objects.get(provider='shopify').secret
        shopify.Session.setup(api_key=shopify_key, secret=shopify_secret)

        session = shopify.Session(shop_name, settings.SHOPIFY_API_VERSION, access_token)
        shopify.ShopifyResource.activate_session(session)

        charge = shopify.RecurringApplicationCharge.create({
            'name': tier_to_set.public_name,
            'price': tier_to_set.price / 100,
            'return_url': request.build_absolute_uri(reverse('shopify_payments:accepted_payment'))
        })
        # return redirect('shopify_payments:login')

        if not charge.is_valid:
            return redirect(reverse('integrate-shopify'))
        #     return redirect('{}/?tier={}&recurring_period={}'.format(
        #             reverse('shopify_payments:login'),
        #             tier_to_set.tier_name,
        #             tier_to_set.recurring_period,
        #     ))

        return redirect(charge.confirmation_url)


class AcceptedPaymentView(LoginRequiredMixin, View):

    def get(self, request):
        shopify_key = SocialApp.objects.get(provider='shopify').client_id
        shopify_secret = SocialApp.objects.get(provider='shopify').secret
        shopify.Session.setup(api_key=shopify_key, secret=shopify_secret)
        try:
            social_account = SocialAccount.objects.get(user=request.user, provider='shopify')
            access_token = SocialToken.objects.get(account=social_account).token
            shop_name = social_account.extra_data['shop']['name']
        except:
            return redirect(reverse('integrate-shopify'))

        session = shopify.Session(shop_name, settings.SHOPIFY_API_VERSION, access_token)
        shopify.ShopifyResource.activate_session(session)

        charge = shopify.RecurringApplicationCharge.find(request.GET['charge_id'])

        if charge.status != 'accepted':
            return redirect(reverse('homepage'))

        shopify.RecurringApplicationCharge.activate(charge)

        if charge.status != 'active':
            return redirect(reverse('homepage'))

        user_tier = request.user.usertier
        user_tier.tier = user_tier.requested_tier_change
        user_tier.requested_tier_change = None
        user_tier.save()
        shopify_payment_successful.send(sender=self.__class__, user=request.user)

        return redirect(reverse('homepage'))


# class ShopifyLoginView(LoginRequiredMixin, View):
#
#     def get(self, request):
#
#         shopify.Session.setup(api_key=settings.SHOPIFY_API_KEY, secret=settings.SHOPIFY_SECRET)
#
#         shop_url = settings.SHOPIFY_SHOP_URL
#         api_version = '2020-10'
#
#         state = binascii.b2a_hex(os.urandom(15)).decode("utf-8")
#         # redirect_uri = 'https://127.0.0.1:8000/shop_success/'
#         # redirect_uri = reverse('shopify_payments:login-success')
#         redirect_uri = '{}/?tier={}&recurring_period={}'.format(
#                 request.build_absolute_uri(reverse('shopify_payments:login')),
#                 request.GET['tier'],
#                 request.GET['recurring_period'],
#         )
#
#         scopes = ['read_products', 'read_orders']
#
#         new_session = shopify.Session(settings.SHOPIFY_SHOP_URL, settings.SHOPIFY_API_VERSION)
#         auth_url = new_session.create_permission_url(scopes, redirect_uri, state)
#         return redirect(auth_url)
#
#
# class ShopifyLoginSuccessView(LoginRequiredMixin, View):
#
#     def get(self, request):
#
#         shopify.Session.setup(api_key=settings.SHOPIFY_API_KEY, secret=settings.SHOPIFY_SECRET)
#
#         new_session = shopify.Session(settings.SHOPIFY_SHOP_URL, settings.SHOPIFY_API_VERSION)
#         access_token = new_session.request_token(request.GET)  # request_token will validate hmac and timing attacks
#
#         user_access_token = ShopifyUserAccessToken.objects.get(user=request.user)
#         user_access_token.access_token = access_token
#         user_access_token.save()
#
#         return redirect('{}/?tier={}&recurring_period={}'.format(
#             reverse('shopify_payments:login'),
#             request.GET['tier'],
#             request.GET['recurring_period'],
#         ))
#

# NOTE: For stripe_payments, the Change and Cancel Views are inside user_tier.
#       It needs redesign
class ChangeTierView(LoginRequiredMixin, View):

    def get(self, request):
        tier_name = request.GET['tier']
        recurring_period = request.GET['recurring_period']

        return redirect(reverse(
            'shopify_payments:recurring-payment',
            args=[tier_name, recurring_period]
        ))


# NOTE: For stripe_payments, the Change and Cancel Views are inside user_tier.
#       It needs redesign
class CancelTierView(LoginRequiredMixin, View):

    def get(self, request):

        try:
            social_account = SocialAccount.objects.get(user=request.user, provider='shopify')
            access_token = SocialToken.objects.get(account=social_account).token
            shop_name = social_account.extra_data['shop']['name']
        except:
            return redirect(reverse('integrate-shopify'))

        try:
            user_tier = UserTier.objects.get(user=request.user)
        except UserTier.DoesNotExist:
            logger.error("UserTier not found during cancellation of Shopify's recurring payment..")
            return HttpResponseServerError("User Tier not found")
        
        shopify_key = SocialApp.objects.get(provider='shopify').client_id
        shopify_secret = SocialApp.objects.get(provider='shopify').secret
        shopify.Session.setup(api_key=shopify_key, secret=shopify_secret)

        session = shopify.Session(shop_name, settings.SHOPIFY_API_VERSION, access_token)
        shopify.ShopifyResource.activate_session(session)

        # Shopify orders the items as LIFO (Last In First Out)
        last_recurring_payment_setup = shopify.RecurringApplicationCharge.find_first()

        # user_tier.tier = Tier.objects.get(name='trial')
        # from datetime import datetime
        # UserTier.objects.create(user=request.user, tier=Tier.objects.get(name='trial'), valid_since=datetime.now())
        last_recurring_payment_setup.destroy()
        user_tier.tier = Tier.objects.get(level_num=99)
        user_tier.valid_since = datetime.today()
        user_tier.valid_until = None
        user_tier.save()

        return redirect(reverse('profile'))
