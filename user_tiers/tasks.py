from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.conf import settings

from allauth.socialaccount.models import SocialToken
from stripe_payments.models import StripeCustomer, PaymentIntent
from user_tiers.models import UserTier
from blocklight.celery import app

from calendar import monthrange
from datetime import timedelta, date

import stripe
import shopify
import logging


logger = logging.getLogger(__name__)


def add_one_recurring_month(d):
    # there can be either problem with day or month(new year) too big. There is no case to have both cases at once
    #  December and January has both 31 days
    try:
        return d.replace(month=d.month+1)
    except ValueError:
        # if there is problem with month, day will not be the problem. Dec and Jan has both 31 days
        if d.month == 12:
            return date(d.year+1, 1, d.day)
        else:
            last_day_of_next_month = monthrange(d.year, (d+timedelta(15)).month)[1]
            return (d + timedelta(15)).replace(day=last_day_of_next_month)


def add_one_recurring_year(d):
    try:
        return d.replace(year=d.year+1)
    except ValueError:
        last_day_of_month_of_next_year = monthrange(d.year+1, d.month)
        return date(d.year+1, d.month, last_day_of_month_of_next_year)


def setup_user_tier(user):
    try:
        user_tier = UserTier.objects.get(user=user)
        today = date.today()
        user_tier.valid_until = add_one_recurring_month(today) \
            if user_tier.tier.recurring_period == 'monthly' else add_one_recurring_year(today)

        if not user_tier.payments_start_date:
            user_tier.payments_start_date = today
        user_tier.last_payment_date = today
        user_tier.active = True
        user_tier.save()
    except UserTier.DoesNotExist as e:
        logger.error("UserTier does not exists. User: {}".format(user))
        raise e
 
    logger.info("Saved user's tier {} ".format(user_tier))


@app.task(name='setup_user_tier_task')
def setup_user_tier_task(payment_intent):
    setup_user_tier(payment_intent)


@app.task(name='execute_payment')
def execute_payment(customer, user_tier, price=None):
    logger.info("Executing recurrent payment for customer: {}".format(customer))
    try:
        p_intent_s = stripe.PaymentIntent.create(
            amount=price if price else user_tier.tier.price,
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
            tier=user_tier.tier,
        )
        payment_intent.save()
        setup_user_tier_task.delay(payment_intent)

    except stripe.error.CardError as e:
        # SEE: https://stripe.com/docs/payments/save-and-reuse#web-create-payment-intent-off-session
        # TODO:
        # We should send info to custommer, about not working credit card, together with link
        #    to provide card nfo again
        err = e.error
        # Error code will be authentication_required if authentication is needed
        logger.error("Unable to use saved Card. ErrorCode: {}\n Error: {}".format(err.code, err))
        # payment_intent_id = err.payment_intent['id']
        # payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)

        raise e


def get_next_payment_day(user_tier):
    """
    Simple method to get next payment day using function 'should_user_pay_today'
    """
    day = date.today()
    # if it loops more then 2 years, there is some bug in logic
    look_until = date.today() + timedelta(days=365*2)
    while day < look_until:
        if should_user_pay_today(user_tier, today=day):
            return day
        day = day + timedelta(days=1)
    return None


def should_user_pay_today(user_tier, today=None):
    if user_tier.tier.recurring_period not in ('monthly, yearly'):
        raise ValueError("Recurring period not known: {}".format(user_tier.tier.recurring_period))

    # Didn't payed yet
    if not user_tier.last_payment_date:
        return True

    today = date.today() if not today else today
    # Already payed today
    if user_tier.last_payment_date == today:
        return False

    if user_tier.tier.recurring_period == 'monthly':
        # Today is the day of month when user should pay
        if user_tier.payments_start_date.day == today.day:
            return True

        # If user pay_day is higher then count of days in current month, he pays on last day of month.
        if ((today + timedelta(days=1)).month > today.month) \
                and (user_tier.payments_start_date.day > today.day):
            return True
    elif user_tier.tier.recurring_period == 'yearly':
        # Today is the day of year when user should pay
        if (user_tier.payments_start_date.month == today.month) and (user_tier.payments_start_date.day == today.day):
            return True

        # Handle February 29
        if (user_tier.payments_start_date.month == 2) and (user_tier.payments_start_date.day == 29):
            if ((today.month == 2) and (today.day == 28)) \
                    and ((today + timedelta(days=1)).month > today.month):
                return True

    return False


def cancel_user_tier(user_tier):
    logger.info("Canceling user's tier: {}".format(user_tier))
    StripeCustomer.object.get(user=user_tier.user).delete()
    user_tier.delete()


@app.task(name='execute_all_recurring_payments')
def execute_all_recurring_payments():

    for user_tier in UserTier.objects.all():
        if user_tier.user.userprofile_set.last().signed_via_shopify:
            continue

        try:
            if should_user_pay_today(user_tier):
                if user_tier.requested_cancel:
                    cancel_user_tier(user_tier)
                    continue

                if user_tier.requested_tier_change:
                    user_tier.tier = user_tier.requested_tier_change
                    user_tier.requested_tier_change = None
                    user_tier.save()
                execute_payment(StripeCustomer.objects.get(user=user_tier.user), user_tier)
        except Exception as e:
            logger.exception(e)
            raise e


@app.task(name='execute_all_recurring_payments')
def check_all_shopify_payments():

    for user_tier in UserTier.objects.all():
        if not user_tier.user.userprofile_set.last().signed_via_shopify:
            continue

        try:
            access_token = SocialToken.objects.get(account__user=user_tier.user, account__provider='shopify').token
            # access_token = ShopifyUserAccessToken.objects.get(user=request.user).access_token
        # except ShopifyUserAccessToken.DoesNotExist:
        except SocialToken.DoesNotExist:
            return redirect(reverse('integrate-shopify'))

        try:
            user_tier = UserTier.objects.get(user=user_tier.user)
        except UserTier.DoesNotExist:
            logger.error("UserTier not found durring cancelation of Shopify's recurring payment..")
            return HttpResponseServerError("UserTier not found")

        shopify.Session.setup(api_key=settings.SHOPIFY_API_KEY, secret=settings.SHOPIFY_SECRET)

        session = shopify.Session(settings.SHOPIFY_SHOP_URL, settings.SHOPIFY_API_VERSION, access_token)
        shopify.ShopifyResource.activate_session(session)

        # Shopify orders the items as LIFO (Last In First Out)
        last_recurring_payment_setup = shopify.RecurringApplicationCharge.find_first()

        if last_recurring_payment_setup.status not in ['accepted', 'active']:
            user_tier.delete()


@app.task(name='send_trial_ending_emails')
def send_trial_ending_emails():
    def send_email(user_tiers, num_days):
        if num_days == 1:
            in_place = ' '
            trial_days = 'Tomorrow'
        else:
            in_place = ' in'
            trial_days = f'{num_days} days'
        
        for user_tier in user_tiers:
            try:
                user = User.objects.get(id=user_tier.user_id)
                subject = 'Your Free Trial Is Ending Soon'
                html_message = render_to_string('account/email/trial_ending_email.html', {
                    'user': user,
                    'num_days': trial_days,
                    'until': user_tier.valid_until,
                    'in': in_place
                })
                message = strip_tags(html_message)
                send_mail(subject, message, None, [user.email], True, html_message=html_message)

            except Exception as e:
                logger.exception(e)
                raise e
        
    for num_days in [7, 3, 1]:
        valid_until_date = date.today() + timedelta(num_days)
        user_tiers = UserTier.objects.filter(
            tier_id=1,
            valid_until=valid_until_date
        )
        try:
            send_email(user_tiers, num_days)
        except Exception as e:
            raise e
