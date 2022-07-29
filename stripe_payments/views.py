from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseNotFound, HttpResponseServerError, HttpResponseBadRequest, HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

import logging

import stripe
from stripe_payments.models import PaymentIntent, SetupIntent, StripeCustomer
from stripe_payments.signals import stripe_payment_successful
from user_tiers.models import Tier
from user_tiers.signals import execute_customers_payment


logger = logging.getLogger(__name__)


# class OneTimePaymentView(LoginRequiredMixin, View):
#     """
#     View to provide one time payments supported by Stripe.
#     It loads required Tier, checks for already existing PaymentIntent and updates or creates it if changed/missing.
#     Then the payment form is rendered including the client_secret for PaymentIntent.
#     """
#
#     template_name = 'stripe_payments/one_time_payment.html'
#
#     def get(self, request, tier_name):
#
#         try:
#             tier = Tier.objects.get(unique_name=tier_name)
#         except Tier.DoesNotExist:
#             logger.info("Requested tier not found tier_name: {}".format(tier_name))
#             return HttpResponseNotFound("Tier does not exists.")
#
#         try:
#             try:
#                 payment_intent = PaymentIntent.objects.get(user=request.user, recurring_payment=False)
#                 try:
#                     p_intent_s = stripe.PaymentIntent.retrieve(
#                         payment_intent.uid,
#                         api_key=settings.STRIPE_SECRET_KEY
#                     )
#                 except Exception as e:
#                     logger.error("Error retrieving PaymentIntent \n {}".format(e))
#
#                 # If webhook (or it's signal handlers) will fail and didn't handle successfull payment,
#                 # we log the error for us and let user continue in new payment.
#                 if p_intent_s.status == 'succeeded':
#                     logger.error(
#                         "THERE IS SUCCEEDED PAYMENTINTENT WHICH WASN'T DELETED.\n"
#                         + "It means propably user had not assigned TIER properly.\n"
#                         + "It's PaymentIntent {}".format(payment_intent)
#                     )
#                     payment_intent.delete()
#                     raise PaymentIntent.DoesNotExist()
#
#                 # Update 'price' if user changed tier which he wants to buy
#                 if payment_intent.tier.unique_name != tier_name:
#                     stripe.PaymentIntent.update(
#                         payment_intent.uid,
#                         amount=tier.price,
#                         currency='usd',
#                         api_key=settings.STRIPE_SECRET_KEY
#                     )
#                     payment_intent.tier = Tier.objects.get(unique_name=tier_name)
#                     payment_intent.save()
#
#             except PaymentIntent.DoesNotExist:
#                 p_intent_s = stripe.PaymentIntent.create(
#                     amount=tier.price,
#                     currency='usd',
#                     api_key=settings.STRIPE_SECRET_KEY
#                 )
#                 payment_intent = PaymentIntent(
#                     uid=p_intent_s.id,
#                     client_secret=p_intent_s.client_secret,
#                     user=request.user,
#                     tier=tier
#                 )
#                 payment_intent.save()
#         except Exception as e:
#             logger.error("Error durring creation of PaymentIntent \n {}".format(e))
#             return HttpResponseServerError()
#
#         tmpl_context = {
#             'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
#             'client_secret': payment_intent.client_secret,
#             'tier_public_name': tier.public_name
#         }
#
#         return render(request, self.template_name, tmpl_context)


class RecurringPaymentView(LoginRequiredMixin, View):
    """
    View to provide form for saving card info for recurring payments supported by Stripe.
    It checks for already existing SetupIntent and updates or creates it if changed/missing.
    Then the payment form is rendered including the client_secret for SetupIntent.
    User can put card info and confirm saving of credit card info.
    """

    template_name = 'stripe_payments/recurring_payment.html'

    def get(self, request, tier_name, recurring_period):

        try:
            tier_to_set = Tier.objects.get(name=tier_name, recurring_period=recurring_period)
        except Tier.DoesNotExist:
            logger.info("Requested tier not found tier_name: {}".format(tier_name))
            return HttpResponseNotFound("Tier does not exists.")

        try:
            try:
                setup_intent = SetupIntent.objects.get(user=request.user)
            except SetupIntent.DoesNotExist:
                s_intent_s = stripe.SetupIntent.create(
                    payment_method_types=["card"],
                    api_key=settings.STRIPE_SECRET_KEY,
                )
                setup_intent = SetupIntent(
                    uid=s_intent_s.id,
                    client_secret=s_intent_s.client_secret,
                    user=request.user,
                    pay_after_succeeded=True,
                    tier=tier_to_set
                )
                setup_intent.save()
        except Exception as e:
            logger.error("Error durring creation of SetupIntent \n {}".format(e))
            return HttpResponseServerError()

        tmpl_context = {
            'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
            'client_secret': setup_intent.client_secret,
            'price': int(tier_to_set.price / 100)
        }

        return render(request, self.template_name, tmpl_context)


class ChangeCreditCardView(LoginRequiredMixin, View):

    template_name = 'stripe_payments/recurring_payment.html'

    def get(self, request):
        try:
            for setup_intent in SetupIntent.objects.filter(user=request.user):
                setup_intent.delete()

            s_intent_s = stripe.SetupIntent.create(
                payment_method_types=["card"],
                api_key=settings.STRIPE_SECRET_KEY,
            )
            setup_intent = SetupIntent(
                uid=s_intent_s.id,
                client_secret=s_intent_s.client_secret,
                user=request.user,
                pay_after_succeeded=False,
            )
            setup_intent.save()
        except Exception as e:
            logger.error("Error durring creation of SetupIntent \n {}".format(e))
            return HttpResponseServerError()

        tmpl_context = {
            'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
            'client_secret': setup_intent.client_secret,
        }

        return render(request, self.template_name, tmpl_context)


@method_decorator(csrf_exempt, name='dispatch')
class WebHookView(View):
    """
    This endpoint serves for receiving events from Stripe.
    It's configured in Stripe Dashboard.
    It receives events 'payment_intent.succeeded' and 'setup_intent.succeeded' and
        does needed handling for this events.
    It sends Signals payment_intent_successful, setup_intent_successful which other apps can receive and handle.

    After successfull PaymentIntent(One time payment of client) we want to assign tier to the User.
    After successful SetupIntent(Saving credit card info for recurring payments) we want to register User for monthly
    payments for particullar tier.
    """

    def post(self, request):
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_ENDPOINT_SECRET
            )
        except ValueError as e:
            logger.warn("Stripe WebHook requested with invalid payload. \n {}".format(e))
            return HttpResponseBadRequest()
        except stripe.error.SignatureVerificationError:
            logger.warn("Stripe WebHook requested with invalid signature")
            return HttpResponseBadRequest()

        # # Handle the event
        # # Note: for localhost testing: (Only uncomment)
        # if event.type == 'payment_intent.succeeded':
        #     # # testing code
        #     from django.contrib.auth.models import User
        #     payment_intent = PaymentIntent.objects.get(user=User.objects.get(id=69), recurring_payment=False)
        #     payment_intent_successful.send(sender=self.__class__, payment_intent=payment_intent)
        #     logger.info('Successful PaymentIntent!')
        #     return HttpResponse()
        if event.type == 'payment_intent.succeeded':
            p_intent_s = event.data.object  # contains a stripe.PaymentIntent
            # Note: this is how to retrieve p_intent_s, when need to test it manualy
            # p_intent_s = stripe.PaymentIntent.retrieve(
            #     payment_intent.uid,
            #     api_key=settings.STRIPE_SECRET_KEY
            # )
            try:
                payment_intent = PaymentIntent.objects.get(uid=p_intent_s.id)
            except PaymentIntent.DoesNotExist:
                logger.error("Received successfull painentIntent which is not in database.")
                return HttpResponse()
            stripe_payment_successful.send(sender=self.__class__, user=payment_intent.user)
            logger.info('Successful PaymentIntent!')
            payment_intent.delete()

        elif event.type == 'setup_intent.succeeded':
            # Note: For local host testing: unindent 1 level, comment one line above and one line bellow
            # elif event.type == 'invoice.created':  # local stripe CLI doesn't support setup_intent.succeeded
            #     from django.contrib.auth.models import User
            #     setup_intent = SetupIntent.objects.get(user=User.objects.get(id=69))
            #     s_intent_s = stripe.SetupIntent.retrieve(
            #         setup_intent.uid,
            #         api_key=settings.STRIPE_SECRET_KEY
            #     )
            #     logger.info('Successful SetupIntent! Setting up customer.')

            s_intent_s = event.data.object  # contains a stripe.SetupIntent
            # Note: this is how to retrieve s_intent_s, when need to test it manualy
            # s_intent_s = stripe.SetupIntent.retrieve(
            #     setup_intent.uid,
            #     api_key=settings.STRIPE_SECRET_KEY
            # )

            try:
                setup_intent = SetupIntent.objects.get(client_secret=s_intent_s.client_secret)
            except SetupIntent.DoesNotExist:
                logger.error("Received setup intent which is not registered by us.")
                return HttpResponseServerError()

            # try:
            #     customer = StripeCustomer.objects.get(user=setup_intent.user)
            # except StripeCustomer.DoesNotExist:

            # delete all old customer records for this user
            for customer in StripeCustomer.objects.filter(user=setup_intent.user):
                customer.delete()

            customer_s = stripe.Customer.create(api_key=settings.STRIPE_SECRET_KEY)
            customer = StripeCustomer(
                customer_id=customer_s.id,
                user=setup_intent.user,
            )
            customer.save()

            try:
                stripe.PaymentMethod.attach(
                    s_intent_s.payment_method,
                    customer=customer.customer_id,
                    api_key=settings.STRIPE_SECRET_KEY
                )
            except Exception as e:
                logger.error("Error attching payment method to customer: {}".format(e))

            customer.payment_method_id = s_intent_s.payment_method
            customer.save()
            if setup_intent.pay_after_succeeded:
                execute_customers_payment(customer, setup_intent)
            setup_intent.delete()
        else:
            # Unexpected event type
            logger.warn("Unexpected event type in Stripe WebHook: {}".format(event.type))
            return HttpResponseBadRequest()

        return HttpResponse()
