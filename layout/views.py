from __future__ import print_function

from .form import SignUpForm, PasswordForm, PasswordResetForm
from .tokens import account_activation_token

from allauth.account.app_settings import EmailVerificationMethod
from allauth.account.utils import perform_login

from blocklight import settings
from blocklight_api import models as blapi_models
from dashboards.models import UserProfile
from datetime import date, timedelta

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from layout.models import SignUp
import logging
from mailchimp3 import MailChimp
from mixpanel import Mixpanel
import re
import requests
from user_tiers.models import Tier, UserTier


# TODO: Possibly there could be a functionality of allauth to have smarter routing.
#       So we would not need to do additional request for routing
def router(request):
    """
    After user is authenticated by allauth.account durring 'login' process, he is redirected here.
    This view decides where it shoud redirect based on user's info.
    """
    if request.user.is_authenticated:
        return redirect('/dashboards/homepage/')

    return redirect('/')


############### Signup Process ###############
def generateAffiliateCode(u_id):
    user = User.objects.get(id=u_id)
    email_no_at = user.email.split('@',1)[0]
    affiliate_code = email_no_at + str(u_id)
    return affiliate_code


def validateLoyaltyCode(code):
    try:
        loyalty_check = blapi_models.LoyaltyCode.objects.get(loyalty_code=code)
        loyalty = [True, loyalty_check]
    except blapi_models.LoyaltyCode.DoesNotExist:
        try:
            affiliate_check = UserProfile.objects.get(affiliate_code=code)
            loyalty_code = blapi_models.LoyaltyCode.objects.get(loyalty_code='Affiliate_Code')
            return [True, loyalty_code]
        except blapi_models.LoyaltyCode.DoesNotExist:
            return [False, None]
    return loyalty


def signup(request):
    if request.method == 'POST':

        # Validate reCAPTCHA
        recaptcha_url = 'https://www.google.com/recaptcha/api/siteverify'
        recaptcha_response = request.POST['g-recaptcha-response']
        recaptcha_values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }

        recaptcha = requests.post(recaptcha_url, data=recaptcha_values)
        recaptcha_result = recaptcha.json()
        recaptcha_success = recaptcha_result.get('success')
        if not recaptcha_success:
            messages.error(
                request, "Error: Please successfully complete reCaptcha.")
            return render(request, "account/signup.html")

        # Validate Loyalty Code
        code = request.POST['loyalty_code']
        if code:
            [loyalty_check, valid_code] = validateLoyaltyCode(request.POST['loyalty_code'])
            if not loyalty_check:
                messages.error(
                    request, "Invalid Loyalty Code!")
                return render(request, "account/signup.html")
        else: 
            valid_code = None

        # Make sure email and confirmation match if not do not run it through the signup_form
        if request.POST['email_address'] != request.POST['email_confirm']:
            messages.error(
                request, "Error: E-mail addresses do not match!")
            return render(request, "account/signup.html")

        # Create a form instance and populate it with data from the request:
        signup_form = SignUpForm(request.POST)

        # If the form is valid, then save it:
        if signup_form.is_valid():
            signup_form_clean = signup_form.cleaned_data

            subscriber_email = signup_form_clean["email_address"]

            # Make sure email address isn't re-used
            check_email = User.objects.filter(email=subscriber_email)
            if check_email.exists():
                messages.error(request, "Error: Email already exists!")
                return render(request, "account/signup.html", {'check_email_flag': True})

            # Create new user auth record, set random password
            logging.info("Beginning of Writing the new user into the auth user")
            user = User.objects.create_user(username=subscriber_email,
                                            email=subscriber_email,
                                            first_name=signup_form_clean["first_name"],
                                            last_name=signup_form_clean["last_name"],
                                            )
            password = User.objects.make_random_password(length=14)
            user.set_password(password)
            user.save()
            logging.info(
                "Writing the new user into the auth user , user detials are =", user)

            current_host = request.get_host()

            # Send Sign Up to Mixpanel
            if current_host == 'blocklight.io':
                mp = Mixpanel(settings.MIXPANEL_TOKEN)
                mp.track(user.id, 'Sign Up', {
                    'From': 'Blocklight',
                    'Loyalty': request.POST['loyalty_code'],
                    'Email': user.email
                })

            # Send Email Verification Info
            subject = 'Activate Your Blocklight Account'
            html_message = render_to_string('account/email/account_activation_email.html', {
                'user': user,
                'domain': current_host,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            message = strip_tags(html_message)
            send_mail(subject, message, None, [subscriber_email], True, html_message=html_message)

            # Grant Affiliate Bonus
            try:
                with transaction.atomic():
                    affiliate_check = UserProfile.objects.get(affiliate_code=code)
                    affiliate_check.affiliate_uses += 1
                    affiliate_check.save()
                    affiliate_user = User.objects.get(id=affiliate_check.user_id)
                    affiliate_user_tier = UserTier.objects.get(user=affiliate_user)
                    affiliate_user_tier.payments_start_date += 60
                    if affiliate_user_tier.valid_until:
                        affiliate_user_tier.valid_until += 60
                    affiliate_user_tier.save()
                    print('Affiliate Bonus Granted To ' + str(affiliate_user.email))
            except:
                print('No Affiliate Bonus Granted For This Signup.')

            # Create new user profile record
            u_id = User.objects.get(username=subscriber_email).id
            affiliate_code = generateAffiliateCode(u_id)
            user_profile = UserProfile.objects.create(user_id=u_id,
                                                      loyalty_code=valid_code,
                                                      affiliate_code=affiliate_code,
                                                      affiliate_uses=0,
                                                      accept_tos=signup_form_clean['accept_tos']
                                                      )
            user_profile.save()
            return redirect("signup_complete")
        else:
            return redirect("signup_failure")
    else:
        signup_url = request.get_full_path()
        signup_aff_code = signup_url.split('/signup/',1)[1]
        if signup_aff_code == '':
            return render(request, "account/signup.html", {'form': SignUp(), 'check_email_flag': False}) 
        else:
            return render(request, "account/signup_affiliate.html", {'form': SignUp(), 'check_email_flag': False, 'affiliate_code': signup_aff_code})


def signup_complete(request):
    return render(request, "account/signup_complete.html", {'django': 'django'})


def signup_failure(request):
    return render(request, "account/signup_failure.html", {'django': 'django'})


def mailchimp_signup(user):
     # Data to Mailchimp list subscription:
        client = MailChimp(settings.MAILCHIMP_API_KEY, settings.MAILCHIMP_EMAIL_ID)
            
        # Subscribing to the BL user mailing list
        try:
            client.lists.members.create(settings.SIGNUP_MAIL_LIST_ID, {
                'email_address': user.email,
                'status': 'subscribed',
                'merge_fields': {
                    'FNAME': user.first_name,
                    'LNAME': user.last_name,
                },
            })
        except:
            logging.error(
                'Mailchimp API failed to subscribe to SIGNUP LIST')

        # Subscribing to the newsletter mailing list
        try:
            client.lists.members.create(settings.NEWSLETTER_LIST_ID, {
                'email_address': user.email,
                'status': 'subscribed',
                'merge_fields': {
                    'FNAME': user.first_name,
                    'LNAME': user.last_name,
                },
            })
        except:
            logging.error(
                'Mailchimp API failed to subscribe to SIGNUP LIST')    


def activate(request, uidb64, token):
    try:
        # Grab user id from encoded url
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        user_profile = UserProfile.objects.get(user_id=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        user_profile = None

    if user and user_profile and account_activation_token.check_token(user, token) and not user_profile.email_verified:
        user.is_active = True
        user_profile.email_verified = True
        user.save()
        user_profile.save()
        login_activated(request, user)
        request.session['uid'] = uid

        # Create favorite dashboard for User
        blapi_models.BLDashboard(
            name='Favorite',
            user=user,
            is_favorite=True
        ).save()

        mailchimp_signup(user)
        return render(request, 'account/password_set.html')
    elif user and user_profile and account_activation_token.check_token(user, token):
        return redirect('/dashboards/integrations')
    else:
        return render(request, 'account/account_activation_invalid.html')


def initializeStripe(user):
    user_profile = UserProfile.objects.get(user_id=user.id)
    loyalty_code = user_profile.loyalty_code
    
    if loyalty_code:
        trial_period = loyalty_code.trial_period
    else:
        trial_period = 14

    today = date.today()
    UserTier(
        tier=Tier.objects.get(level_num=0),
        user=user,
        active=True,
        valid_since=today,
        valid_until=today + timedelta(trial_period),
    ).save()


def set_password(request):
    if request.method == 'POST':
        password_form = PasswordForm(request.POST)

        if password_form.is_valid():
            password_form_clean = password_form.cleaned_data

            # Check that password meets criteria
            if password_form_clean['password'] != password_form_clean['confirm_password']:
                messages.error(
                    request, "Error: Passwords do not match!")
                return render(request, "account/password_set.html")
            elif len(password_form_clean['password']) < 8:
                messages.error(
                    request, "Password must be at least 8 characters long.")
                return render(request, "account/password_set.html")
            elif not re.search(r"[\d]+",password_form_clean['password']):
                messages.error(
                    request, "Password must contain at least one number.")
                return render(request, "account/password_set.html")
            elif not any(ch.isupper() for ch in password_form_clean['password']):
                messages.error(
                    request, "Password must contain at least one upper case letter.")
                return render(request, "account/password_set.html")
            else:
                uid = request.session['uid']
                user = User.objects.get(pk=uid)
                user.set_password(password_form_clean['password'])
                user.save()

                # Start Free Trial
                initializeStripe(user)

                # Send Welcome Email
                subject = 'Welcome to Blocklight!'
                html_message = render_to_string('account/email/welcome_email.html', {
                    'user': user,
                })
                message = strip_tags(html_message)
                send_mail(subject, message, None, [user.email], True, html_message=html_message)

                # Send Account Verification to Mixpanel
                current_host = request.get_host()

                if current_host == 'blocklight.io':
                    mp = Mixpanel(settings.MIXPANEL_TOKEN)
                    mp.track(user.id, 'Verified Account', {
                        'Email': user.email
                    })

                perform_login(request, user, email_verification = EmailVerificationMethod.NONE)
            
            return redirect('/dashboards/integrations')

        else:
            return render(request, 'account/password_set.html')


############### Forgot Password ###############
def forgot_password(request):
    if request.method == 'POST':
        reset_form = PasswordResetForm(request.POST)
        if reset_form.is_valid():
            reset_form_clean = reset_form.cleaned_data
            check_user = User.objects.filter(email=reset_form_clean["email_address"])
            if check_user.exists():
                user = User.objects.get(email=reset_form_clean["email_address"])
                user_profile = UserProfile.objects.get(user_id=user.pk)
                user_profile.forgot_password = True
                user_profile.save()

                # Send Password Reset Email
                subject = 'Blocklight Password Reset'
                current_host = request.get_host()
                html_message = render_to_string('account/email/password_reset_email.html', {
                    'user': user,
                    'domain': current_host,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                message = strip_tags(html_message)
                send_mail(subject, message, None, [user.email], True, html_message=html_message)
                
        return redirect("forgot_password_complete")
    else:
        return render(request, "account/password_reset.html", {'form': SignUp()})

def forgot_password_complete(request):
    return render(request, "account/forgot_password_complete.html", {'django': 'django'})

def password_reset_key(request, uidb64, token):
    try:
        # Grab user id from encoded url
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        user_profile = UserProfile.objects.get(user_id=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token) and user_profile.email_verified is True and user_profile.forgot_password is True:
        request.session['uid'] = uid
        return render(request, 'account/new_password.html')
    elif user is not None and user_profile and account_activation_token.check_token(user, token):
        return redirect('/dashboards/integrations')
    else:
        return render(request, 'account/account_activation_invalid.html')

def new_password(request):
    if request.method == 'POST':
        password_form = PasswordForm(request.POST)

        if password_form.is_valid():
            password_form_clean = password_form.cleaned_data
            uid = request.session['uid']
            user = User.objects.get(pk=uid)

            # Check that password meets criteria
            # TODO: Use django's built-in password validators instead of own implementation
            if password_form_clean['password'] != password_form_clean['confirm_password']:
                messages.error(
                    request, "Error: Passwords do not match!")
                return render(request, "account/new_password.html")
            elif len(password_form_clean['password']) < 8:
                messages.error(
                    request, "Password must be at least 8 characters long.")
                return render(request, "account/new_password.html")
            elif not re.search(r"[\d]+",password_form_clean['password']):
                messages.error(
                    request, "Password must contain at least one number.")
                return render(request, "account/new_password.html")
            elif not any(ch.isupper() for ch in password_form_clean['password']):
                messages.error(
                    request, "Password must contain at least one upper case letter.")
                return render(request, "account/new_password.html")
            elif user.check_password(password_form_clean['password']):
                messages.error(
                    request, "Password cannot be the same as your previous password.")
                return render(request, "account/new_password.html")
            else:
                user.set_password(password_form_clean['password'])
                user.save()
                user_profile = UserProfile.objects.get(user_id=uid)
                user_profile.forgot_password = False
                user_profile.save()

            return redirect('/dashboards/integrations')

        else:
            return render(request, 'account/new_password.html')


def home(request):
    # if request.user.is_authenticated():
    #     # your logic here
    #     return redirect("/dashboards/integrations")  # or your url name

    # """ Default view for the root """
    print("------------------------------")
    print(request.user)
    print(request.user.__class__)
    return render(request, "layout/home.html", {'django': 'django', 'user': request.user})


@login_required
def profile(request):
    return render(request, "user/profile.html", {'django': 'django'})


def about(request):
    return render(request, "layout/home.html/#section-3", {'django': 'django'})


def tos(request):
    return render(request, "layout/tos.html", {'django': 'django'})


def blog(request):
    return render(request, "blogs/blog_list.html", {'django': 'django'})


def contact(request):
    return render(request, "layout/home.html/#section-11", {'django': 'django'})


def support(request):
    return render(request, "layout/home.html", {'django': 'django'})


def privacy(request):
    return render(request, "layout/privacy.html", {'django': 'django'})


def login_activated(request, user):
    return render(request, "account/login.html", {'django': 'django'})


def login(request):
    if request.user.is_authenticated():
        # your logic here
        print('it works')
        return redirect("/dashboards/integrations")  # or your url name

    return render(request, "account/login.html", {'django': 'django'})


def faq(request):
    return render(request, "layout/faq.html", {'django': 'django'})


def blog(request):
    return render(request, "layout/blog.html", {'django': 'django'})


def connections_redirect(request):
    return render(request, "socialaccount/connections_redirect.html", {'django': 'django'})


def roadmap(request):
    return render(request, "layout/roadmap.html", {'django': 'django'})


def bbm(request):
    return render(request, "layout/bbm.html", {'django': 'django'})


def about(request):
    return render(request, "layout/about.html", {'django': 'django'})


def use_cases(request):
    return render(request, "layout/use_cases.html", {'django': 'django'})


def bap(request):
    return render(request, "layout/bap.html", {'django': 'django'})
