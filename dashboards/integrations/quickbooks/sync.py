from allauth.socialaccount.models import SocialApp
from datetime import datetime
from django.utils import timezone

from intuitlib.client import AuthClient
from intuitlib.exceptions import AuthClientError

import logging
import requests
import socket
import urllib


logger = logging.getLogger(__name__)


def refresh(auth_params):
    app = SocialApp.objects.get(provider='quickbooks') 

    if socket.gethostname().startswith('dev'):
        DJANGO_HOST = "dev.blocklight.io"
    elif socket.gethostname().startswith('local'):
        DJANGO_HOST = "localhost:8000"
    else:
        DJANGO_HOST = "blocklight.io"

    auth_client = AuthClient(
        app.client_id,
        app.secret,
        redirect_uri='https://'+DJANGO_HOST+'/quickbooks/login/callback/',
        environment="sandbox",
        refresh_token=auth_params["refresh_token"],
    )

    try:
        auth_client.refresh()
    except AuthClientError as e:
        print(e.status_code)
        print(e.intuit_tid)
    return auth_client

def qbo_api_call(access_token, realm_id, key, lower_limit, upper_limit):
    lower_limit = str(lower_limit)[:10]
    upper_limit = str(upper_limit)[:10]
    

    base_url = "https://sandbox-quickbooks.api.intuit.com"
    
    routes = {
        'CompanyInfo': '/v3/company/{0}/companyinfo/{0}'.format(realm_id),
        'Account': '/v3/company/{0}/query?query={1}&minorversion=53'.format(realm_id, urllib.parse.quote("select * from Account where MetaData.CreateTime >= '"+lower_limit+"' and MetaData.CreateTime <= '"+upper_limit+"'")),
        'Bill': '/v3/company/{0}/query?query={1}&minorversion=53'.format(realm_id, urllib.parse.quote("select * from bill where MetaData.CreateTime >= '"+lower_limit+"' and MetaData.CreateTime <= '"+upper_limit+"'")),
        'Ledger': '/v3/company/{0}/reports/GeneralLedger?start_date={1}&end_date={2}'.format(realm_id, urllib.parse.quote(lower_limit), urllib.parse.quote(upper_limit)),
        'LedgerCrawl': '/v3/company/{0}/reports/GeneralLedger?date_macro={1}'.format(realm_id, urllib.parse.quote(upper_limit))
    }

    auth_header = 'Bearer {0}'.format(access_token)
    headers = {
        'Authorization': auth_header,
        'Accept': 'application/json'
    }
    print(routes[key])
    return requests.get('{0}{1}'.format(base_url, routes[key]), headers=headers)

def save_quickbooks(integration=None, user=None, task_id=None):


    logger.debug("SYNC - QUICKBOOKS - {}".format(user))
    user_iden = user.id
    integration.set_sync_state(user_iden, 'quickbooks', task_id)
    auth_params = integration.build_auth_params('quickbooks', user)
    if auth_params != 'done':
        apis = integration.get_params(auth_params)
        auth_client = refresh(auth_params)
        for api in apis:
            name = api['name']
            data = api['data']
            # data parser 
            model = data['model']
            key = data['key']
            handler = data['handler']
            status = SyncQuickbooks(auth_params['initialize'], model, auth_params['pk'], name, handler, user_iden, auth_client, auth_params, key)
        return status

def SyncQuickbooks(initialize, model, pk, name, handler, user_iden, auth_client, auth_params, key):

    def Sync(data, pk, model, handler, name, now_time, user_iden, partition=None):
        table_handler = handler(data, pk, user_iden, 'quickbooks', name)
        table_handler.save_all_objects()
    
    ct_internal = len(model.objects.filter(integration_id=pk))
    now_time = timezone.now()
    oldest_record = datetime.isoformat(now_time)

    if ct_internal > 0:
        last_creation = datetime.isoformat(model.objects.filter(user_iden=user_iden).latest('create_time').create_time)
        data = qbo_api_call(auth_client.access_token, auth_params["realm_id"], key, last_creation, now_time)
        handler_data = data.json()
        if len(handler_data) > 0:
            Sync(handler_data, pk, model, handler, name, now_time, user_iden)
        try:
            oldest_record = datetime.isoformat(model.objects.filter(user_iden=user_iden).exclude(create_time=None).order_by('create_time')[0].create_time)
        except Exception as e:
            oldest_record = now_time

    print('crawl')
    data = qbo_api_call(auth_client.access_token, auth_params["realm_id"], key, '2015-01-01', oldest_record)
    handler_data = data.json()
    if len(handler_data) > 0:
        Sync(handler_data, pk, model, handler, name, now_time, user_iden)
    
    return 'success'
