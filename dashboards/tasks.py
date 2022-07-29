from __future__ import print_function

from celery import group, shared_task, chain
from celery.result import AsyncResult
from blocklight.celery import app
from collections import defaultdict
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
from dashboards.integrations.integrationFactory import factory

from dashboards.models import Integrations_UserSettings, Integrations_User_LastSync, TimeLine_Entry
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.handlers.wsgi import WSGIRequest
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.test import RequestFactory
import logging
from blocklight_api.views.timeline_views import TimeLineView
from django.http import HttpRequest
from django.utils import datastructures
import collections
from django.db import transaction
from .models import UserProfile
from datetime import timedelta, date


logger = logging.getLogger(__name__)


# TODO: Used in views.py for manual sync. Need to check if we still need it.
def checkIfNoActiveSync(user_iden, integration_name):
    """
        Check if there are no active sync tasks occuring
    Args:
        user_iden:
        integration_name:

    Returns:
        True if there is no current sync task (Celery), false otherwise
    """

    try:
        last_sync = Integrations_User_LastSync.objects.get(
            user_iden=user_iden, integration_name=integration_name)
        result = AsyncResult(id=last_sync.celery_key)
        status = result.status
    except:
        return True

    if status in ["STARTED", "PENDING", "RETRY"]:
        return False
    else:
        return True
    # initialize = Integrations_User_LastSync.objects.filter(user_iden=user_iden, initialize=True,
    #                                                        integration_name=integration_name).count()
    # sync_is_active = Integrations_User_LastSync.objects.filter(user_iden=user_iden, sync_is_active=True,
    #                                                            integration_name=integration_name).count()
    # if initialize == 1 or sync_is_active == 1:
    #     return False
    # else:
    #     return True


def get_integration_sync_task(user_iden, integration_name):

    integration = factory.get_integration(integration_name)
    user = User.objects.get(id=user_iden)

    # TODO tcount is not being used, remove it
    task, tcount = integration.get_task(user)

    # task_message = 'Syncing data integrations...'
    return task.si(integration, user)


def sync_users_integrations(users_integrations):
    """
    Run integrations for provided list of users and integrations
    :param users_integrations: list of tuples (user_iden, [<integrations>])
    """

    # Run the synchronization tasks in parralel but per user in serial
    # NOTE: If two sync tasks for same integration runs in parralel they cause a mysql deadlock
    for user_iden, user_integrations in users_integrations:
        group(get_integration_sync_task(user_iden, integration_name)
              for integration_name in user_integrations).delay()

    # TODO: this would be probably better. I'm not sure if the previous solution runs the groups in serial,
    #        but it solved the mysql deadlocks, so it'f fine for now.
    #      The problem with chain is that it stops on first failed group
    #        and we don't won't it to stop on failure of any group.
    # chain(*(
    #     chord((get_integration_sync_task(user_iden, integration_name) for integration_name in user_integrations), pass_task.si())
    #     for user_iden, user_integrations in users_integrations.items())
    # ).delay()


def user_sync_on_integration(user_iden, integration_names):
    tasks = []
    for integration in integration_names:
        tasks.append(get_integration_sync_task(user_iden, integration))
    group1 = group(*tasks)
    user = User.objects.get(id=user_iden)
    timeline_task = consolidate_user_timeline.si(user, True)
    group1.delay()
    timeline_task.apply_async(countdown=60)


@shared_task(name='sync_all_integrations_data')
def sync_all_integrations_data():
    """
    This is a function which collects all current integrations of users and run sync tasks for them.
    There is data inconsistenci between info about integrations and actual users. Just the intersection
    of this data is used.
    The function is meant to be run as a periodic celery task, does not include Facebook or Instagram
    """

    # TODO: currently we need to filter the Integrations_UserSettings by auth..User becouse of inconsistent data
    #       There are user_id in the Integrations_UserSettings of the users which does not exists
    users_integrations = defaultdict(list)
    for user_setting in Integrations_UserSettings.objects.filter((~Q(
            integration_name='facebook') & ~Q(integration_name='instagram')),
        user_iden__in=User.objects.values_list('id'),
    ).values('user_iden', 'integration_name'):

        users_integrations[user_setting['user_iden']].append(
            user_setting['integration_name'])

    sync_users_integrations(users_integrations.items())


def get_timeline(request: WSGIRequest) -> dict:
    tl_view = TimeLineView()
    tl_view.request = request
    response = tl_view.list(request).data
    return response


def clean_ordered_dict(od: collections.OrderedDict) -> dict:
    newd = dict(od)
    for k, v in newd.items():
        if isinstance(v, collections.OrderedDict):
            newd[k] = clean_ordered_dict(v)
        if isinstance(v, list):
            for i, subentry in enumerate(v):
                if isinstance(subentry, collections.OrderedDict):
                    v[i] = clean_ordered_dict(subentry)
            newd[k] = v

    return newd


def process_timeline_page_data(timeline_page: list, user: User):
    with transaction.atomic():
        for entry in timeline_page:
            if entry['src'] != 'shopify':
                account = SocialAccount.objects.get(
                    provider=entry['src'], user_id=user.id)
            else:
                account_id = entry['data'].get('integration_id', None)
                if not account_id:
                    account = None
                else:
                    account = SocialAccount.objects.get(
                        id=account_id)
            if account:

                entry_model, created = TimeLine_Entry.objects.update_or_create(
                    id=entry['entry_id'],
                    defaults={
                        'insight': entry['insight'],
                        'integration': account,
                        'data': clean_ordered_dict(entry['data']),
                        'ts': entry['ts'],
                        'user': user
                    }
                )


def group_timeline_tasks(should_crawl=True):
    users = User.objects.all()
    tasks = []
    for user in users:
        user_tl_task = consolidate_user_timeline.si(user, should_crawl)
        tasks.append(user_tl_task)
    return tasks


@shared_task(name='consolidate_user_timeline')
def consolidate_user_timeline(user: User, should_crawl: bool):
    pg = 1
    inc_limit = 10
    max_limit = 50
    # keep going if we should crawl ,if we shouldnt keep going till we hit our page limit

    while (should_crawl or pg <= inc_limit and (pg <= max_limit)):
        request = RequestFactory().get(f'/?page={pg}')
        request.user = user
        response = get_timeline(request)
        data = response['results']

        process_timeline_page_data(data, user)
        print(response['next'])
        pg += 1

        if not response['next']:
            break


@shared_task(name='consolidate_timeline_head')
def consolidate_timeline_head():
    tasks = group_timeline_tasks(should_crawl=False)
    group(tasks).delay()
    print("testing consolidate")


@shared_task(name='consolidate_full_timeline')
def consolidate_full_timeline():
    tasks = group_timeline_tasks(should_crawl=True)
    group(tasks).delay()
    print("testing consolidate")


@ shared_task(name='sync_all_fb_ig_data')
def sync_all_fb_ig_data():
    """
    This is a function which collects all current integrations of users and run sync tasks for them.
    There is data inconsistenci between info about integrations and actual users. Just the intersection
    of this data is used.
    The function is ment to be run as a periodic celery task., does not include facebook or instagram
    """
    # TODO: currently we need to filter the Integrations_UserSettings by auth..User becouse of inconsistent data
    #       There are user_id in the Integrations_UserSettings of the users which does not exists
    users_integrations = defaultdict(list)
    for user_setting in Integrations_UserSettings.objects.filter((Q(
            integration_name='facebook') | Q(integration_name='instagram')),
        user_iden__in=User.objects.values_list('id'),
    ).values('user_iden', 'integration_name'):
        users_integrations[user_setting['user_iden']].append(
            user_setting['integration_name'])

    sync_users_integrations(users_integrations.items())


@app.task(name='send_birthday_email')
def send_birthday_email():
    today = date.today()
    user_profiles = UserProfile.objects.filter(
        birthday__month=today.month,
        birthday__day=today.day,
    )
    for user_profile in user_profiles:
        try:
            user = User.objects.get(id=user_profile.user_id)
            subject = f'Happy Birthday, {user.first_name}!'
            html_message = render_to_string('account/email/birthday_email.html', {
                'user': user,
            })
            message = strip_tags(html_message)
            send_mail(subject, message, None, [
                      user.email], True, html_message=html_message)

        except Exception as e:
            logger.exception(e)
            raise e


@app.task(name='send_onboarding_email')
def send_onboarding_email():
    def send_email(users, subject, template):
        for user in users:
            try:
                html_message = render_to_string(template, {
                    'user': user,
                })
                message = strip_tags(html_message)
                send_mail(subject, message, None, [
                          user.email], True, html_message=html_message)

            except Exception as e:
                logger.exception(e)
                raise e

    templates = {
        1: ('Integrations', 'account/email/onboarding_integration.html'),
        2: ('Dashboards', 'account/email/onboarding_dashboards.html'),
        3: ('Homepage', 'account/email/onboarding_homepage.html')
    }

    today = date.today()
    for num_days in templates:
        join_date = today - timedelta(num_days)
        users = User.objects.filter(date_joined__contains=join_date)
        subject_type, template = templates[num_days]
        subject = f'Getting to know Blocklight: {subject_type}'
        try:
            send_email(users, subject, template)
        except Exception as e:
            raise e
