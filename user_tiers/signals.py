from datetime import date

from django.conf import settings
from django.dispatch import receiver

import logging

import stripe
from stripe_payments.models import PaymentIntent
from stripe_payments.signals import stripe_payment_successful
from shopify_payments.signals import shopify_payment_successful
from user_tiers.tasks import setup_user_tier
from user_tiers.models import UserTier


logger = logging.getLogger(__name__)


@receiver(stripe_payment_successful)
@receiver(shopify_payment_successful)
def setup_user_tier_eceiver(sender, user, **kwargs):
    setup_user_tier(user)


def execute_customers_payment(customer, setup_intent):

    logger.info("Executing recurrent payment for customer: {}".format(customer))

    try:
        p_intent_s = stripe.PaymentIntent.create(
            amount=setup_intent.tier.price,
            currency='usd',
            customer=customer.customer_id,
            payment_method=customer.payment_method_id,
            off_session=True,
            confirm=True,
            api_key=settings.STRIPE_SECRET_KEY
        )
        payment_intent = PaymentIntent(
            uid=p_intent_s.id,
            client_secret=p_intent_s.client_secret,
            user=customer.user,
            tier=setup_intent.tier
        )

        try:
            user_tier = UserTier.objects.get(user=customer.user)
        except UserTier.DoesNotExist:
            user_tier = UserTier(
                tier=setup_intent.tier,
                user=customer.user,
                active=True,
                valid_since=date.today()
            )
            user_tier.save()

        user_tier.tier = setup_intent.tier
        payment_intent.save()
        today = date.today()
        if not user_tier.payments_start_date:
            user_tier.payments_start_date = today
        user_tier.last_payment_date = today
        user_tier.save()
    except stripe.error.CardError as e:
        # SEE: https://stripe.com/docs/payments/save-and-reuse#web-create-payment-intent-off-session
        # We should send info to customer, about not working credit card, together with link
        #    to provide card info again
        err = e.error
        # Error code will be authentication_required if authentication is needed
        logger.error("Unable to use saved Card. ErrorCode: {}\n Error: {}".format(err.code, err))