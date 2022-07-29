import abc
from allauth.socialaccount.models import SocialAccount, SocialToken
import base64
from datetime import timedelta
from dashboards.models import Integrations_User_LastSync, BasicAuthRecords, Integrations_UserSettings
from django.utils import timezone
import logging
import socket
import traceback


ODDBALLS = ['shipstation']

if socket.gethostname().startswith('dev'):
    DJANGO_HOST = "development"
elif socket.gethostname().startswith('www'):
    DJANGO_HOST = "production"
else:
    DJANGO_HOST = "localhost"

logger = logging.getLogger(__name__)


class Integration(abc.ABC):

    @abc.abstractmethod
    def get_task(self, user):
        pass

    @abc.abstractmethod
    def get_params(self, **kwargs):
        pass

    @abc.abstractmethod
    def set_sync_state(self, user_id, integration_name, celery_id):
        """

        Args:
            user_id:
            integration_name:
            celery_id:

        Returns:

        """
        try:
            last_sync, created = Integrations_User_LastSync.objects.get_or_create(user_iden=user_id,
                                                                                  integration_name=integration_name,
                                                                                  checkpoint=2)
        except Integrations_User_LastSync.MultipleObjectsReturned:
            last_sync, created = Integrations_User_LastSync.objects.filter(user_iden=user_id,
                                                                           integration_name=integration_name,
                                                                           checkpoint=2)[0], None
        last_sync.celery_key = celery_id
        if created:
            last_sync.initialize = True
        else:
            last_sync.initialize = False
        last_sync.last_sync_time = timezone.now()
        last_sync.save()

    # TODO: Revisit this logic and segregate it among children
    @abc.abstractmethod
    def build_auth_params(self, integration_name, user):
        user_iden = user.id
        ints = [integration_name]

        for integration_name in ints:
            last_sync = self.checkLastSync(user_iden, integration_name, 2)
            initialize = last_sync['initialize']
            should_sync = last_sync['should_sync']
            last_sync_time = last_sync['last_sync_time']
            # changeSyncState(START_STATE, integration_name, request)
            state = should_sync
            if integration_name not in ODDBALLS:
                if len(integration_name) == len(integration_name.replace('_celery', '')):
                    try:
                        django = SocialAccount.objects.get(
                            provider=integration_name, user_id=user_iden)
                    except SocialAccount.DoesNotExist as e:
                        logger.error(
                            "Following error occurred when trying to retrieve social account object for integration " + integration_name + " of user " + str(
                                user))
                        logger.error(traceback.print_exc())
                        raise e
                    pk = django.id
                    # Google doesn't use access_token
                    if integration_name == 'google':
                        to_return = \
                            {'pk': pk, 'django': django,
                             'integration_name': integration_name, 'user': user,
                             'user_iden': user_iden, 'initialize': initialize, 'last_sync_time': last_sync_time}
                    elif integration_name == 'quickbooks':
                        account_info = SocialAccount.objects.get(
                            user_id=user_iden, provider="quickbooks")

                        token = account_info.socialtoken_set.first()

                        # pull extra data
                        extra_data = account_info.extra_data
                        code = extra_data["code"]
                        access_token = extra_data["access_token"]
                        realm_id = extra_data["realm_id"]
                        refresh_token = extra_data["refresh_token"]

                        to_return = \
                            {"code": code, 'token': token, "access_token": access_token, "realm_id": realm_id, 'pk': pk,
                             'django': django, 'integration_name': integration_name, 'user': user,
                             'user_iden': user_iden, 'initialize': initialize, 'last_sync_time': last_sync_time,
                             "refresh_token": refresh_token}
                    else:
                        access_token = SocialToken.objects.get(account__user=user,
                                                               account__provider=integration_name).token
                        to_return = \
                            {'access_token': access_token, 'pk': pk, 'django': django,
                             'integration_name': integration_name, 'user': user,
                             'user_iden': user_iden, 'initialize': initialize, 'last_sync_time': last_sync_time}
                    return to_return

                else:
                    access_token = SocialToken.objects.get(account__user=user,
                                                           account__provider=integration_name).token
                    to_return = \
                        {'access_token': access_token, 'pk': pk, 'django': django,
                         'integration_name': integration_name, 'user': user,
                         'user_iden': user_iden, 'initialize': initialize, 'last_sync_time': last_sync_time}
                return to_return
            else:
                # ODDBALLS ARE APIs THAT ONLY SUPPORT BASICAUTH (NOT OAUTH OR OATH2)
                if integration_name == 'shipstation':
                    keys_data = BasicAuthRecords.objects.get(
                        integration_name='shipstation', user_iden=user_iden)
                    api_key = keys_data.api_key
                    api_secret = keys_data.api_secret
                    keySecret = api_key + ':' + api_secret
                    base64auth_string = str(base64.b64encode(
                        keySecret.encode('utf-8')), 'utf-8')
                    _initTable, created = BasicAuthRecords.objects.get_or_create(
                        integration_name='shipstation', user_iden=user_iden)
                    _initTable.integration_name = integration_name
                    _initTable.user_iden = user_iden
                    _initTable.api_key = api_key
                    _initTable.api_secret = api_secret
                    _initTable.base64auth_string = base64auth_string
                    _initTable.save()
                    auth_record = BasicAuthRecords.objects.get(
                        integration_name='shipstation', user_iden=user_iden)
                    base64auth_string = auth_record.base64auth_string
                    # search_time = timezone.now() - timedelta(days=1825)
                    return {'auth_record': auth_record, 'base64auth_string': base64auth_string,
                            # 'search_time': search_time,
                            'initialize': initialize, 'integration_name': integration_name, 'user': user,
                            'user_iden': user_iden, 'initialize': initialize, 'last_sync_time': last_sync_time}

    def checkLastSync(self, user_iden, integration_name, checkpoint):
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
            check_stuck_syncs = Integrations_User_LastSync.objects.get(integration_name=integration_name,
                                                                       user_iden=user_iden, checkpoint=checkpoint,
                                                                       sync_is_active=True)
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
                return {'initialize': False, 'should_sync': False, 'sync_is_active': True,
                        'last_sync_time': 'syncing_now'}
            # Else, continue
            else:
                prior_syncs = Integrations_User_LastSync.objects.filter(integration_name=integration_name,
                                                                        user_iden=user_iden, checkpoint=checkpoint)[0]
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
