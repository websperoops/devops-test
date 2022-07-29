from __future__ import print_function

from requests.api import get

from celery import shared_task, group

from dashboards.integrations.facebook_instagram.instagram import ig_api
from dashboards.integrations.facebook_instagram.utils import fb_ig
from dashboards.integrations.utils import create_integration_logger

from django.utils import timezone
import requests
import time


logger = create_integration_logger(__name__, "instagram")


def save_instagram(integration, user):
    RESULTS = []
    try:
        logger.info(f"SYNC - INSTAGRAM- {user}")

        auth_params = integration.build_auth_params('instagram', user)
        user_iden = user.id
        if auth_params != 'done':

            apis_n_stuff = integration.get_params(auth_params)
            apis = apis_n_stuff['apis']
            access_token = apis_n_stuff['access_token']
            response_body = apis_n_stuff['response_body']
            try:
                data = response_body['data']
            except:
                data = []

            for entries in data:

                for api in apis:
                    name = api['name']
                    data = api['data']
                    API = data["API"]
                    model = data['model']
                    integration_name = data['integration_name']
                    key = data['key']
                    handler = data['handler']
                    timestamp_field = data['timestamp_field']
                    api_type = data['api-type']
                    page_key = data['page-key']
                    result = Sync_Ig_Insight.si(auth_params['initialize'], access_token, auth_params['user_iden'], name, model, API,
                                                integration_name, key, auth_params['pk'], entries['name'], entries['id'], handler, timestamp_field, api_type, page_key)
                    RESULTS.append(result)

        group(RESULTS).delay()

    except Exception as e:
        logger.exception(e)
        raise e

    return 'done'


def Sync(api_type, handler, data, pk, user_iden, key, account_name, model=None):
    begin = time.time()
    if api_type == 'insight':
        table_handler = handler(data, pk, user_iden, key, account_name, model)
        table_handler.save_all_objects()
    elif api_type == 'media':
        table_handler = handler(data, pk, user_iden, key, account_name, False)
        table_handler.save_all_objects()
    elif api_type == 'story':
        table_handler = handler(data, pk, user_iden, key, account_name, True)
        table_handler.save_all_objects()
    else:
        pass
    return time.time() - begin

    
def make_api_call(until, since, period, API, api_type, handler, pk, user_iden, key, account_name, model, total_time, syncs, ts_field, name):
    until = str(int(until.timestamp()))
    since = str(int(since.timestamp()))
    response = API(period=period, since=since, until=until)
    data = response["data"]
    init_elapsed = Sync(api_type, handler, data, pk,
                        user_iden, key, account_name, model)
    total_time += init_elapsed
    syncs += 1
    avg_time = total_time / syncs

    oldest_date = getattr(model.objects.filter(
        user_iden=user_iden).earliest(ts_field), ts_field, None)
    if oldest_date:
        oldest_date -= timezone.timedelta(days=1)

@shared_task(time_limit=3600, name="Sync_Ig_Insight")
def Sync_Ig_Insight(initialize, access_token, user_iden, name, model, API, integration_name, key, pk, account_name, page_id, handler, ts_field, api_type, page_key):

    CRAWL = True
    MAX_TIME = 900
    START_TIME = time.time()
    ct_internal = model.objects.filter(user_iden=user_iden).count()
    total_time = 0
    syncs = 0
    avg_time = 0

    ig_api.IG_API(page_id, access_token)

    period = 'day'

    oldest_date = None

    today = timezone.now()
    if name == "ig_follower_count":
        logger.info("------ FOLLOWER COUNT SUBMITTED -----")
        most_recent_date = today - timezone.timedelta(days=30)
        make_api_call(today, most_recent_date, period, API, api_type, handler, pk, user_iden, key, account_name, model, total_time, syncs, ts_field, name)
        return "success"
    ## GRAB NEW DATA IF DATA EXISTS #####################
    if ct_internal > 0:
        most_recent_date = getattr((model.objects.filter(user_iden=user_iden).latest(
            ts_field)), ts_field, None)    
        make_api_call(today, most_recent_date, period, API, api_type, handler, pk, user_iden, key, account_name, model, total_time, syncs, ts_field, name)
        oldest_date = getattr((model.objects.filter(user_iden=user_iden).earliest(
            ts_field)), ts_field, None)
    ## CRAWL DATA FROM OLDEST RECORD OR FROM TODAY IF NO RECORDS EXIST ##################
    if CRAWL:
        logger.info("-----CRAWLING-----")

        if oldest_date:
            ceiling = oldest_date
        else:
            ceiling = timezone.now()

        two_yrs_ago = timezone.now() - timezone.timedelta(days=2*365)
        floor = two_yrs_ago
        if ceiling <= two_yrs_ago:
            return "success"

        floor = str(int(floor.timestamp()))
        ceiling = str(int(ceiling.timestamp()))
        response = API(period=period, since=floor, until=ceiling)
        data = response["data"]
        if api_type == 'insight' and len(data) > 0:
            keep_going = fb_ig.is_insight_data_within_two_years(data)
        elif api_type == 'media' or api_type == 'story' and len(data) > 0:
            keep_going = fb_ig.is_media_object_data_within_two_years(
                data, access_token)
        else:
            keep_going = False

        # "previous" in response["paging"] and
        while keep_going:
            if (int(time.time() - START_TIME)) + avg_time > MAX_TIME:
                return "to be continued"

            elapsed = Sync(api_type, handler, data, pk,
                           user_iden, key, account_name, model)
            total_time += elapsed
            syncs += 1
            avg_time = total_time / syncs

            try:
                next_page_url = response["paging"][page_key]
            except:
                break
            response = requests.get(next_page_url).json()

            if 'data' not in response:
                err_msg = str(response)
                limit_flag = 'last 2 years'
                if limit_flag in err_msg:
                    break
                else:
                    raise IOError(err_msg)

            else:
                data = response["data"]
                if api_type == 'insight' and len(data) > 0:
                    keep_going = fb_ig.is_insight_data_within_two_years(data)
                elif api_type == 'media' or api_type == 'story' and len(data) > 0:
                    keep_going = fb_ig.is_media_object_data_within_two_years(
                        data, access_token)
                else:
                    keep_going = False
    return "success"
