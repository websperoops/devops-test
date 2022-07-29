from __future__ import print_function

from allauth.account.app_settings import EmailVerificationMethod
from allauth.account.utils import perform_login
from allauth.socialaccount.models import SocialApp, SocialToken, SocialLogin
from allauth.socialaccount.signals import social_account_added
from allauth.socialaccount.views import ConnectionsView
from ast import literal_eval
from avatar.models import Avatar
from blocklight import settings
from blocklight.commons import google_api_calls
from blocklight_api import models as blapi_models
from celery.result import AsyncResult
from csv import writer

from dashboards.forms import *
from dashboards.integrations.google.google_api import set_up_google_cred, query_google_account_summaries, \
    get_google_account_summaries
from dashboards.models import UserProfile, Tab, Integrations_ChartData, Integrations_FacebookInsights_Impressions, \
    Integrations_FacebookInsights_Views, Integrations_FacebookInsights_Engagements, \
    Integrations_FacebookInsights_Reactions, Integrations_FacebookInsights_Posts, \
    Integrations_FacebookInsights_Demographics, Integrations_InstagramInsights_Impressions, \
    Integrations_InstagramInsights_Reach, Integrations_InstagramInsights_Followers, \
    Integrations_MailChimp_ListStats, Integrations_ShipStation_Fulfillments, \
    Integrations_Shopify_Shop, Integrations_Shopify_Customer, Integrations_Shopify_Order, \
    Integrations_Shopify_Customer_Address, Integrations_Shopify_Abandoned_Checkouts, \
    Integrations_Shopify_Address, Integrations_Shopify_Abandoned_Checkout_Line_Items, \
    Integrations_Shopify_Refund, Integrations_Shopify_Refund_Line_Item, \
    Integrations_Shopify_Refund_Order_Adjustment, Integrations_Shopify_Line_Item, \
    Integrations_Shopify_Transaction, Integrations_Shopify_Shipping_Line, \
    Integrations_Shopify_Discount_Application, Integrations_Shopify_Discount_Code, \
    Integrations_Shopify_Fulfillment

from dashboards.sync import *
from dashboards.tasks import *
from dashboards.tasks import sync_users_integrations

from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, EmailMessage
from django.db import transaction
from django.db.models import Max
from django.forms.models import model_to_dict
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.html import strip_tags
from django.views.generic import DetailView, CreateView, DeleteView, View

from io import StringIO
from intuitlib.client import AuthClient
from json import dumps, loads, load

from layout.models import SignUp
from layout.views import mailchimp_signup, validateLoyaltyCode, initializeStripe, generateAffiliateCode

from mixpanel import Mixpanel
from os import mkdir, remove
import re
import requests
from user_tiers.models import UserTier


global DJANGO_HOST


if socket.gethostname().startswith('dev'):
    DJANGO_HOST = "development"
elif socket.gethostname().startswith('prod'):
    DJANGO_HOST = "production"
else:
    DJANGO_HOST = "localhost"

# Error Logging on DO Server
logger = logging.getLogger(__name__)

# Set widget (chart) size parameters
GRID_WIDTH = 12
WIDGET_WIDTH = 4
WIDGET_HEIGHT = 4


@login_required
def request_oauth_token(request):

    # Extract information from request
    code = request.GET['code']
    state_token = request.GET.get('state', None)
    realm_id = request.GET.get('realmId', None)

    user_iden = request.user.id

    app = SocialApp.objects.get(provider='quickbooks')

    current_host = request.get_host()

    # Get Refresh Token
    auth_client = AuthClient(
        client_id=app.client_id,
        client_secret=app.secret,
        environment='sandbox',
        redirect_uri='https://'+current_host+'/quickbooks/login/callback/',
        realm_id=realm_id
    )
    auth_client.get_bearer_token(code, realm_id=realm_id)

    # Store extra information in extra_data dictionary
    extra_data = {}
    extra_data["access_token"] = auth_client.access_token
    extra_data["realm_id"] = realm_id
    extra_data["state_token"] = state_token
    extra_data["refresh_token"] = auth_client.refresh_token
    extra_data["code"] = code

    account_info = SocialAccount(
        user_id=user_iden,
        provider='quickbooks',
        extra_data=extra_data
    )
    account_info.save()

    social_login = SocialLogin(
        account=account_info
    )

    social_account_added.send(
        request=request,
        sociallogin=social_login,
        sender=SocialLogin
    )

    return redirect('/dashboards/integrations')


# Send Abandoned Cart Email
def send_abandoned_cart_email(request):
    if request.method == 'POST':
        data = loads(request.body)

        subtotal = data['subtotal_price']
        tax = data['total_tax']
        shipping = data['shipping_price']
        total_line_items = data['total_line_items_price']
        total_price = data['total_price']
        discounts = data['total_discounts']
        url = data['abandoned_checkout_url']
        email = data['customer_ref']['email']

        # Line Items
        line_items = data['line_items']

        html_message = render_to_string('account/email/abandoned_cart_email.html', {
            'subtotal': subtotal,
            'tax': tax,
            'discounts': discounts,
            'url': url,
            'shipping': shipping,
            'total_price': total_price,
            'line_items': line_items,
        })

        to = email
        subject = 'Complete Your Checkout!'

        message = strip_tags(html_message)
        send_mail(subject, message, None, [
                  to], True, html_message=html_message)

        # Send Recovery to Mixpanel
        current_host = request.get_host()
        if current_host == 'blocklight.io':
            mp = Mixpanel(settings.MIXPANEL_TOKEN)
            mp.track(request.user.id, 'Abandoned Cart Recovery Sent', {
                'Url': url,
                'Email': request.user.email
            })

        return JsonResponse({'success': True})

    return HttpResponse('test')


# Reset default password
@login_required
def change_password(request):
    """
    To change the user password
    Uses CustomPasswordChangeForm to handle all error and success cases
    Args:
        request: GET - displays the password change form
                 POST - Changes the password
    Returns:
        Redirects to profile page if successful
        Redirects to change_password page with the errors displayed if failed

    """
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            # Update password
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('/dashboards/profile/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'dashboards/change_password.html', {
        'form': form
    })


# Supporting functions for POPULATING PAGES

# Determine user's theme color
def getThemeColor(user_iden):
    """
    Retrives theme color fof user based on User profile settings. Defaults to dark if none exist
    Args:
        user_iden: id of user

    Returns:
        Color (string)
    """
    try:
        theme_color = 'light' if UserProfile.objects.get(
            user_id=user_iden).light_theme else 'dark'
    except:
        theme_color = 'dark'
    return theme_color


# TODO: Don't traverse all rows in all fb tables just to get account names
#       Maybe store this info somewhere separately
def get_unique_account_names(user_iden, tables):

    if not tables:
        return []

    unique_account_names_by_tables = list(map(
        lambda a: a.objects.filter(
            user_iden=user_iden,
            account_name__isnull=False
        ).values_list(
            'account_name',
            flat=True
        ).distinct(),
        tables
    ))

    # Note: the union needs to be 'flat' (not nested) in mysql5.7. So we cannot use 'reduce' function here
    unique_account_names = list(filter(
        lambda a: a is not None,
        unique_account_names_by_tables[0].union(
            *unique_account_names_by_tables[1:]).distinct()
        if (len(tables) > 1) else unique_account_names_by_tables[1].distinct()
    ))

    return unique_account_names


# Determine which Facebook accounts should be displayed as an option for several default charts
def checkFacebookAccountAvailability(user_iden):

    fb_tables = (
        Integrations_FacebookInsights_Impressions,
        Integrations_FacebookInsights_Views,
        Integrations_FacebookInsights_Engagements,
        Integrations_FacebookInsights_Reactions,
        Integrations_FacebookInsights_Posts,
        Integrations_FacebookInsights_Demographics,
    )

    return get_unique_account_names(user_iden, fb_tables)


# Determine which Instagram accounts should be displayed as an option for several default charts
def checkInstagramAccountAvailability(user_iden):

    ig_tables = (
        Integrations_InstagramInsights_Impressions,
        Integrations_InstagramInsights_Reach,
        Integrations_InstagramInsights_Followers
    )

    return get_unique_account_names(user_iden, ig_tables)


# Determine which integrations the user has data for
def checkIntegrationsData(user_iden):
    all_syncs = list(Integrations_UserSettings.objects.filter(user_iden=user_iden).values_list('integration_name',
                                                                                               flat=True).distinct())
    response = [x for x in all_syncs if not '_celery' in x]
    logger.debug(response)
    all_syncs = list(SocialAccount.objects.filter(
        user_id=user_iden).values_list('provider', flat=True).distinct())
    response = list(set(response + all_syncs))
    return response


# Check where a new chart can be placed on a dashboard
def checkChartPlacement(existing_charts):
    # Get all chart positions
    all_positions = list(existing_charts.values_list(
        'x_position', 'y_position', 'width', 'height'))
    logger.debug('\nall_positions:')
    logger.debug(all_positions)
    # Only if other charts on dash yet
    if len(all_positions) > 0:
        # Find most bottom y_position
        max_y_pos = max(all_positions, key=lambda pos: pos[1])
        max_y = max_y_pos[1]
        # Find all charts with max y position, then find furthest right position from the group
        all_max_y_positions = [pos for pos in all_positions if pos[1] == max_y]
        max_right_pos = max(all_max_y_positions,
                            key=lambda pos: pos[0] + pos[2])
        max_right = max_right_pos[0] + max_right_pos[2]
        max_down_pos = max(all_max_y_positions,
                           key=lambda pos: pos[1] + pos[3])
        max_down = max_down_pos[1] + max_down_pos[3]
        # Check if there's space to put a chart on the same row to the right
        if GRID_WIDTH - max_right >= WIDGET_WIDTH:
            space_right = True
        else:
            space_right = False
        # Find all charts that extend past the max y position, if any exist will just place on next line
        all_overlap_y_positions = [pos for pos in all_positions if
                                   pos[1] + pos[3] > max_y and not pos in all_max_y_positions]
        if len(all_overlap_y_positions) > 0:
            next_line = True
        else:
            next_line = False
        # Place chart
        if space_right and not next_line:
            new_x, new_y = max_right, max_y
        else:
            new_x, new_y = 0, max_down
    # Else this is the first chart to be added
    else:
        new_x, new_y = 0, 0
    # Return
    return (new_x, new_y)


# Quick check to see if facebook or instagram are in integration string
def checkFBInsta(integration):
    is_fb = 'facebook' in integration.split('_')
    is_instagram = 'instagram' in integration.split('_')
    return (is_fb or is_instagram)


def checkMailchimp(integration):
    is_mailchimp = 'mailchimp' in integration.split('_')
    return (is_mailchimp)


# To add default charts to widget DB table
def addDefaultWidgets(default_chart_objects, available_integrations, user_iden):
    # First check to see how many rows are in DB table for default charts
    existing_charts = list(
        Widget.objects.filter(user_iden=user_iden, is_blocklight_default=True, is_homepage_summary=False).values_list(
            'metric', flat=True))
    num_existing = len(existing_charts)
    # Check to see how many default charts should be in DB table
    logger.debug(available_integrations)
    available_charts = [(metric, chart_object) for metric, chart_object in
                        default_chart_objects.items() if
                        set(chart_object['integration'].split('_')).issubset(available_integrations)]
    num_available = len(available_charts)
    # If the numbers don't match
    if not num_existing == num_available:
        # Determine which default chart widgets need to be added
        charts_to_add = [(metric, chart_object) for metric, chart_object in available_charts if
                         metric not in existing_charts]
        # Loop through default chart objects
        for metric, chart_object in charts_to_add:
            # Set title
            title = 'default_%s_%s' % (
                chart_object['integration'], chart_object['metric'])
            # Determine which default dashboard the chart belongs to
            dash_slug_start = slugify(chart_object['integration']) if not '_' in chart_object[
                'integration'] else slugify('combined')
            dash_slug = dash_slug_start + '_' + str(user_iden) + '_0'

            # Eric changed this (might change back)
            # Determine x and y position based on other charts already on the dashboard
            # others_on_dash = Widget.objects.filter(user_iden=user_iden, dashboard=dash_slug, is_published=True)
            # x_position, y_position = checkChartPlacement(others_on_dash)
            x_position, y_position = None, None

            # Eric also added this
            # Get time option list
            # if checkFBInsta(chart_object['integration']):
            #     time_options = facebook_time
            if (chart_object['metric'], chart_object['integration']) in only_all_time_metrics:
                time_options = only_all_time
            else:
                time_options = all_times

            # Get mailchimp list
            if checkMailchimp(chart_object['integration']) and (
                    chart_object['metric'], chart_object['integration']) in mailchimp_list_metrics:
                try:
                    option = list(
                        Integrations_MailChimp_ListStats.objects.filter(user_iden=user_iden).values_list('list_name',
                                                                                                         flat=True))
                    chart_object['supported_options'] = {'value': option}
                    if chart_object['current_option'] == {'value': 'ListName'}:
                        chart_object['current_option']['value'] = option[0]
                except:
                    logger.debug(
                        'Mailchimp options data not stored in the database yet')

            # Choose time option
            if not chart_object['current_chart_type'] == 'USA_Map':
                # current_time_period = time_options[0]
                current_time_period = time_options[
                    -1]  # Temporary - starting with longest time period to try to speed things up
            else:
                current_time_period = time_options[-1]

            # Determine unique chart slug (count number of other records with same title to determine slug)
            num_same_titles = str(Widget.objects.filter(
                user_iden=user_iden, title=title).count())
            widget_slug = slugify(title) + '_' + \
                str(user_iden) + '_' + num_same_titles
            # Add record
            _in, created = Widget.objects.get_or_create(user_iden=user_iden, is_blocklight_default=True,
                                                        is_blocklight_generic=False,
                                                        is_user_added=False, is_published=True,
                                                        is_homepage_summary=False, metric=chart_object['metric'],
                                                        display_name=chart_object['display_name'],
                                                        integration=chart_object['integration'],
                                                        supported_options=str(
                                                            chart_object['supported_options']),
                                                        current_option=str(
                                                            chart_object['current_option']),
                                                        supported_chart_types=str(
                                                            chart_object['supported_chart_types']),
                                                        current_chart_type=chart_object['current_chart_type'],
                                                        supported_time_periods=str(
                                                            chart_object['supported_time_periods']),
                                                        current_time_period=current_time_period,
                                                        dashboard=dash_slug, x_position=x_position,
                                                        y_position=y_position, width=WIDGET_WIDTH, height=WIDGET_HEIGHT,
                                                        title=title, slug=widget_slug)
            # If it's a single metric widget, it's eligible to be shown on the homepage, so need to add 2 records
            priority = ['orders_single_metric',
                        'sales_single_metric',
                        'google_total_website_views',
                        'shipment_total_single_metric',
                        'page_engagement',
                        'profile_followers',
                        'overall_subscribes_single_metric',
                        'total_website_hits',
                        'repeat_customer_rate',
                        'average_website_bounce_rate',
                        'refund_count_single_metric',
                        'overall_unsubscribes_single_metric',
                        'page_reach',
                        'profile_reaches',
                        'shipment_per_order_single_metric',
                        'average_website_session_duration',
                        'page_impressions',
                        'page_views',
                        'profile_impressions',
                        'profile_clicks']
            if chart_object['metric'] in priority:
                # Generate dash and widget slugs
                dash_slug = 'blocklight_homepage_summary_' + \
                    str(user_iden) + '_2018'
                widget_slug = slugify(title) + '_homepage_' + \
                    str(user_iden) + '_' + num_same_titles
                # Add record
                _in, created = Widget.objects.get_or_create(user_iden=user_iden, is_blocklight_default=True,
                                                            is_blocklight_generic=False,
                                                            is_user_added=False, is_published=False,
                                                            is_homepage_summary=True, metric=chart_object['metric'],
                                                            display_name=chart_object['display_name'],
                                                            integration=chart_object['integration'],
                                                            supported_options=str(
                                                                chart_object['supported_options']),
                                                            current_option=str(
                                                                chart_object['current_option']),
                                                            supported_chart_types=str(
                                                                ['Single_Metric']),
                                                            current_chart_type='Single_Metric',
                                                            supported_time_periods=str(
                                                                chart_object['supported_time_periods']),
                                                            current_time_period=current_time_period,
                                                            dashboard=dash_slug, x_position=0, y_position=0, width=0,
                                                            height=0, title=title, slug=widget_slug)


# To add default dashboards to DB table
def addFavoritesDashboard(user_iden):
    does_exist = Dashboard.objects.filter(user_id=user_iden, title="Favorites")
    if not does_exist.exists():
        dash_slug = "Favorites_" + str(user_iden)
        index = list(
            Dashboard.objects.filter(user_id=user_iden, is_blocklight_stock=True).values_list('slug', flat=True))
        i = len(index)
        _in, created = Dashboard.objects.get_or_create(user_id=user_iden, title="Favorites", slug=dash_slug,
                                                       is_published=True, is_blocklight_stock=True, current_dashboard=0,
                                                       tab_index=i)


def addDefaultDashboards(user_iden):
    # Check if associated dashboards need to be added
    required_dash = list(
        Widget.objects.filter(user_iden=user_iden, is_blocklight_default=True, is_homepage_summary=False).values_list(
            'dashboard', flat=True).distinct())
    num_required = len(required_dash) + 1
    existing_dash = list(
        Dashboard.objects.filter(user_id=user_iden, is_blocklight_stock=True).values_list('slug', flat=True))
    num_existing = len(existing_dash)
    # If the numbers don't match
    if not num_existing == num_required:
        # Determine which dashboards we're missing
        missing_dash = [
            dash_slug for dash_slug in required_dash if not dash_slug in existing_dash]
        # Loop through and add required additional dashboards

        args = Dashboard.objects.filter(user_id=user_iden)

        for i, dash_slug in enumerate(missing_dash):
            # Get title from slug
            title = '_'.join(dash_slug.split('_')[:-2]).title()
            # Check if there is already a current dashboard, if so don't change
            current_exists = (Dashboard.objects.filter(
                user_id=user_iden, current_dashboard=True).count() > 0)

            max = args.aggregate(Max('tab_index'))
            if max['tab_index__max'] == None:
                max['tab_index__max'] = -1

            # Create new record
            _in, created = Dashboard.objects.get_or_create(user_id=user_iden, title=title, slug=dash_slug,
                                                           is_published=True,
                                                           is_blocklight_stock=True,
                                                           current_dashboard=(
                                                               i == 0 and not current_exists),
                                                           tab_index=max['tab_index__max'] + 1)
    addFavoritesDashboard(user_iden)


# Building summary metric for the homepage
def build_summary_metric(user_iden, record, mailchimp_lists, fb_accounts, insta_accounts, x_pos):
    # Build chart object
    chart_object = {
        'dashboard': record['dashboard'],
        'id': record['slug'],
        'integration': record['integration'],
        'widget_header': ' & '.join(record['integration'].split('_')).title(),
        'metric': record['metric'],
        'supported_options': literal_eval(record['supported_options']),
        'current_option': literal_eval(record['current_option']),
        'supported_time_periods': literal_eval(record['supported_time_periods']),
        'current_time_period': record['current_time_period']
    }
    # Several MailChimp metrics requires some extra work
    if record['metric'] in ['list_subscribes_vs_unsubscribes', 'list_subscribes_single_metric',
                            'list_unsubscribes_single_metric']:
        chart_object['supported_options']['value'] = mailchimp_lists
        if not chart_object['current_option']['value'] in mailchimp_lists:
            chart_object['current_option']['value'] = mailchimp_lists[0]
    # All Facebook and Instagram metrics require some extra work
    if chart_object['supported_options'] and chart_object['current_option']:
        if 'account' in list(chart_object['supported_options'].keys()) and 'account' in list(
                chart_object['current_option'].keys()):
            if record['integration'] == 'facebook':
                if len(fb_accounts) > 0:
                    chart_object['supported_options']['account'] = fb_accounts
                    if not chart_object['current_option']['account'] in fb_accounts:
                        chart_object['current_option']['account'] = fb_accounts[0]
                else:
                    chart_object['supported_options'].pop('account', None)
                    chart_object['current_option'].pop('account', None)
            if record['integration'] == 'instagram':
                if len(insta_accounts) > 0:
                    chart_object['supported_options']['account'] = insta_accounts
                    if not chart_object['current_option']['account'] in insta_accounts:
                        chart_object['current_option']['account'] = insta_accounts[0]
                else:
                    chart_object['supported_options'].pop('account', None)
                    chart_object['current_option'].pop('account', None)
        # Make sure supported_options and current_option are okay
        if len(list(chart_object['supported_options'].keys())) == 0:
            chart_object['supported_options'] = None
        if len(list(chart_object['current_option'].keys())) == 0:
            chart_object['current_option'] = None
    # Mark record as a summary metric
    current_metric = Widget.objects.get(
        user_iden=user_iden, slug=record['slug'])
    current_metric.is_published = True
    current_metric.x_position = x_pos
    current_metric.save()
    # Return chart object
    return chart_object


# Get all appropriate metric definitions for specified dashboard
def build_chartlist(user_iden, which_dashboard, metric_availability, all_lists, all_facebook_accounts,
                    all_instagram_accounts):
    # Build list of metric names
    # Homepage and Favorites dashboard
    if which_dashboard.split("_", 1)[0] in ['Favorites', 'Homepage']:
        metric_objects = Widget.objects.filter(
            user_iden=user_iden, is_published=True, is_favorite=True)
        # Else normal dashboard
    else:
        metric_objects = Widget.objects.filter(
            dashboard=which_dashboard, user_iden=user_iden, is_published=True)

    # Build chart object with all info necessary to display metrics
    # Loop through all appropriate records from DB table to build chartlist and new chart structure
    chartlist = []
    for record in list(metric_objects.values()):

        # Check if chart should be added, if so continue
        # try:
        if (metric_availability[record['metric']]):

            # Build chart object
            chart_object = {
                'id': record['slug'],
                'num_id': record['id'],
                'dashboard': record['dashboard'],
                'integration': record['integration'],
                'widget_header': ' & '.join(record['integration'].split('_')).title(),
                'metric': record['metric'],
                'supported_options': literal_eval(record['supported_options']),
                'current_option': literal_eval(record['current_option']),
                'supported_chart_types': literal_eval(record['supported_chart_types']),
                'current_chart_type': record['current_chart_type'],
                'supported_time_periods': literal_eval(record['supported_time_periods']),
                'current_time_period': record['current_time_period'],
                'positions': [str(record['x_position']), str(record['y_position']), str(record['width']),
                              str(record['height'])],
                'data_series': None
            }

            # Check if user has provided feedback on the chart (used to color thumbs up and thumbs down buttons)
            try:
                chart_feedback = Feedback.objects.get(user_iden=user_iden, topic=record['slug'],
                                                      feedback_type='metric_specific').description
            except:
                chart_feedback = 'none'
            chart_object['feedback'] = chart_feedback

            # Several metrics requires some extra work
            if record['metric'] in ['list_subscribes_vs_unsubscribes', 'list_subscribes_single_metric',
                                    'list_unsubscribes_single_metric']:
                chart_object['supported_options']['value'] = all_lists
                if not chart_object['current_option']['value'] in all_lists:
                    chart_object['current_option']['value'] = all_lists[0]

            # All Facebook and Instagram metrics require some extra work
            if chart_object['supported_options'] and chart_object['current_option']:
                if 'account' in list(chart_object['supported_options'].keys()) and 'account' in list(
                        chart_object['current_option'].keys()):
                    if record['integration'] == 'facebook':
                        if len(all_facebook_accounts) > 0:
                            chart_object['supported_options']['account'] = all_facebook_accounts
                            if not chart_object['current_option']['account'] in all_facebook_accounts:
                                chart_object['current_option']['account'] = all_facebook_accounts[0]
                        else:
                            chart_object['supported_options'].pop(
                                'account', None)
                            chart_object['current_option'].pop('account', None)
                    if record['integration'] == 'instagram':
                        if len(all_instagram_accounts) > 0:
                            chart_object['supported_options']['account'] = all_instagram_accounts
                            if not chart_object['current_option']['account'] in all_instagram_accounts:
                                chart_object['current_option']['account'] = all_instagram_accounts[0]
                        else:
                            chart_object['supported_options'].pop(
                                'account', None)
                            chart_object['current_option'].pop('account', None)
                # Make sure supported_options and current_option are okay
                if len(list(chart_object['supported_options'].keys())) == 0:
                    chart_object['supported_options'] = None
                if len(list(chart_object['current_option'].keys())) == 0:
                    chart_object['current_option'] = None

            # NEW - Get the data for the chart
            params = {'user_iden': user_iden,
                      'chart_id': chart_object['id'],
                      'integration': chart_object['integration'],
                      'metric': chart_object['metric'],
                      'option': str(chart_object['current_option']),
                      'chart_type': chart_object['current_chart_type'],
                      'time_period': chart_object['current_time_period'],
                      'dashboard_slug': chart_object['dashboard'],
                      'what_changed': 'current_chart_type'}
            if not params['chart_type'] == 'USA_Map':
                data_series = chart_data_initial(params)
            else:
                data_series = {
                    'series': []}  # Temporary - USA_Map charts are taking forever to load, so disabling for now

            # If the data series is empty, see if we can try a longer time period
            # Temporary - disabling for now to try to speed things up
            '''
            exhausted_all_times = False
            if checkFBInsta(
                chart_object['integration']): time_options = facebook_time
            elif (params['metric'], params['integration']) in only_all_time_metrics:
                time_options = only_all_time
            else: time_options = all_times
            while len(data_series['series']) == 0 and not exhausted_all_times:
                print('\nTrying a longer time period')
                print('Old: %s' % (params['time_period']))
                current_time_period = params['time_period']
                next_index = time_options.index(current_time_period) + 1
                if next_index < len(time_options):
                    print(next_index, len(time_options))
                    params['time_period'] = time_options[next_index]
                    print('Got here!')
                    data_series = chart_data_initial(params)
                else:
                    exhausted_all_times = True
                print('New: %s' % (params['time_period']))
            if exhausted_all_times: print('Exhausted all times!!')
            '''

            # If the data series is non-empty, add chart
            if len(data_series['series']) > 0:
                logger.debug('CHART HAS DATA SO ADDING IT')

                # If the time period was changed successfully, then need to update DB record
                if not chart_object['current_time_period'] == params['time_period']:
                    logger.debug('Found a new time period that works!!')
                    chart_object['current_time_period'] = params['time_period']
                    try:
                        record = Widget.objects.get(
                            user_iden=user_iden, slug=record['slug'], is_homepage_summary=False)
                        record.current_time_period = chart_object['current_time_period']
                        record.save()
                    except:
                        pass
                    try:
                        record = Widget.objects.get(
                            user_iden=user_iden, slug=record['slug'], is_homepage_summary=True)
                        record.current_time_period = chart_object['current_time_period']
                        record.save()
                    except:
                        pass

                # Add
                chart_object['data_series'] = dumps(data_series)

                # If necessary, update chart placement
                if not which_dashboard == 'Homepage':
                    if record['x_position'] == None or record['y_position'] == None:
                        logger.debug('Updating chart position')
                        others_on_dash = Widget.objects.filter(user_iden=user_iden, dashboard=which_dashboard,
                                                               is_published=True).exclude(x_position=None,
                                                                                          y_position=None)
                        logger.debug('Num widgets on dash: %d' %
                                     others_on_dash.count())
                        x_position, y_position = checkChartPlacement(
                            others_on_dash)
                        chart_object['positions'][0], chart_object['positions'][1] = str(
                            x_position), str(y_position)
                        # Update db record
                        try:
                            record = Widget.objects.get(user_iden=user_iden, slug=record['slug'],
                                                        is_homepage_summary=False)
                            record.x_position = int(x_position)
                            record.y_position = int(y_position)
                            record.save()
                            logger.debug('Updated chart position!')
                        except:
                            logger.debug('Failed to update chart position.')

                # Append to chart list
                # print("ADDING DEFAULT CHART: %s at %s" % (record['metric'], str(chart_object['positions'])))
                chartlist.append(chart_object)
            else:
                logger.debug("[NO DATA] NOT ADDING DEFAULT CHART: %s" %
                             (record['metric']))

        # Else metric isn't available
        else:
            logger.debug("NOT ADDING DEFAULT CHART: %s" % record['metric'])
        # except Exception as e:
        #    print('Error loading chart')
        #    exc_type, exc_obj, exc_tb = sys.exc_info()
        #    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        #    print(exc_type, fname, exc_tb.tb_lineno)
        #    print(e)

    return chartlist


# Supporting functions for INTERACTING WITH PAGES

# When adding integration, check to see if it exists in another blockligh account
@login_required
def checkIfIntegrationExists(user_iden, integration_id, integration_name):
    check_if_exists = SocialAccount.objects.filter(
        provider=integration_name, user_id=user_iden, uid=integration_id)
    if check_if_exists.exists():
        return redirect("/dashboards/integrations")


# To delete widgets, dashboards, syncs, user data (when an integration is deleted)
def removeDataOnItegrationDelete(user_iden, integration, account_id=None):
    # Keep track of which deletes fail
    failures = []
    # Widgets and dashboards
    # Get names of dashboards that widgets are on
    all_dashboards = Widget.objects.filter(user_iden=user_iden, integration__icontains=integration).values_list(
        'dashboard', flat=True)
    # For each dashboard, check if all widgets on that dashboard use the integration
    delete_dashboards = []
    for dash in all_dashboards:
        # Get all widgets on dash
        dash_integrations = Widget.objects.filter(user_iden=user_iden, dashboard=dash).values_list('integration',
                                                                                                   flat=True)
        # If all widgets use the integration that is being deleted, then dash should be deleted
        if all(integration in x for x in dash_integrations):
            delete_dashboards.append(dash)
    # Convert list to set to remove duplicates
    delete_dashboards = list(set(delete_dashboards))

    # Reduce the tab_index for all other dashboard.
    # TODO: What if the favorites dashoard is removed?
    for dashboard in delete_dashboards:
        if Dashboard.objects.filter(user_id=user_iden, slug=dashboard, is_published=True).exists():

            related_dash = Dashboard.objects.get(
                user_id=user_iden, slug=dashboard, is_published=True)
            remaining_dash = Dashboard.objects.filter(user_id=user_iden, is_published=True,
                                                      tab_index__gt=related_dash.tab_index)

            # IF current dashboard is removed try making the index 0 to the current dashboard
            related_dash.tab_index = -1
            related_dash.save()
            if remaining_dash.exists():
                for board in remaining_dash:
                    board.tab_index = board.tab_index - 1
                    board.save()
                if related_dash.current_dashboard == 1:
                    new_current_dashboard = Dashboard.objects.get(
                        user_id=user_iden, tab_index=0, is_published=True)
                    new_current_dashboard.current_dashboard == 1
                    new_current_dashboard.save()

    # Delete widgets
    try:
        Widget.objects.filter(user_iden=user_iden,
                              integration__icontains=integration).delete()
    except:
        failures.append('Widgets')
    # Delete dashboards
    try:
        Dashboard.objects.filter(
            user_id=user_iden, slug__in=delete_dashboards).delete()
    except:
        failures.append('Dashboards')
    # Syncs and settings
    try:
        Integrations_User_LastSync.objects.filter(
            user_iden=user_iden, integration_name__icontains=integration).delete()
    except:
        failures.append('Syncs')
    try:
        num_social_accounts = SocialAccount.objects.filter(
            provider=integration, user_id=user_iden).count()

        if not account_id or num_social_accounts == 1:
            dashboards = blapi_models.BLDashboard.objects.filter(
                user_id=user_iden
            )
            for db in dashboards:
                charts = db.charts.all()
                for chart in charts:
                    metric = chart.metric
                    integrations = metric.integrations.all()
                    integration_names_in_metric = set(
                        map(lambda int: int.name, integrations))
                    if integration in integration_names_in_metric:
                        metric = chart.metric
                        metric.delete()

            integrations = blapi_models.Integration.objects.filter(
                name=integration,
                user_id=user_iden
            )
            integrations.delete()
            Integrations_UserSettings.objects.filter(
                user_iden=user_iden, integration_name=integration).delete()
            blapi_models.BLDashboard.objects.filter(
                account___provider=integration
            ).account = None

    except Exception as e:
        print(e)
        failures.append('Settings')
    # Billing
    if integration == 'shopify':
        try:
            pass
            # BlocklightBilling_Recurring_Shopify.objects.filter(user_account=user_iden).delete()
        except:
            failures.append('Billing')
    # Social Account (everything except Shipstation)
    if not integration == 'shipstation':
        try:
            if not account_id:
                account = SocialAccount.objects.filter(
                    user_id=user_iden, provider=integration).first()
                account.delete()
            else:
                account = SocialAccount.objects.filter(
                    user_id=user_iden, provider=integration, id=account_id).first()
                account.delete()

        except Exception as e:
            print(e)
            failures.append('Social Account')
    # User data (only Shipstation)
    else:
        try:
            BasicAuthRecords.objects.filter(
                user_iden=user_iden, integration_name=integration).delete()
            Integrations_ShipStation_Shipments.objects.filter(
                user_iden=user_iden).delete()
            Integrations_ShipStation_OrderItems.objects.filter(
                user_iden=user_iden).delete()
            Integrations_ShipStation_Orders.objects.filter(
                user_iden=user_iden).delete()
            Integrations_ShipStation_Tags.objects.filter(
                user_iden=user_iden).delete()
            Integrations_ShipStation_Warehouses.objects.filter(
                user_iden=user_iden).delete()
            Integrations_ShipStation_Fulfillments.objects.filter(
                user_iden=user_iden).delete()
        except:
            failures.append('Social Account')

    Integrations_User_LastSync.objects.filter(
        user_iden=user_iden, integration_name=integration).delete()

    # Return failures
    return failures


# TODO: Get rid of this function during views refactor
def getIntegrationName(url_is, user_iden):
    """
    Given a URL that contains an integration name, returns the integration name, the sync task function for that integration,
    and the number of sync tasks for that integration
    Args:
        url_is: a URL (string value)
        user_iden: id of user who requested the url

    Returns:

        A tuple of integration name (string), task (a celery task function) and tcount (int)

    """
    task = 'None'
    integration_name = 'combined'
    tcount = 0
    # if 'shopify' in url_is:
    #     integration_name = 'shopify'
    #     task = initialize_shopify_syncworker_task
    #     tcount = SocialAccount.objects.filter(provider='shopify', user_id=user_iden).count()
    #     # tcount = BlocklightBilling_Recurring_Shopify.objects.filter(user_account=user_iden).count()
    # if 'mailchimp' in url_is:
    #     integration_name = 'mailchimp'
    #     task = initialize_mailchimp_syncworker_task
    #     tcount = SocialAccount.objects.filter(provider='mailchimp', user_id=user_iden).count()
    # if 'facebook' in url_is:
    #     integration_name = 'facebook'
    #     task = initialize_instagramfacebook_syncworker_task
    #     tcount = SocialAccount.objects.filter(provider='facebook', user_id=user_iden).count()
    # if 'instagram' in url_is:
    #     integration_name = 'instagram'
    #     task = initialize_instagramfacebook_syncworker_task
    #     tcount = SocialAccount.objects.filter(provider='instagram', user_id=user_iden).count()
    # if 'shipstation' in url_is:
    #     integration_name = 'shipstation'
    #     task = initialize_shipstation_syncworker_task
    #     tcount = BasicAuthRecords.objects.filter(integration_name='shipstation', user_iden=user_iden).count()
    # if 'google' in url_is:
    #     integration_name = 'google'
    #     task = initialize_google_syncworker_task
    #     tcount = SocialAccount.objects.filter(provider='google', user_id=user_iden).count()

    return (integration_name, task, tcount)


@login_required
def profile(request):
    """
    Displays the data on the profile page.
    Modifies the data in database if the user edits it in the front end.
    Args:
        request: GET or POST

    Returns:
        for GET request, renders the profile page with default values.
        for POST request, updates the database and the renders the profile page with edited values

    """
    profile = UserProfile.objects.get(user=request.user)
    if not profile.affiliate_code:
        affiliate_code = generateAffiliateCode(request.user.id)
        profile.affiliate_code = affiliate_code
        profile.affiliate_uses = 0
        profile.save()

    return render(request, "dashboards/profile.html")


def save_profile_completion_status(user_profile):
    '''
    If "has completed profile" is not True, cycles through users profile information.  
    If user has completed 70% of their profile, sets "has completed profile" to True.
    This is part of the onboading checklist process.
    TODO: Move this into profile page so check only runs when profile is updated.
    '''
    if not user_profile.has_completed_profile:
        profile_completion_percent = 70
        profile_dict = model_to_dict(user_profile)
        completed_items_required = (
            (1-(profile_completion_percent/100))*len(profile_dict))
        count = 0
        for profile_key, profile_obj in profile_dict.items():
            if profile_obj is None:
                count += 1
        if count < completed_items_required:
            user_profile.has_completed_profile = True
            user_profile.save()


# HOMEPAGE
@login_required
def homepage(request):
    user = request.user
    user_iden = request.user.id
    user_profile = UserProfile.objects.get(user_id=user_iden)
    save_profile_completion_status(user_profile)

    # Setup and re-directs
    check_these = Integrations_UserSettings.objects.filter(user_iden=user_iden)
    for row in check_these:
        integration_name = row.integration_name
        should_sync = checkLastSync(user_iden, integration_name, 2)[
            'should_sync']

    '''
    Re-direct checks-
    Determine if any integrations have been added, if not re-direct to integrations page
    '''
    any_integrations_added = (
        SocialAccount.objects.filter(user_id=user_iden).count() > 0)
    any_integrations_added = (
        (any_integrations_added + BasicAuthRecords.objects.filter(user_iden=user_iden).count()) > 0)
    if not any_integrations_added:
        return redirect("/dashboards/integrations")

    if user.first_name == 'shopify_signup':
        return redirect('/dashboards/shopify_signup')

    # If only 1 account has been added and it's still initializing (syncing) re-direct to sync page
    other_choices = Dashboard.objects.filter(
        user_id=user_iden, is_published=True).only('title')
    syncing = Integrations_User_LastSync.objects.filter(user_iden=user_iden, sync_is_active=True,
                                                        initialize=True).only('integration_name')
    logger.debug(('testing1 = ', other_choices, syncing))
    final_choices = []
    if syncing.count() > 0:

        for choice in other_choices:

            if choice not in syncing:
                final_choices.append(choice)
        if len(final_choices) == 0:
            return redirect("/dashboards/sync")
    return render(request, "dashboards/homepage.html")


# DASH (re-directs to correct dashboard tab)
@login_required
def dash(request):
    # Isolate info from request
    user = request.user
    user_iden = request.user.id
    check_these = Integrations_UserSettings.objects.filter(user_iden=user_iden)
    for row in check_these:
        integration_name = row.integration_name
        should_sync = checkLastSync(user_iden, integration_name, 2)

    # Check if user has an avatar, if not set default avatar
    avatar_count = Avatar.objects.filter(user_id=user_iden).count()
    if avatar_count == 0:
        filename = 'avatars/master.png'
        model_entry, created = Avatar.objects.get_or_create(
            user_id=user_iden, primary=True)
        if created:
            model_entry.avatar = filename
            model_entry.save()

    # Re-direct checks
    # Determine if any integrations have been added, if not re-direct to integrations page
    any_integrations_added = (
        SocialAccount.objects.filter(user_id=user_iden).count() > 0)
    any_integrations_added = (
        (any_integrations_added + BasicAuthRecords.objects.filter(user_iden=user_iden).count()) > 0)
    if not any_integrations_added:
        return redirect("/dashboards/integrations")

    # If only 1 account has been added and it's still initializing (syncing) re-direct to sync page

    other_choices = Dashboard.objects.filter(
        user_id=user_iden, is_published=True).only('title')
    syncing = Integrations_User_LastSync.objects.filter(user_iden=user_iden, sync_is_active=True,
                                                        initialize=True).only('integration_name')
    logger.debug(('testing1 = ', other_choices, syncing))
    final_choices = []
    if syncing.count() > 0:

        for choice in other_choices:

            if choice not in syncing:
                final_choices.append(choice)
        if len(final_choices) == 0:
            return redirect("/dashboards/sync")


    # Dashboard / chart setup
    # [1] Check to see which integrations the user has data for
    # [2] Add default blocklight chart widgets to DB, if needed
    # [3] Add default dashboards for default chart widgets, if needed
    available_integrations = checkIntegrationsData(user_iden)
    logger.debug(available_integrations)
    addDefaultWidgets(default_blocklight_chart_objects,
                      available_integrations, user_iden)
    addDefaultDashboards(user_iden)

    # Figure out which dashboard is in first index, then re-direct to /dashboards/{{ dashboard.slug }}/view/
    try:
        first_dashboard_id = Dashboard.objects.filter(
            user_id=user_iden, tab_index=0, is_published=True)[0].id

        new_url = "/dashboards/" + str(first_dashboard_id) + "/view"
    except Exception as e:
        available_integrations = checkIntegrationsData(user_iden)
        ct = Dashboard.objects.filter(
            user_id=user_iden, tab_index=0, is_published=True).count()

        if ct > 1:
            Dashboard.objects.filter(user_id=user_iden, tab_index=0).delete()
            addDefaultWidgets(
                default_blocklight_chart_objects, available_integrations, user_iden)
            addDefaultDashboards(user_iden)
            first_dashboard_id = Dashboard.objects.get(
                user_id=user_iden, tab_index=0).id
            new_url = "/dashboards/" + str(first_dashboard_id) + "/view"
        elif ct == 0:
            dashes = Integrations_UserSettings.objects.filter(
                user_iden=user_iden)
            if dashes.count() == 0:
                return redirect('/dashboards/homepage/')
            dashes = Integrations_UserSettings.objects.filter(
                user_iden=user_iden).only("integration_name")
            logger.debug(dashes)
            for dassh in dashes:
                integration_name = dassh.integration_name
                repair, created = Dashboard.objects.get_or_create(user_id=user_iden, title=integration_name,
                                                                  is_published=True)
                if created:
                    repair.tab_index = 0
                    repair.save()
                first_dashboard_id = Dashboard.objects.get(user_id=user_iden, title=integration_name, tab_index=0,
                                                           is_published=True).id
                new_url = "/dashboards/" + str(first_dashboard_id) + "/view"

                # redirect (goes to DashView for all dashboards)
    return redirect(new_url)


class DashboardV2View(LoginRequiredMixin, View):
    template_name = 'dashboards/dashboard_v2.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


# INTEGRATIONS PAGE
@login_required
def integrations(request):
    logger.debug("integration functions")
    code = request.GET.get('code', None)
    logger.debug(code)
    if code:
        credentials = google_api_calls.get_refresh_token(code)
        logger.debug(credentials.token)
        logger.debug(credentials.refresh_token)

    # Get return url and user_iden
    user_iden = request.user.id
    user = request.user
    check_these = Integrations_UserSettings.objects.filter(user_iden=user_iden)
    for row in check_these:
        integration_name = row.integration_name
        should_sync = checkLastSync(user_iden, integration_name, 2)[
            'should_sync']

    # If User is coming from shopify signup process, redirect to fill out information
    if user.first_name == 'shopify_signup':
        return redirect('/dashboards/shopify_signup')
    else:
        user_profile = UserProfile.objects.get(user_id=user_iden)
        save_profile_completion_status(user_profile)

        # Determine user's color theme preference (default to dark)
        user_iden = request.user.id
        theme_color = getThemeColor(user_iden)

        # Check For Has User Completed An Integration (Onboarding Checklist)
        if not user_profile.has_integrated_social_account:
            if SocialAccount.objects.filter(user_id=user_iden):
                user_profile.has_integrated_social_account = True
                user_profile.save()

        # Check Time of Last Login for Social Accounts
        # accounts = SocialAccount.objects.filter(user_id=user_iden)
        # for account in accounts:
        #     time_diff = datetime.utcnow() - account.last_login.replace(tzinfo=None)
        #     print('TEST----------------------------')
        #     print(account.provider)
        #     print(time_diff.total_seconds())
        #     print(time_diff.total_seconds() < 120)
        #     if time_diff.total_seconds() < 120:
        #         print('REMOVE REAUTH FLAAG')
        #         account.extra_data.pop('Force_Reauth', None)
        #         account.save()

        # Continuing loading integration page
        data = {'theme_color': theme_color}
        # Set current_url
        data['current_url'] = request.get_host()
        # Set all integration statuses
        data['all_status'] = []
        # Shopify
        shopify_status = 'added' if (
            SocialAccount.objects.filter(provider='shopify', user_id=user_iden).count() > 0) else 'not_added'
        data['all_status'].append(
            {'name': 'shopify', 'status': shopify_status})

        # Mailchimp
        mailchimp_status = 'added' if (
            SocialAccount.objects.filter(provider='mailchimp', user_id=user_iden).count() > 0) else 'not_added'
        data['all_status'].append(
            {'name': 'mailchimp', 'status': mailchimp_status})
        # Shipstation - need to figure out what form needs to be added for this one
        shipstation_status = 'added' if (BasicAuthRecords.objects.filter(integration_name='shipstation',
                                                                         user_iden=user_iden).count() > 0) else 'not_added'
        data['all_status'].append(
            {'name': 'shipstation', 'status': shipstation_status})
        # Facebook
        facebook_status = 'not_added'
        if SocialAccount.objects.filter(provider='facebook', user_id=user_iden).count() > 0:
            print(SocialAccount.objects.get(
                provider='facebook', user_id=user_iden).extra_data)
            try:
                removed = SocialAccount.objects.get(
                    provider='facebook', user_id=user_iden).extra_data['removed']
            except:
                print(SocialAccount.objects.get(
                    provider='facebook', user_id=user_iden))
                facebook_status = 'added'

        data['all_status'].append(
            {'name': 'facebook', 'status': facebook_status})
        print('facebook status: ' + facebook_status)

        # Instagram
        instagram_status = 'not_added'
        if SocialAccount.objects.filter(provider='instagram', user_id=user_iden).count() > 0:
            print(SocialAccount.objects.get(
                provider='instagram', user_id=user_iden).extra_data)
            try:
                removed = SocialAccount.objects.get(
                    provider='instagram', user_id=user_iden).extra_data['removed']
            except:
                print(SocialAccount.objects.get(
                    provider='instagram', user_id=user_iden))
                instagram_status = 'added'

        data['all_status'].append(
            {'name': 'instagram', 'status': instagram_status})
        print('instagram status: ' + instagram_status)

        # Google
        google_status = 'not_added'
        if SocialAccount.objects.filter(provider='google', user_id=user_iden).count() > 0:
            print(SocialAccount.objects.get(
                provider='google', user_id=user_iden).extra_data)
            try:
                removed = SocialAccount.objects.get(
                    provider='google', user_id=user_iden).extra_data["removed"]

            except:
                google_status = 'added'

        data['all_status'].append({'name': 'google', 'status': google_status})
        print(google_status)

        if google_status == 'added':  # check if there is a view ID
            if UserProfile.objects.get(user_id=user_iden).google_view_id == None or UserProfile.objects.get(
                    user_id=user_iden).google_view_id == "":
                data["google_info_needed"] = True
                social_account = SocialAccount.objects.get(
                    provider='google', user_id=user_iden)
                query_google_account_summaries(social_account)
                accounts = get_google_account_summaries(social_account)
                data["google_account_options"] = dumps(accounts)
                logger.debug(f"Google info needed {dumps(accounts)}")
        # Quickbooks
        quickbooks_status = 'added' if (SocialAccount.objects.filter(
            provider='quickbooks', user_id=user_iden).count() > 0) else 'not_added'
        data['all_status'].append(
            {'name': 'quickbooks', 'status': quickbooks_status})

        # Twitter
        twitter_status = 'added' if (SocialAccount.objects.filter(
            provider='twitter', user_id=user_iden).count() > 0) else 'not_added'
        data['all_status'].append(
            {'name': 'twitter', 'status': twitter_status})

        # Etsy
        etsy_status = 'added' if (SocialAccount.objects.filter(
            provider='etsy', user_id=user_iden).count() > 0) else 'not_added'
        data['all_status'].append({'name': 'etsy', 'status': etsy_status})
        # Get first added integration, if any
        data['first_added'] = 'none'
        for item in data['all_status']:
            if item['status'] == 'added':
                data['first_added'] = item['name']
                # data['email'] = SocialAccount.objects.get(
                #     provider=item['name'], user_id=user_iden)
                break

        for item in data['all_status']:
            if item['status'] == 'added':
                item['email'] = SocialAccount.objects.filter(
                    provider=item['name'], user_id=user_iden).first()

                if item['name'] == 'shopify':
                    queryset = SocialAccount.objects.filter(
                        provider=item['name'], user_id=user_iden)

                    item['data'] = []
                    item['count'] = queryset.count()
                    for acc in queryset:
                        item['data'].append({
                            'email': acc.extra_data['shop']['email'],
                            'other': acc.extra_data['shop']['name'],
                            'id': acc.id
                        })

                elif(item['name'] == 'google'):
                    item['email'] = SocialAccount.objects.get(
                        provider=item['name'], user_id=user_iden).extra_data['email']
                elif(item['name'] == 'mailchimp'):
                    item['email'] = SocialAccount.objects.get(
                        provider=item['name'], user_id=user_iden).extra_data['login']['email']
                elif(item['name'] == 'twitter'):
                    nameTwitter = SocialAccount.objects.get(
                        provider=item['name'], user_id=user_iden).extra_data['name']
                    item['email'] = "@{}".format(nameTwitter)
                elif(item['name'] == 'etsy'):
                    item['email'] = SocialAccount.objects.get(
                        provider=item['name'], user_id=user_iden).extra_data['primary_email']
                elif(item['name'] == 'facebook' or item['name'] == 'instagram'):
                    item['email'] = SocialAccount.objects.get(
                        provider=item['name'], user_id=user_iden).extra_data['email']
                # elif(item['name' == 'shipstation']):
                #     item['email'] = SocialAccount.objects.get(
                #         provider=item['name'], user_id=user_iden).extra_data['email']

                    # For added integrations, make sure settings record exists; if not, add default
        data['all_settings'] = []
        for item in data['all_status']:
            integration, status = item['name'], item['status']
            if status == 'added':
                try:
                    integration_id = SocialAccount.objects.filter(
                        user_id=user_iden, provider=integration).last().id
                    settings = Integrations_UserSettings.objects.get(
                        integration_name=integration, user_iden=user_iden,
                        integration_id=integration_id)

                    if integration == 'facebook' and request.GET:
                        settings.options = request.GET.get('shop')
                        settings.save()

                    if integration == 'facebook' and (settings.options == '' or settings.options == None):
                        access_token = SocialToken.objecxts.get(
                            account__user=user, account__provider=integration).token
                        url = "https://graph.facebook.com/v8.0/" + str(SocialAccount.objects.get(user_id=int(user_iden),
                                                                                                 provider='facebook').uid) + "/accounts?fields=id,name,title,instagram_business_account&access_token="
                        url = url + str(access_token)
                        response_body = requests.get(url).json()
                        # return render(request, "dashboards/facebook_connect_required.html", response_body)

                    autosync_enabled = int(settings.is_autosync)
                    data['all_settings'].append({'name': integration, 'autosync_enabled': autosync_enabled,
                                                 'autosync_time': settings.autosync_timer})
                except:
                    integration_id = SocialAccount.objects.filter(
                        user_id=user_iden, provider=integration).last().id
                    blapi_models.Integration.objects.get_or_create(
                        name=integration,
                        user_id=user_iden
                    )

                    _in, created = Integrations_UserSettings.objects.get_or_create(integration_name=integration,
                                                                                   integration_id=integration_id,
                                                                                   user_iden=user_iden, is_autosync=True,
                                                                                   autosync_timer='00_00_05_00')

                    isExtraShopifyAccount = integration == 'shopify' and SocialAccount.objects.filter(
                        provider='shopify', user_id=user_iden).count() > 1

                    if created and not isExtraShopifyAccount:
                        # Create default dashboards
                        user_ints = Integrations_UserSettings.objects.filter(
                            user_iden=user_iden
                        )
                        user_ints_names = [
                            i[0] for i in user_ints.values_list('integration_name')
                        ]
                        # Filter PredefinedMetrics for all added user's integrations
                        predefined_metrics = filter(
                            lambda pm: not set(
                                i[0] for i in pm.predefined_integrations.all().values_list('name')  # noqa
                            ) - set(user_ints_names),
                            blapi_models.PredefinedMetric.objects.filter(
                                predefined_integrations__name__in=user_ints_names,
                                predefined_dashboard__isnull=False
                            ).distinct()
                        )
                        # Filter out p_metrics without currently added integration
                        predefined_metrics = list(filter(
                            lambda pm: integration in [
                                t[0]for t in pm.predefined_integrations.all().values_list('name')  # noqa
                            ],
                            predefined_metrics
                        ))

                        dashboards_to_create = blapi_models.PredefinedDashboard.objects.filter(  # noqa
                            id__in=map(
                                lambda p: p.predefined_dashboard_id,
                                predefined_metrics
                            )
                        )

                        new_dashboards = {}
                        for dashboard_to_create in dashboards_to_create:

                            social_account = SocialAccount.objects.filter(
                                provider=integration, user_id=user_iden).last()
                            new_dashboard = blapi_models.BLDashboard(
                                name=dashboard_to_create.name,
                                user_id=user_iden,
                                account=social_account
                            )
                            new_dashboard.save()
                            new_dashboards[dashboard_to_create.name] = new_dashboard  # noqa

                        for pm in predefined_metrics:
                            p_time_range = blapi_models.PredefinedTimeRange.objects.get(  # noqa
                                predefined_metric=pm
                            )
                            new_time_range = blapi_models.TimeRange(
                                since=p_time_range.since,
                                until=p_time_range.until,
                            )
                            new_time_range.save()

                            p_chart_type = blapi_models.PredefinedChartType.objects.get(  # noqa
                                predefined_metric=pm
                            )
                            new_chart_type = blapi_models.ChartType.objects.get(
                                name=p_chart_type.name
                            )
                            new_chart_type.save()

                            pmt = blapi_models.PredefinedMetricType.objects.get(  # noqa
                                predefined_metric=pm
                            )

                            new_metric = blapi_models.Metric(
                                datasource=pmt.datasource,
                                name=pmt.name,
                                title=pmt.title,
                                chart_type=new_chart_type,
                                time_range=new_time_range,
                                filter=pmt.filter_expression,
                                group_by=pmt.group_by_expression,
                                aggregate=pmt.aggregate_expression,
                                time_group_by=pmt.time_group_by_expression,
                                x_field=pmt.x_field,
                                y_field=pmt.y_field,
                                group_field=pmt.group_field,
                                x_label=pmt.x_label,
                                y_label=pmt.y_label,
                                group_label=pmt.group_label,
                            )
                            new_metric.save()

                            user_pm_ints = blapi_models.Integration.objects.filter(
                                user_id=user_iden,
                                name__in=list(
                                    map(lambda l: l[0], pm.predefined_integrations.values_list('name')))
                            )
                            new_metric.integrations.set(user_pm_ints)
                            new_metric.save()

                            new_chart = blapi_models.Chart(
                                metric=new_metric,
                                dashboard=new_dashboards[pm.predefined_dashboard.name],  # noqa
                                predefined_metric=pm.predefined_metric_for_edit
                            )
                            new_chart.save()

                            p_dashboard_layout = blapi_models.PredefinedDashboardLayout.objects.get(  # noqa
                                predefined_metric=pm
                            )
                            blapi_models.DashboardLayout(
                                dashboard=new_dashboards[pm.predefined_dashboard.name],  # noqa
                                chart=new_chart,
                                x=p_dashboard_layout.x,
                                y=p_dashboard_layout.y,
                                w=p_dashboard_layout.w,
                                h=p_dashboard_layout.h,
                            ).save()

                        # --
                        _in.user_iden = user_iden
                        _in.is_autosync = True
                        _in.autosync_timer = '00_00_05_00'
                        _in.integration_name = integration
                        _in.save()
                        if integration == 'facebook':
                            access_token = SocialToken.objects.get(
                                account__user=user, account__provider=integration).token
                            url = "https://graph.facebook.com/v3.2/" + str(SocialAccount.objects.get(user_id=int(user_iden),
                                                                                                     provider='facebook').uid) + "/accounts?fields=id,name,title,instagram_business_account&access_token="
                            url = url + str(access_token)
                            response_body = requests.get(url).json()
                            # return render(request, "dashboards/facebook_connect_required.html", response_body)
                            # _in.options = 'Blocklight'
                    data['all_settings'].append(
                        {'name': integration, 'autosync_enabled': 1, 'autosync_time': '00_00_05_00'})
        return render(request, "dashboards/integrations_mailchimp_add.html", data)


# SOCIAL PAGE
@login_required
def social(request):
    return render(request, "dashboards/social.html")


# FEEDBACK PAGE
@login_required
def feedback(request):
    """
    Sends the feedback content to info@blocklight.io.
    Stores the feedback content in the database
    Args:
        request: POST request - fetches the topic and description from the feedback form
                 GET request - displays the feedback.html page

    Returns:
        POST request: success if feedback is submitted
        GET request: displays the feedback template page
    """

    # Determine user's color theme preference (default to dark)
    user = request.user
    theme_color = getThemeColor(user.id)
    # If this is a POST request we need to process the form data
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request:
        data = loads(request.body)
        form = FeedbackForm(data)

        # If the form is valid, then save it:
        status = 'fail'
        if form.is_valid():
            # Get info of user submitting the feedback
            name = user.first_name + " " + user.last_name
            email = user.email
            user_profile = UserProfile.objects.get(user_id=user.id)
            if user_profile.business_name:
                business_name = user_profile.business_name
            else:
                business_name = "Not Provided"

            # Save feedback form to the database
            record = form.save(commit=False)
            # Add additional fields
            record.user_iden = user.id
            record.username = name
            record.email = email
            record.business_name = business_name
            record.feedback_type = 'general'
            record.save()
            form.save_m2m()

            # Constructing the email message :
            topic = data['topic']
            description = data['description']
            subject = "New Feedback Submitted"
            message = "User: " + name + \
                      "\nEmail ID: " + email + \
                      "\nBusiness Name: " + str(business_name) + \
                      "\nTopic: " + topic + \
                      "\nDescription: " + description

            email_from = settings.EMAIL_HOST_USER
            recipient_list = ['support@blocklight.io']
            send_mail(subject, message, email_from, recipient_list)
            return redirect('feedback_sent')
    else:
        return render(request, 'dashboards/feedback.html', {'form': Feedback(), 'theme_color': theme_color})


@login_required
def feedback_sent(request):
    return render(request, 'dashboards/feedback_sent.html')


# DASHBOARD CHART FEEDBACK - using a GET request and simple return
@login_required
def chart_feedback(request):
    # Identify the request user
    user_iden = request.user.id
    # Parse the request parameter
    params = request.GET
    topic = params.get('topic', '')
    description = params.get('description', '')
    # Get existing record or make a new one
    obj, created = Feedback.objects.get_or_create(
        user_iden=user_iden, topic=topic, feedback_type='metric_specific')
    # Add description (will overwrite if previous record for the chart existed)
    obj.description = description
    obj.save()
    # Return with status
    return HttpResponse(dumps({'status': created}), content_type='application/json')


# Functions called by hitting various urls: MODIFYING DASHBOARDS

# For loading data into a chart (called by frontend)
@login_required
def chart_data_json(request):
    # Identify the request user, set checkpoint

    user_iden = request.user.id
    params = request.GET
    chart_id = params.get('chart_id', '')
    try:
        chart = Widget.objects.get(user_iden=user_iden, slug=chart_id)
    except Widget.DoesNotExist:
        return HttpResponseNotFound()
    dashboard_slug = chart.dashboard

    user_iden = request.user.id
    # Parse the request parameters
    integration = params.get('integration', '').encode(
        "utf-8").lower()  # Important to user lower()
    metric = params.get('metric', '').encode("utf-8")
    option = params.get('option', '')
    chart_type = params.get('chart_type', '')
    time_period = params.get('time_period', '').encode("utf-8")
    # dashboard_slug = params.get('dashboard_slug', '')
    what_changed = params.get('what_changed', '')
    data = build_data_series(user_iden, chart_id, integration, metric, option, chart_type, time_period, dashboard_slug,
                             what_changed)
    return HttpResponse(dumps(data), content_type='application/json')


# For saving the app theme color
@login_required
def save_theme_color(request):
    # Identify the request user
    user_iden = request.user.id
    # Parse the request parameter
    params = request.GET
    theme = params.get('theme', '')
    # Update associated DB record
    try:
        user_record = UserProfile.objects.get(user_id=user_iden)
        if theme == 'light':
            user_record.light_theme = True
        else:
            user_record.light_theme = False
        user_record.save()
        logger.debug('Successfully updated color theme')
    except:
        logger.debug('Failed to update color theme')
    # Return
    return HttpResponse(dumps({}), content_type='application/json')


# Functions called by hitting various urls: ADDING / EDITING INTEGRATIONS

# [1] Shopify
@login_required
def shopify_connect(request):
    url = request.get_full_path()
    store_name = url.split('/shopify/',1)[1]
    return render(request, "dashboards/shopify_connect_required.html", {'django': 'django', 'store_name': store_name})


# [3] ShipStation
@login_required
def connectshipstation(request):
    user_iden = request.user.id
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request:
        form = ShipStationConnectForm(request.POST)
        # If the form is valid, then save it:
        if form.is_valid():
            # Save form without committing
            record = form.save(commit=False)
            # Add user id
            record.user_iden = request.user.id
            # Save again
            record.save()
            form.save_m2m()
            # Return to dashboards
            return redirect("/dashboards/integrations")
        # Else fail - need to add to integration failure page
        else:
            return render(request, "dashboards/remove_failure.html", {'django': 'django'})

    return redirect("/dashboards/integrations")


# [4] Google
@login_required
def connect_google(request):
    logger.debug(f"Connecting to google, from request {request}")
    # Identify the request user
    user_iden = request.user.id
    # Parse the request parameter, get the google_id
    params = request.GET
    google_id = params.get('google_id', '')
    logger.debug(f"Google id of {google_id}")
    # # Add Google ID
    user_profile = UserProfile.objects.get(user_id=user_iden)
    user_profile.google_view_id = google_id
    user_profile.save()

    logger.info("User (id={}) add new integration (provider={}). Running synch.".format(
        user_iden, 'google'))
    sync_users_integrations([(user_iden, ('google',))])

    return HttpResponse(dumps({}), content_type='application/json')


# For updating integration settings
@login_required
def update_integration_settings(request):
    # Identify the request user
    user_iden = request.user.id
    # Parse the request parameters
    params = request.GET
    integration = params.get('integration', '')
    autosync_enabled = params.get('autosync_enabled', '')
    autosync_time = params.get('autosync_time', '')
    # Update the correct DB record
    try:
        settings = Integrations_UserSettings.objects.get(
            integration_name=integration, user_iden=user_iden)
        settings.is_autosync = autosync_enabled
        settings.autosync_timer = autosync_time
        settings.save()
    except:
        logger.debug('Failed to save integration settings')
    # Return
    return HttpResponse(dumps({}), content_type='application/json')


@login_required
def get_user_id(request):
    user_iden = request.user.id
    obj = {
        "id": user_iden
    }
    return HttpResponse(dumps(obj), content_type='application/json')


@login_required
def toggle_shopify_account(request):
    user_id = request.user.id
    account_id = request.GET.get('id')
    return_id = account_id
    if not account_id:
        rc = 500
    else:
        with transaction.atomic():
            shopify_accounts = SocialAccount.objects.filter(
                provider='shopify', user_id=user_id)
            for shop in shopify_accounts:
                shop.extra_data['is_selected'] = False
                shop.save()

            to_select = shopify_accounts.filter(
                provider='shopify', id=account_id, user_id=user_id)

            if len(to_select) != 1:
                return_id = None
                rc = 500
            else:
                to_select[0].extra_data['is_selected'] = True
                to_select[0].save()
                rc = 200
    return HttpResponse(dumps({
        "shop_id": return_id
    }),
        content_type='application/json',
        status=rc)


@login_required
def get_selected_shopify_shop(request):
    user_id = request.user.id
    return_id = None
    rc = 200
    shopify_accounts = SocialAccount.objects.filter(
        provider='shopify', user_id=user_id)

    objects = []
    for shop in shopify_accounts:
        objects.append({
            'shop_id': shop.id,
            'is_selected': shop.extra_data['is_selected'],
            'name': shop.extra_data['shop']['name']
        })

    return HttpResponse(dumps(objects),
                        content_type='application/json',
                        status=rc)


# Functions called by hitting various urls: DELETING INTEGRATIONS

# [1] Shopify
@login_required
def remove_shopify(request):
    account_id = request.GET.get('id', None)
    user_iden = request.user.id

    shopify_accounts = SocialAccount.objects.filter(
        provider='shopify', user_id=user_iden)

    if account_id:
        shopify_accounts = SocialAccount.objects.filter(
            provider='shopify', user_id=user_iden, id=account_id)

    failed = False
    for shopify_account in shopify_accounts:

        social_id = shopify_account.id
        dct = shopify_account.extra_data
        shopname = dct['shop']['myshopify_domain']
        token_current = shopify_account.socialtoken_set.first()
        headers = {
            "X-Shopify-Access-Token": str(token_current),
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Content-Length": "0",
        }
        response_body = requests.delete(
            'https://' + shopname + '/admin/api_permissions/current.json', headers=headers)

        if str(response_body) == '<Response [200]>':
            """ A 200 RESPONSE MEANS SHOPIFY REMOVED THE APP INSIDE THE CUSTOMER'S SHOPIFY DASHBOARD,
            THEREFORE WE CLEAR ALL DB RECORDS"""
            # Remove all necessary DB records
            failures = removeDataOnItegrationDelete(
                user_iden, 'shopify', account_id=account_id)
            logger.debug(('Shopify remove errors: ' + str(failures)))
            # Return

        else:
            failed = True
            """ NO 200 RESPONSE MEANS THAT WE LIKELY HAD A MISMATCH OF API KEYS, USUALLY STEMMING FROM
            "US" MANUALLY REMOVING ALL LINKED INTEGRATIONS DURING DEV WORK, BUT WE TYPICALLY FORGET TO
            ALSO DISABLE INSIDE SHOPIFY ADMIN WHICH MEANS SHOPIFY RETAINS OLD
            RECORDS ALSO - IN THIS CASE WE NEED TO DISPLAY SOMETHING INDICATING TO THE USER THAT
            THERE WAS A PROBLEM DURING UNINSTALL AND THAT THEY NEED TO MANUALLY REMOVE
            THE BLOCKLIGHT APP INSIDE THEIR SHOPIFY ADMIN, INTERNALLY WE STILL CLEAR ALL USER RECORDS
            """
            # Remove all necessary DB records
            failures = removeDataOnItegrationDelete(
                user_iden, 'shopify', account_id=account_id)
            logger.debug(('Shopify remove errors: ' + str(failures)))
            # Return

    # else:
    #     """IF THERE WAS NO USER RECORD FOR SHOPIFY, FOR NOW WE STILL CLEAR ALL USER DATA IN CASE THERE WAS A MISTAKE,
    #     A FRESH SLATE SHOULD HOPEFULLY FIX"""
    #     # Remove all necessary DB records
    #     failures = removeDataOnItegrationDelete(user_iden, 'shopify')
    #     logger.debug(('Shopify remove errors: ' + str(failures)))
    #     # Return
    #     return redirect("/dashboards/integrations")
    current_host = request.get_host()
    if current_host == 'blocklight.io':
        mp = Mixpanel(settings.MIXPANEL_TOKEN)
        mp.track(request.user.id, 'Removed Integration', {
            'Integration': 'shopify',
            'Email': request.user.email
        })
    return_code = 500 if failed else 200
    return HttpResponse(status=return_code)


# [2] MailChimp
@login_required
def remove_mailchimp(request):
    # Setup
    user_iden = request.user.id
    # Remove all necessary DB records
    failures = removeDataOnItegrationDelete(user_iden, 'mailchimp')
    logger.debug(('Mailchimp remove errors: ' + str(failures)))

    # Send Removal to Mixpanel
    current_host = request.get_host()
    if current_host == 'blocklight.io':
        mp = Mixpanel(settings.MIXPANEL_TOKEN)
        mp.track(request.user.id, 'Removed Integration', {
            'Integration': 'mailchimp',
            'Email': request.user.email
        })

    # Return
    return redirect("/dashboards/integrations")


# [3] Shipstation
@login_required
def remove_shipstation(request):
    # Setup
    user_iden = request.user.id
    # Remove all necessary DB records
    failures = removeDataOnItegrationDelete(user_iden, 'shipstation')
    logger.debug(('Shipstation remove errors: ' + str(failures)))

    # Send Removal to Mixpanel
    current_host = request.get_host()
    if current_host == 'blocklight.io':
        mp = Mixpanel(settings.MIXPANEL_TOKEN)
        mp.track(request.user.id, 'Removed Integration', {
            'Integration': 'shipstation',
            'Email': request.user.email
        })

    # Return
    return redirect("/dashboards/integrations")


# [4] Facebook
@login_required
def remove_facebook(request):
    user_iden = request.user.id
    account = SocialAccount.objects.get(
        provider="facebook", user_id=user_iden)
    account.extra_data["removed"] = True
    account.save()
    failures = removeDataOnItegrationDelete(user_iden, 'facebook')

    logger.debug(('Facebook remove errors: ' + str(failures)))

    # Send Removal to Mixpanel
    current_host = request.get_host()
    if current_host == 'blocklight.io':
        mp = Mixpanel(settings.MIXPANEL_TOKEN)
        mp.track(request.user.id, 'Removed Integration', {
            'Integration': 'facebook',
            'Email': request.user.email
        })

    # Return
    remove_instagram(request)
    return redirect("/dashboards/integrations")


# [5] Instagram
@login_required
def remove_instagram(request):
    user_iden = request.user.id
    failures = removeDataOnItegrationDelete(user_iden, 'instagram')

    logger.debug(('Instagram remove errors: ' + str(failures)))

    # Send Removal to Mixpanel
    current_host = request.get_host()
    if current_host == 'blocklight.io':
        mp = Mixpanel(settings.MIXPANEL_TOKEN)
        mp.track(request.user.id, 'Removed Integration', {
            'Integration': 'instagram',
            'Email': request.user.email
        })

    # Return
    return redirect("/dashboards/integrations")


@login_required
def remove_google(request):
    token = SocialAccount.objects.get(
        provider="google", user_id=request.user.id).socialtoken_set.first()
    try:
        # allow for token to be refreshed
        credentials = set_up_google_cred(token)
        response = requests.post('https://accounts.google.com/o/oauth2/revoke',
                                 params={'token': credentials.token},
                                 headers={'content-type': 'application/x-www-form-urlencoded'})
    except:
        logger.error(
            "Failed to properly disconnect google, due to token issue, still deleting user data")

    user_profile = UserProfile.objects.get(user_id=request.user.id)
    user_profile.google_view_id = None
    user_profile.save()

    user_iden = request.user.id
    account = SocialAccount.objects.get(provider="google", user_id=user_iden)
    account.extra_data["removed"] = True
    account.save()
    failures = removeDataOnItegrationDelete(user_iden, 'google')

    # Send Removal to Mixpanel
    current_host = request.get_host()
    if current_host == 'blocklight.io':
        mp = Mixpanel(settings.MIXPANEL_TOKEN)
        mp.track(request.user.id, 'Removed Integration', {
            'Integration': 'google',
            'Email': request.user.email
        })

    return redirect("/dashboards/integrations")


# [7] Quickbooks - does nothing right now
@login_required
def remove_quickbooks(request):
    # Setup
    user_iden = request.user.id
    # Remove all necessary DB records - NONE CURRENTLY
    failures = removeDataOnItegrationDelete(user_iden, 'quickbooks')
    logger.debug(('Quickbooks remove errors: ' + str(failures)))

    # Send Removal to Mixpanel
    current_host = request.get_host()
    if current_host == 'blocklight.io':
        mp = Mixpanel(settings.MIXPANEL_TOKEN)
        mp.track(request.user.id, 'Removed Integration', {
            'Integration': 'quickbooks',
            'Email': request.user.email
        })

    # Return
    return redirect("/dashboards/integrations")


@login_required
def remove_twitter(request):
    # NOTE: not sure if this is all that needs to happen,
    # we still keep the
    user_iden = request.user.id
    provider = 'twitter'
    failures = removeDataOnItegrationDelete(user_iden, provider)

    # Send Removal to Mixpanel
    current_host = request.get_host()
    if current_host == 'blocklight.io':
        mp = Mixpanel(settings.MIXPANEL_TOKEN)
        mp.track(request.user.id, 'Removed Integration', {
            'Integration': 'twitter',
            'Email': request.user.email
        })

    return redirect("/dashboards/integrations")


@login_required
def remove_etsy(request):
    user_iden = request.user.id

    failures = removeDataOnItegrationDelete(user_iden, 'etsy')

    # Send Removal to Mixpanel
    current_host = request.get_host()
    if current_host == 'blocklight.io':
        mp = Mixpanel(settings.MIXPANEL_TOKEN)
        mp.track(request.user.id, 'Removed Integration', {
            'Integration': 'etsy',
            'Email': request.user.email
        })

    return redirect("/dashboards/integrations")


# Functions called by hitting various urls: MISCELANEOUS

# For re-directing when an unknown path is encountered
@login_required
def redirect_all_unknown_paths(request):
    return redirect('/dashboards/integrations')


# Manual integration sync
@login_required
def manual_sync(request):
    # Identify the request user
    user = request.user
    user_iden = request.user.id
    # Parse the request parameters
    params = request.GET
    integration = params.get('integration', '')
    # Other setup
    _, task, tcount = getIntegrationName(integration, user_iden)
    req = {'user': {'id': user_iden}}
    # Sync
    result = 0
    if tcount > 0 and checkIfNoActiveSync(user_iden, integration):
        result = task.apply_async(args=[req, user, ''])
    # Return
    return HttpResponse(dumps({}), content_type='application/json')


# When user needs to wait for data to sync
@login_required
def sync_wait(request):
    return render(request, "dashboards/integrations_add_wait.html", {'django': 'django'})


# ?
class ModIntegrations(LoginRequiredMixin, ConnectionsView):
    template_name = 'dashboards/mod_integrate.html'


# Handle Facebook allauth
@login_required
def handle_facebook_auth(request):
    params = request.GET
    code = params.get('code', '')
    url = 'https://graph.facebook.com/v3.0/oauth/access_token?'
    django = SocialApp.objects.get(provider='facebook')
    client_id = django.client_id
    client_secret = django.secret
    return_url_is = '/facebook/login/callback/'
    url = url + 'client_id=' + str(client_id) + '&redirect_uri=' + str(return_url_is) + '&client_secret=' + str(
        client_secret) + '&code=' + str(code)

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Content-Length": "0",
    }
    response_body = requests.delete(url, headers=headers).json()
    return redirect("/dashboards/integrations")


# If Shopify billing is declined
@login_required
def billing_declined(request):
    # Setup
    user_iden = request.user.id
    # Remove all necessary DB records
    removeDataOnItegrationDelete(user_iden, 'shopify')
    # Re-direct
    return render(request, "dashboards/billing_declined.html", {'django': 'django'})



# To initialize Shopify billing
# For now, this function does nothing (since we are not billing any beta users)
@login_required
def init_shopify_billing(request):
    # return_url_is = request.get_host()

    # OLD
    # already_connected = False
    # count = SocialAccount.objects.filter(provider='shopify', user_id=request.user.id).count()
    # if count == 0:
    #     django = SocialAccount.objects.filter(provider='shopify')
    #     for store in django:
    #         dct = store.extra_data
    #         shopname = dct['shop']['myshopify_domain']
    #         print(shopname)
    #         if BlocklightBilling_Recurring_Shopify.objects.filter(confirmation_url__contains=shopname).count() != 0:
    #             print('Error 1')
    #             print("This is a Error!!! account already linked")
    #             return render(request, 'dashboards/shopify_connect_required.html', {'already_connected': True})
    # if count != 0:
    #     django = SocialAccount.objects.get(provider='shopify', user_id=request.user.id)
    #     social_id = django.id
    #     django = SocialAccount.objects.get(pk=social_id)
    #     dct = django.extra_data
    #     shopname = dct['shop']['myshopify_domain']
    #     print(shopname)
    #     if BlocklightBilling_Recurring_Shopify.objects.filter(confirmation_url__contains= shopname).count() != 0:
    #         print('Error 2')
    #         print("This is a Error!!! account already linked")
    #         return render(request, 'dashboards/shopify_connect_required.html', {'already_connected': True})
    #     token_current = django.socialtoken_set.first()
    #     session = Session(shopname, token_current.token)
    #     ShopifyResource.activate_session(session)
    #     check, created = BlocklightBilling_Recurring_Shopify.objects.get_or_create(user_account=request.user.id)
    #     if created:
    #         testcharge = RecurringApplicationCharge()
    #         testcharge.test = True
    #         testcharge.return_url = return_url_is
    #         testcharge.price = 0.99
    #         testcharge.trial_days = 30
    #         testcharge.name = 'Recurring charge'
    #         testcharge.save()
    #         if DJANGO_HOST == 'localhost':  print(('testcharge = ', testcharge))
    #         check.user_account = request.user.id
    #         check.charge_id = testcharge.id
    #         check.status = testcharge.status
    #         check.confirmation_url = testcharge.confirmation_url
    #         check.name = testcharge.name
    #         check.api_client_id = testcharge.api_client_id
    #         check.price = testcharge.price
    #         check.return_url = testcharge.return_url
    #         check.created_at = testcharge.created_at
    #         check.updated_at = testcharge.updated_at
    #         check.test = testcharge.test
    #         check.trial_days = testcharge.trial_days
    #         check.decorated_return_url = testcharge.decorated_return_url
    #         check.save()
    #         conf_url = testcharge.confirmation_url
    #         return redirect(return_url_is + "/accounts/social/connections")
    #     else:
    #         check = BlocklightBilling_Recurring_Shopify.objects.get(user_account=request.user.id)
    #         charge_id = check.charge_id
    #         status = check.status
    #         confirmation_url = check.confirmation_url
    #         testcharge2 = RecurringApplicationCharge()
    #         if status == 'pending':
    #             return redirect(confirmation_url)

    #         elif status == 'accepted':
    #             testcharge2.activate()
    #             status = testcharge2.status
    #             check, created = BlocklightBilling_Recurring_Shopify.objects.get_or_create(user_account=request.user.id,
    #                                                                                        charge_id=charge_id)
    #             if created:
    #                 check.status = testcharge2.status
    #             check.save()
    #             return redirect(return_url_is + "/accounts/social/connections_redirect")

    #         elif 'status' in testcharge2:
    #             if testcharge2.status == 'declined':
    #                 BlocklightBilling_Recurring_Shopify.objects.filter(user_account=request.user.id).delete()
    #                 return redirect(return_url_is + "/dashboards/billing/declined")

    return redirect("/accountsauth/")


# Not being used currently?
@login_required
def shopify(request, pk):
    # USE VIEW 'DASH' TO SEE/EDIT CURRENT LOGIC
    data = {}
    return render(request, "dashboards/dash.html", data)


@login_required
def stats_json(request):
    # data = {'stats': UserStats(request.user).user_stats}
    data = {}
    return HttpResponse(dumps(data), content_type='application/json')


class DashDelete(LoginRequiredMixin, DeleteView):
    """Displays the details of a BlogPost"""
    model = Dashboard
    success_url = reverse_lazy('dash_home')


class TabDelete(LoginRequiredMixin, DeleteView):
    model = Tab
    success_url = reverse_lazy('dash_home')


class WidgetDelete(LoginRequiredMixin, DeleteView):
    model = Widget
    success_url = reverse_lazy('dash_home')


class TabView(LoginRequiredMixin, DetailView):
    """Displays the details of a BlogPost"""
    model = Tab

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(TabView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        try:
            dash = Dashboard.objects.get(
                id=request.GET['id'], user_id=user_iden)
        except Dashboard.DoesNotExist:
            return HttpResponseNotFound()
        # widget = Widget.objects.get(slug=self.kwargs['slug'])
        widget = Widget.objects.get(slug=dash.slug)
        tab = Tab.objects.get(id=widget.tab)
        # dash = Dashboard.objects.get(slug=tab.dashboard)
        # context['slug'] = self.kwargs['slug']
        context['dash'] = dash
        context['tabs'] = tabs
        widgets = Widget.objects.filter(tab__in=tabs)
        context['widgets'] = widgets
        return context


class TabAdd(LoginRequiredMixin, CreateView):
    """Displays the details of a BlogPost"""
    model = Tab
    fields = ['title']

    def get_success_url(self):
        # TODO: delete need of this
        # dash = Dashboard.objects.get(id=self.kwargs['id'])
        # return reverse('dash_view', kwargs={'slug': dash.slug})
        return reverse('dash_view', kwargs={'pk': self.kwargs['id']})

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.dashboard_id = self.kwargs['id']
        response = super(TabAdd, self).form_valid(form)
        Widget.objects.create(
            tab=self.object,
            element_id=1,
            # sql="test",
            # other fields
            title="Default"
        )
        return response


class WidgetAdd(LoginRequiredMixin, CreateView):
    """Displays the details of a BlogPost"""
    model = Widget
    form_class = WidgetForm

    def get_form_kwargs(self):
        kwargs = super(WidgetAdd, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_success_url(self):
        tab = Tab.objects.get(id=self.kwargs['id'])
        return reverse('tab_view', kwargs={'slug': tab.slug})

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.tab_id = self.kwargs['id']
        response = super(WidgetAdd, self).form_valid(form)
        return response


class ReportAdd(LoginRequiredMixin, CreateView):
    """Displays the details of a BlogPost"""
    model = Report
    form_class = ReportForm

    def get_form_kwargs(self):
        kwargs = super(ReportAdd, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        obj = form.save(commit=False)
        response = super(ReportAdd, self).form_valid(form)
        return response


@login_required
def add_dash(request):
    """ Default view for the root """
    return render(request, "dashboards/dash.html", {'django': 'django'})


@login_required
def modify_dash(request):
    """ Default view for the root """
    return render(request, "dashboards/dash.html", {'django': 'django'})


# @login_required
# def delete_dash(request):
#     """ Default view for the root """
#     return render(request, "dashboards/dash.html", {'django': 'django'})

@login_required
def landing(request):
    """ Default view for the root """
    return render(request, "dashboards/landing.html", {'django': 'django'})


@login_required
def facebook(request, pk):
    """ Default view for the root """
    return render(request, "dashboards/facebook.html", {'django': 'django'})


@login_required
def twitter(request, pk):
    """ Default view for the root """
    return render(request, "dashboards/twitter.html", {'django': 'django'})


@login_required
def quickbooks(request, pk):
    """ Default view for the root """
    access_token = SocialToken.objects.get(account_id=pk)
    return render(request, "dashboards/quickbooks.html", {'django': 'django'})


@login_required
def mailchimp(request, pk):
    # USE VIEW 'DASH' TO SEE/EDIT CURRENT LOGIC

    data = {'chartlist': ['chart00_mailchimp', 'chart1_mailchimp', 'chart2_mailchimp', 'chart3_mailchimp',
                          'chart4_mailchimp']}

    """ Default view for the root """
    return render(request, 'dashboards/mailchimp.html', data)


@login_required
def google(request, pk):
    logger.debug(f"Google requested from request: {request} with pk {pk}")

    """A simple example of how to access the Google Analytics API."""

    """ Default view for the root """
    return render(request, "dashboards/google.html", {'django': 'django'})


@login_required
def server_name(request):
    """ Send server host name to the front end.
    This is implemented to make distinct dev and prod server updates.
    """
    return render(request, 'dashboards/integrations.html', {'server_name': DJANGO_HOST})


@login_required
def integration_sync_status(request):
    integration_name = request.GET.get('name', '')
    try:
        last_sync = Integrations_User_LastSync.objects.get(
            user_iden=request.user.id, integration_name=integration_name)
        result = AsyncResult(id=last_sync.celery_key)
        try:
            response = {"status": result.status,
                        "initial": last_sync.initialize}
        except:  # will happen if celery was restarted and can't get the status of a task id
            response = {"status": "NONE", "initial": False}
    except:  # will happen if the integration has never synced before.
        response = {"status": "NEVER", "initial": False}

    # This is a quckfix of infinite spinner problem. (On frontend it's much complex to fix it.)
    return JsonResponse({"status": "SUCCESS", "initial": False})
    return JsonResponse(response)


def shopify_signup(request):
    if request.method == 'POST':

        # Validate Loyalty Code
        code = request.POST['loyalty_code']
        if code:
            [loyalty_check, valid_code] = validateLoyaltyCode(
                request.POST['loyalty_code'])
            if not loyalty_check:
                messages.error(
                    request, "Invalid Loyalty Code!")
                return render(request, "account/shopify_signup.html")
        else:
            valid_code = None

        signup_form = ShopifySignupForm(request.POST)
        if signup_form.is_valid():
            signup_form_clean = signup_form.cleaned_data

            # Check that password meets criteria
            if signup_form_clean['password'] != signup_form_clean['confirm_password']:
                messages.error(
                    request, "Error: Passwords do not match!")
                return render(request, "account/shopify_signup.html")
            elif len(signup_form_clean['password']) < 8:
                messages.error(
                    request, "Password must be at least 8 characters long.")
                return render(request, "account/shopify_signup.html")
            elif not re.search(r"[\d]+", signup_form_clean['password']):
                messages.error(
                    request, "Password must contain at least one number.")
                return render(request, "account/shopify_signup.html")
            elif not any(ch.isupper() for ch in signup_form_clean['password']):
                messages.error(
                    request, "Password must contain at least one upper case letter.")
                return render(request, "account/shopify_signup.html")
            else:
                user = request.user
                user.first_name = signup_form_clean['first_name']
                user.last_name = signup_form_clean['last_name']
                user.set_password(signup_form_clean['password'])
                user.save()

                user_profile = UserProfile.objects.get(user_id=user.id)
                user_profile.loyalty_code = valid_code
                user_profile.save()

                # Start Free Trial
                initializeStripe(user)

                # Add to Mailing Lists
                mailchimp_signup(user)

                # Send Sign Up to Mixpanel
                mp = Mixpanel(settings.MIXPANEL_TOKEN)
                mp.track(user.id, 'Sign Up', {
                    'From': 'Shopify',
                    'Loyalty': request.POST['loyalty_code'],
                    'Email': user.email
                })

                perform_login(
                    request, user, email_verification=EmailVerificationMethod.NONE)

                return redirect('/dashboards/integrations')
    else:
        return render(request, "account/shopify_signup.html", {'form': SignUp(), 'check_email_flag': False})


def shopify_gdpr_shop_redact(request):
    def post(self, request):
        data = request.body
        shop_id = data['shop_id']
        shop_url = data['shop_domain']
        shopify_shop = Integrations_Shopify_Shop.objects.get(shop_id=shop_id)
        social_account = SocialAccount.objects.get(
            id=shopify_shop.integration_id)
        removeDataOnItegrationDelete(
            social_account.user_id, 'shopify', social_account.id)
        return HttpResponse(status='200')


def shopify_gdpr_customers_redact(request):
    def post(self, request):
        data = request.body
        shop_id = data['shop_id']
        shop_url = data['shop_domain']
        customer = data['customer']
        orders = data['orders_to_redact']
        redact_customer = Integrations_Shopify_Customer.objcts.get(
            email=customer['email'])
        if orders:
            for order in orders:
                if shop_id:
                    order_to_delete = Integrations_Shopify_Order.objects.filter(
                        order_id=order,
                        customer_ref=redact_customer,
                        shop_id=shop_id
                    )
                else:
                    order_to_delete = Integrations_Shopify_Order(
                        order_id=order,
                        customer_ref=redact_customer
                    )
                order_to_delete.delete()
        else:
            redact_customer.delete()
        return HttpResponse(status='200')


def shopify_gdpr_customers_data_request(request):
    def send_gdpr_email(csvfile, email_address):
        try:
            email = EmailMessage(
                'Your Shopify GDPR Request',
                'Your data is attached.',
                'no-reply@blocklight.io',
                [email_address],
            )
            email.attach('GDPRdata.csv', csvfile.getvalue(), 'text/csv')
            email.send()
        except:
            logger.debug(
                'GDPR Data Request Email failure for user: ', email_address)

    def write_title(csvwriter, title):
        row = ''
        csvwriter.writerow([row])
        row = title + ' Endpoint'
        csvwriter.writerow([row])

    def write_headers(csv_writer, model):
        row = []
        for field in model._meta.fields:
            row.append(field.name)
        csv_writer.writerow(row)

    def write_data(csv_writer, instance):
        instance_dict = model_to_dict(instance)
        row = []
        for key, obj in instance_dict.items():
            row.append(obj)
        csv_writer.writerow(row)

    def write_none(csvriter):
        row = 'No Data for this Endpoint.'
        csvwriter.writerow([row])

    def handle_data_from_customer(customers, title, model, csvwriter):
        write_title(csvwriter, title)
        write_headers(csvwriter, model)
        data_to_return = []
        for customer in customers:
            try:
                data_set = model.objects.filter(customer_ref=customer)
            except:
                data_set = model.objects.filter(customer=customer)
            for data in data_set:
                if title == 'Customer_Address':
                    data = Integrations_Shopify_Address.objects.get(
                        id=data.address.id)
                write_data(csvwriter, data)
                data_to_return.append(data)
        if not data_to_return:
            write_none(csvwriter)
        return data_to_return

    def handle_data_from_order(orders, title, model, csvwriter):
        write_title(csvwriter, title)
        write_headers(csvwriter, model)
        data_to_return = []
        for order in orders:
            try:
                data_set = model.objects.filter(order_ref=order)
            except:
                data_set = model.objects.filter(order=order)
            for data in data_set:
                write_data(csvwriter, data)
                data_to_return.append(data)
        if not data_to_return:
            write_none(csvwriter)
        return data_to_return

    def handle_data_from_abandoned_carts(carts, title, model, csvwriter):
        write_title(csvwriter, title)
        write_headers(csvwriter, model)
        data_to_return = []
        for cart in carts:
            data_set = model.objects.filter(checkout=cart)
            for data in data_set:
                write_data(csvwriter, data)
                data_to_return.append(data)
        if not data_to_return:
            write_none(csvwriter)

    def handle_data_from_refunds(refunds, title, model, csvriter):
        write_title(csvwriter, title)
        write_headers(csvwriter, model)
        data_to_return = []
        for refund in refunds:
            try:
                data_set = model.objects.filter(refund=refund)
            except:
                data_set = model.objects.filter(refund_ref=refund)
            for data in data_set:
                write_data(csvwriter, data)
                data_to_return.append(data)
        if not data_to_return:
            write_none(csvwriter)

    def post(self, request):
        data = request.body
        shop_id = data['shop_id']
        shop_url = data['shop_domain']
        customer = data['customer']
        orders = data['orders_to_redact']
        shopify_customers = Integrations_Shopify_Customer.objects.filter(
            email=customer['email'])
        from_customer = {
            'Customer_Address': Integrations_Shopify_Customer_Address,
            'Orders': Integrations_Shopify_Order,
            'Abandoned_Checkout': Integrations_Shopify_Abandoned_Checkouts
        }
        from_abandoned_carts = {
            'Abandoned_Checkout_Line_Items': Integrations_Shopify_Abandoned_Checkout_Line_Items
        }
        from_orders = {
            'Refunds': Integrations_Shopify_Refund,
            'Line_Items': Integrations_Shopify_Line_Item,
            'Transactions': Integrations_Shopify_Transaction,
            'Shipping_Line': Integrations_Shopify_Shipping_Line,
            'Discount_Application': Integrations_Shopify_Discount_Application,
            'Discount_Code': Integrations_Shopify_Discount_Code,
            'Fulfillment': Integrations_Shopify_Fulfillment

        }
        from_refunds = {
            'Refund_Order_Adjustments': Integrations_Shopify_Refund_Order_Adjustment,
            'Refund_Line_Items': Integrations_Shopify_Refund_Line_Item,
        }
        csvfile = StringIO()
        csvwriter = writer(csvfile)
        write_title(csvwriter, 'Customer')
        write_headers(csvwriter, Integrations_Shopify_Customer)
        for shopify_customer in shopify_customers:
            write_data(csvwriter, shopify_customer)

        # Handle Data With Customer FK
        for customer_item in from_customer:
            from_dependant = handle_data_from_customer(
                shopify_customers, customer_item, from_customer[customer_item], csvwriter)
            if customer_item == 'Orders':
                for order_item in from_orders:
                    from_second_dependant = handle_data_from_order(
                        from_dependant, order_item, from_orders[order_item], csvwriter)
                    if order_item == 'Refunds':
                        for refund_item in from_refunds:
                            handle_data_from_refunds(
                                from_second_dependant, refund_item, from_refunds[refund_item], csvwriter)
            elif customer_item == 'Abandoned_Checkout':
                for abandoned_cart_item in from_abandoned_carts:
                    handle_data_from_abandoned_carts(
                        from_dependant, abandoned_cart_item, from_abandoned_carts[abandoned_cart_item], csvwriter)
        csvfile.close
        send_gdpr_email(csvfile, customer['email'])
        return HttpResponse(status='200')
