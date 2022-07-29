from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseNotFound, HttpResponseBadRequest, JsonResponse, HttpResponseRedirect
from django.views import View
from django.conf import settings

from stripe_payments.models import StripeCustomer
from user_tiers.models import Tier, UserTier
from user_tiers.tasks import execute_payment, add_one_recurring_year, get_next_payment_day

from mixpanel import Mixpanel
from datetime import date, timedelta
import stripe
import logging


logger = logging.getLogger(__name__)


class ChangeTierView(LoginRequiredMixin, View):

    def get(self, request):
        tier_name = request.GET['tier']
        recurring_period = request.GET['recurring_period']

        try:
            change_to_tier = Tier.objects.get(name=tier_name, recurring_period=recurring_period)
        except Tier.DoesNotExist:
            logger.info("Requested tier not found. (tier_name: {}_{})".format(tier_name, recurring_period))
            return HttpResponseNotFound("Requested tier ({}_{}) does not exists.".format(tier_name, recurring_period))

        try:
            user_tier = UserTier.objects.get(user=request.user)
        except UserTier.DoesNotExist:
            logger.info("User does not have registered any tier yet. (user: {})".format(request.user))
            return HttpResponseNotFound("User does not have registered any tier yet.")

        # Upgrade from trial version
        if user_tier.tier.level_num == 0:

            # TODO:
            #   - it's a duplicate of the one which is bellow in the function
            #   - error handling
            #   - don't depend on server' hostname(eg. running in Docker), use environments variables
            #   - Note that this is only request for a change, not actually confirmed/payed change
            # Send Tier Change to Mixpanel
            current_host = request.get_host()
            if current_host == 'blocklight.io':
                mp = Mixpanel(settings.MIXPANEL_TOKEN)
                mp.track(request.user.id, 'Tier Change', {
                    'Old Tier': user_tier.tier.name,
                    'New Tier': change_to_tier.name,
                    'Email': request.user.email
                })

            return HttpResponseRedirect(reverse('stripe_payments:recurring-payment', args=[tier_name, recurring_period]))

        if (user_tier.tier.level_num == change_to_tier.level_num) \
                and (user_tier.tier.recurring_period == change_to_tier.recurring_period):
            return HttpResponseRedirect(reverse('profile'))

        try:
            customer = StripeCustomer.objects.get(user=user_tier.user)
        except StripeCustomer.DoesNotExist:
            logger.info("User requested change of tier without having credit card saved.")

        # Change of recurring period is done on the day when current recurring period ends
        if change_to_tier.recurring_period != user_tier.tier.recurring_period:
            user_tier.requested_tier_change = change_to_tier
            user_tier.save()
            return HttpResponseRedirect(reverse('profile'))

        # Upgrade
        if change_to_tier.level_num > user_tier.tier.level_num:
            # when upgrading 'monthly tier', the user is billed on usual billing day
            if recurring_period == 'yearly':
                today = date.today()
                credit = round((1 - ((today - user_tier.last_payment_date).days/365)) * user_tier.tier.price, 2)
                to_pay = change_to_tier.price - credit
                try:
                    execute_payment(customer, user_tier, price=int(to_pay))
                except Exception as e:
                    logger.error("Error executing payment for upgrade of yearly payments period. \n{}".format(e))
                    logger.exception(e)
                    return HttpResponseBadRequest("Error executing payment")

                user_tier.payments_start_date = today
                user_tier.last_payment_date = today
                user_tier.valid_until = add_one_recurring_year(today)

                # Send Tier Change to Mixpanel
                current_host = request.get_host()
                if current_host == 'blocklight.io':
                    mp = Mixpanel(settings.MIXPANEL_TOKEN)
                    mp.track(request.user.id, 'Tier Change', {
                        'Old Tier': user_tier.tier.name,
                        'New Tier': change_to_tier.name,
                        'Email': request.user.email
                    })

        # Downgrade
        elif change_to_tier.level_num < user_tier.tier.level_num:
            if recurring_period == 'yearly':
                today = date.today()
                credit = round((1 - ((today - user_tier.last_payment_date).days / 365)) * user_tier.tier.price, 2)
                to_pay = change_to_tier.price - credit

                if to_pay > 0:
                    try:
                        execute_payment(customer, user_tier, price=int(to_pay))
                    except Exception as e:
                        logger.error("Error executing payment to downgrade user tier. \n{}".format(e))
                        return HttpResponseBadRequest("Error executing payment to downgrade user tier")
                    valid_until = add_one_recurring_year(today)
                elif to_pay < 0:
                    additional_days = int(((to_pay * -1) / change_to_tier.price) * 365)
                    valid_until = add_one_recurring_year(today) + timedelta(additional_days)
                else:
                    valid_until = add_one_recurring_year(today)

                customer.payments_start_date = today
                user_tier.valid_until = valid_until
            else:
                user_tier.requested_tier_change = change_to_tier
                user_tier.save()
                return HttpResponseRedirect(reverse('profile'))

        # TODO:
        #   - error handling
        #   - don't depend on server' hostname(eg. running in Docker), use environments variables
        #   - Note that this is only request for a change, not actually confirmed/payed change
        # Send Tier Change to Mixpanel
        current_host = request.get_host()
        if current_host == 'blocklight.io':
            mp = Mixpanel(settings.MIXPANEL_TOKEN)
            mp.track(request.user.id, 'Tier Change', {
                'Old Tier': user_tier.tier.name,
                'New Tier': change_to_tier.name,
                'Email': request.user.email
            })

        user_tier.tier = change_to_tier
        user_tier.save()
        return HttpResponseRedirect(reverse('profile'))


class TierCancelView(LoginRequiredMixin, View):
    # template_name = 'stripe_payments/tier_cancel.html'

    def get(self, request):

        try:
            user_t = UserTier.objects.get(user=request.user)
        except UserTier.DoesNotExist:
            logger.info("User does not have registered any tier. (user: {})".format(request.user))
            return HttpResponseNotFound("User does not have registered any tier.")

        # TODO:
        #   - error handling
        #   - don't depend on server' hostname(eg. running in Docker), use environments variables
        #   - Note that this is only request for a change, not actually confirmed/payed change
        # Send Tier Change to Mixpanel
        current_host = request.get_host()
        if current_host == 'blocklight.io':
            mp = Mixpanel(settings.MIXPANEL_TOKEN)
            mp.track(request.user.id, 'Tier Change', {
                'Old Tier': user_t.tier.name,
                'New Tier': 'Cancelled',
                'Email': request.user.email
            })

        if request.user.userprofile_set.last().signed_via_shopify:
            return redirect(reverse('shopify_payments:cancel-tier'))

        user_t.requested_cancel = True
        user_t.save()
        return HttpResponseRedirect(reverse('profile'))
        # return HttpResponse()


class RequestedTierCancelView(LoginRequiredMixin, View):
    # template_name = 'stripe_payments/tier_cancel.html'

    def get(self, request):

        try:
            user_t = UserTier.objects.get(user=request.user)
        except UserTier.DoesNotExist:
            logger.info("User does not have registered any tier. (user: {})".format(request.user))
            return HttpResponseNotFound("User does not have registered any tier.")

        user_t.requested_tier_change = None
        user_t.save()
        return HttpResponseRedirect(reverse('profile'))


class CancelRequestedTierCancelView(LoginRequiredMixin, View):
    # template_name = 'stripe_payments/tier_cancel.html'

    def get(self, request):

        try:
            user_t = UserTier.objects.get(user=request.user)
        except UserTier.DoesNotExist:
            logger.info("User does not have registered any tier. (user: {})".format(request.user))
            return HttpResponseNotFound("User does not have registered any tier.")

        user_t.requested_cancel = False
        user_t.save()
        return HttpResponseRedirect(reverse('profile'))


class SubscriptionInfoView(LoginRequiredMixin, View):

    def get(self, request):
        card_last4 = None
        try:
            try:
                customer = StripeCustomer.objects.get(user=request.user)
                card_last4 = stripe.PaymentMethod.retrieve(
                    customer.payment_method_id,
                    api_key=settings.STRIPE_SECRET_KEY
                ).card.last4
            except StripeCustomer.DoesNotExist:
                pass
        except Exception as e:
            # TODO: It's not error anymore, when the user uses Shopify's payment gateway
            logger.error("Error retrieving credit card info: {}".format(e))

        try:
            user_tier = UserTier.objects.get(user=request.user)
            current_tier = {
                'name': user_tier.tier.name,
                'recurring_period': user_tier.tier.recurring_period,
                'public_name': user_tier.tier.public_name
            }
            requested_tier_change = {
                'name': user_tier.requested_tier_change.name,
                'recurring_period': user_tier.requested_tier_change.recurring_period,
                'public_name': user_tier.requested_tier_change.public_name
                # Shopify's users gets the updates immediately
            } if user_tier.requested_tier_change and (not request.user.userprofile_set.first().signed_via_shopify) \
                else None
            requested_cancel = True if user_tier.requested_cancel else False
            next_payment_price = None
            if not user_tier.requested_cancel:
                next_payment_price = user_tier.tier.price if not user_tier.requested_tier_change else \
                    user_tier.requested_tier_change.price
            next_payment_date = get_next_payment_day(user_tier) if user_tier.active else None
        except UserTier.DoesNotExist:
            current_tier = None
            requested_tier_change = None
            requested_cancel = None
            next_payment_price = None
            next_payment_date = None

        # possible_tiers = [{
        #     'public_name': t.public_name,
        #     'name': t.name,
        #     'recurring_period': t.recurring_period,
        # } for t in Tier.objects.all()]

        return JsonResponse({
            'card_last4': card_last4,
            'current_tier': current_tier,
            'requested_tier_change': requested_tier_change,
            'requested_cancel': requested_cancel,
            # 'possible_tiers': possible_tiers,
            'next_payment_price': next_payment_price,
            'next_payment_date': next_payment_date,
        })
