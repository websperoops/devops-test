from __future__ import print_function, absolute_import

from dashboards.models import Integrations_User_LastSync, Integrations_UserSettings
from datetime import timedelta
from django.utils import timezone
import logging
import socket


global DJANGO_HOST


logger = logging.getLogger(__name__)


if socket.gethostname().startswith('dev'):
    DJANGO_HOST = "development"
elif socket.gethostname().startswith('www'):
    DJANGO_HOST = "production"
else:
    DJANGO_HOST = "localhost"


def checkLastSync(user_iden, integration_name, checkpoint):
    """
    Checks the last time an integration was synced for the user.

    Args:
        user_iden: id of user
        integration_name: name of integration to which check
        checkpoint:

    Returns:
        A dictionary with the following fields:
        {'``should_sync``': boolean value indicating whether a sync should occur,
        '``initialize``': boolean value indicating whether the user is sync first time,
        '``sync_is_active``': boolean value indicating if a sync is currently in progress,
        '``last_sync_time``': datatime object indicated last time the integration was synced.
    """

    # Number of seconds between syncs
    check_user_sync_settings = Integrations_UserSettings.objects.filter(user_iden=user_iden,
                                                                        integration_name=integration_name)

    # Eric turned off printing temporarily
    verbose = False and (DJANGO_HOST == 'localhost')

    if len(check_user_sync_settings) > 0:

        check_user_sync_settings = Integrations_UserSettings.objects.filter(user_iden=user_iden,
                                                                            integration_name=integration_name).last()

        user_sync_timer = check_user_sync_settings.autosync_timer
        seconds = int(user_sync_timer.split('_')[-1])
        minutes = user_sync_timer.split('_')[-2]
        minutes = int(minutes.split('_')[-1])
        minutes = minutes * 60
        hours = user_sync_timer.split('_')[-3]
        hours = int(hours)
        hours = hours * 3600
        days = user_sync_timer.split('_')[-4]
        days = int(days)
        days = days * 86400
        time_between_syncs = seconds + minutes + hours + days
    else:
        time_between_syncs = 5 * 60

    if verbose:
        print('time_between_syncs =', time_between_syncs)

    # ints = ['facebook', 'facebook_celery', 'instagram', 'instagram_celery']
    # if integration_name in ints:
    #     # time_between_syncs = 86400
    #     time_between_syncs = 300
    #     if verbose:  print('facebook syncs only 1x per day')
    #     # return {'initialize': False, 'should_sync': False, 'sync_is_active': False, 'last_sync_time': 'Never'}

    prior_syncs = Integrations_User_LastSync.objects.filter(
        integration_name=integration_name, user_iden=user_iden)
    prior_count = len(prior_syncs)

    # CHECK / REMOVE STUCK SYNC PROCESSES
    if not integration_name == 'facebook':
        probably_stuck_time = 600
    else:
        probably_stuck_time = 3600

    check_stuck_syncs = Integrations_User_LastSync.objects.filter(integration_name=integration_name,
                                                                  user_iden=user_iden,
                                                                  checkpoint=checkpoint, sync_is_active=True)
    if len(check_stuck_syncs) > 0:
        check_stuck_syncs = Integrations_User_LastSync.objects.filter(integration_name=integration_name,
                                                                      user_iden=user_iden, checkpoint=checkpoint,
                                                                      sync_is_active=True).first()
        might_be_stuck_sync_time = check_stuck_syncs.last_sync_time
        # Check if we need to sync
        is_stuck = (timezone.now(
        ) - might_be_stuck_sync_time) > timedelta(seconds=probably_stuck_time)
        if is_stuck:
            check_stuck_syncs.sync_is_active = False
            check_stuck_syncs.initialize = False
            check_stuck_syncs.save()
        else:
            if verbose:
                print('no stuck sync processes')

    ##################################
    # Proceed based on previous syncs
    ##################################
    # If user has never synced
    if prior_count == 0:
        if DJANGO_HOST == 'localhost':
            print(
                ('User %s, Integration: %s, Never synced!') % (user_iden, integration_name))
        return {'initialize': True, 'should_sync': True, 'sync_is_active': False, 'last_sync_time': 'Never'}
    # If user has synced at least once
    elif prior_count > 0:
        if DJANGO_HOST == 'localhost':
            print(
                ('User %s, Integration: %s, Prior count: %d') % (user_iden, integration_name, prior_count))
        # Check if there is a sync currently active
        check = len(Integrations_User_LastSync.objects.filter(user_iden=user_iden, sync_is_active=True,
                                                              integration_name=integration_name))
        sync_is_active = check
        # If so, return
        if sync_is_active > 0:
            return {'initialize': False, 'should_sync': False, 'sync_is_active': True, 'last_sync_time': 'syncing_now'}
        # Else, continue
        else:
            prior_syncs = Integrations_User_LastSync.objects.filter(integration_name=integration_name,
                                                                    user_iden=user_iden, checkpoint=checkpoint).first()
            last_sync_time = prior_syncs.last_sync_time
            # Check if we need to sync
            should_sync = (
                timezone.now() - last_sync_time) > timedelta(seconds=time_between_syncs)
            # Return with appropriate values
            if DJANGO_HOST == 'localhost':
                print(
                    ('User %s, Integration: %s, Should sync: %r') % (
                        user_iden, integration_name, should_sync),
                    ' time_between_syncs = ', time_between_syncs)
            # change to should_sync
            return {'should_sync': should_sync, 'initialize': False, 'sync_is_active': sync_is_active,
                    'last_sync_time': last_sync_time}
