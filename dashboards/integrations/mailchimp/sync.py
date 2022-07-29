from django.db.models import Count
from datetime import datetime
from django.db import connection
from django.utils import timezone
import logging


logger = logging.getLogger(__name__)


def save_mailchimp(integration=None, user=None, task_id=None):

    logger.debug("SYNC - MAILCHIMP - {}".format(user))
    user_iden = user.id
    logger.debug('SAVE_MAILCHIMP----------------------------------------------------------')
    logger.debug(user)
    logger.debug(user_iden)
    integration.set_sync_state(user_iden, 'mailchimp', task_id)
    auth_params = integration.build_auth_params('mailchimp', user)
    if auth_params != 'done':
        apis = integration.get_params(auth_params)
        # // BEGIN LOOP THROUGH ENDPOINTS
        for api in apis:
            name = api['name']
            data = api['data']
            # data parser
            model = data['model']
            API = data['API']
            handler = data['handler']
            key = data['key']
            logger.debug('SAVE MAILCHIMP AUTH -----------------------------')
            logger.debug(auth_params['user_iden'])
            status = SyncMailchimp(auth_params['initialize'], model, API,
                         auth_params['pk'], name, handler, auth_params['user_iden'], key)

    return status


def SyncMailchimp(initialize, model, MailChimpAPI, pk, name, handler, user_iden, key):

    def Sync(data, pk, model, handler, name, now_time, user_iden, MailChimpAPI, partition=None):
            table_handler = handler(data, pk, user_iden, 'mailchimp', name)
            table_handler.save_all_objects()
    logger.debug('SAVE_MAILCHIMP USER IDEN----------------------------------------')
    logger.debug(user_iden)
    ct_internal = model.objects.filter(user_iden=user_iden).count()
    logger.info(f'Count Internal {ct_internal}')

    now_time = timezone.now()
    oldest_record = datetime.isoformat(now_time)
    
    if ct_internal > 0:
        last_creation = datetime.isoformat(model.objects.filter(user_iden=user_iden).latest('date_created').date_created)
        data = MailChimpAPI.all(count=1000, since_date_created=last_creation)
        handler_data = data.get(key,[])

        if len(handler_data) > 0:
            Sync(list(handler_data), pk, user_iden, handler, name, now_time, user_iden, MailChimpAPI)
        try:
            oldest_record = datetime.isoformat(model.objects.filter(user_iden=user_iden).exclude(date_created=None).order_by('date_created')[0].date_created)
        except Exception as e:
            oldest_record = now_time

    # Pagination Handler #
    logger.info('----- CRAWL -----')
    REQ_LIMIT = 250
    records_synced = 0
    total_items = 1
    while total_items >= 0:
        data = MailChimpAPI.all(count=REQ_LIMIT, offset=records_synced, before_date_created=oldest_record)
        total_items = data.get('total_items', 0)
        handler_data = data.get(key,[])
        if len(handler_data) > 0:
            Sync(list(handler_data), pk, model, handler, name, now_time, user_iden, MailChimpAPI)
        total_items -= records_synced
        records_synced += REQ_LIMIT

    return 'success'