from __future__ import print_function

from celery import shared_task, group

from dashboards.integrations.facebook_instagram.facebook import fb_api
from dashboards.integrations.facebook_instagram.utils import fb_ig
from dashboards.integrations.utils import create_integration_logger, Handler
from dashboards.integrations.utils.dashboard_sync_complete import token_failure

from django.utils import timezone
import requests
import time


logger = create_integration_logger(__name__, "facebook")
logger.info("working")


def save_facebook(integration, user):

    RESULTS = []
    logger.info("SYNC - FACEBOOK - {}".format(user))
    auth_params = integration.build_auth_params('facebook', user)
    user_iden = user.id
    if auth_params != 'done':
        apis_n_stuff = integration.get_params(auth_params)
        apis = apis_n_stuff['apis']
        access_token = apis_n_stuff['access_token']
        response_body = apis_n_stuff['response_body']
        data = response_body.get('data', [])

        logger.info("Facebook API Response Body for User's Facebook Accounts:\n{}\n".format(
            str(response_body)))
        logger.info(
            "Facebook API Response Body DATA for User's Facebook Accounts:\n{}\n".format(str(data)))
        print('----------------------------------------------------------------------')
        if 'error' in response_body:
            print(response_body['error']['type'])
            if response_body['error']['type'] == 'OAuthException':
                token_failure('facebook', user.id)
                print('TOKEN FAILED')
                return 'failed'

        for entries in data:
            for api in apis:
                name = api['name'],
                data = api['data']
                API = data['API']
                model = data['model']
                integration_name = data['integration_name']
                key = data['key']
                handler = data["handler"]
                api_type = data['api-type']
                ts_field = data['timestamp_field']
                page_key = data['page-key']

                result = Sync_Fb_Insight.si(auth_params['initialize'], access_token, auth_params['user_iden'], name, model, API,
                                            integration_name, key, auth_params['pk'], entries['name'], entries['id'], handler, api_type, ts_field, page_key)
                RESULTS.append(result)

    logger.info("# of subtasks spawned", (len(RESULTS)))
    group(RESULTS).delay()

    return 'done'


def sync_response(handler, data, pk, user_iden, key, account_name, model):
    Handler.logger = logger
    logger.info("SYNCING RESPONSE FROM FB API:")
    logger.info("# of Top-Level records in response:\n{}\n".format(len(data)))
    begin = time.time()
    table_handler = handler(data, pk, user_iden, key, account_name, model)
    table_handler.save_all_objects()
    return int(time.time() - begin)


@shared_task(time_limit=3600, name="Sync_Fb_Insight")
def Sync_Fb_Insight(initialize, access_token, user_iden, name, model, API, integration_name, key, pk, account_name, page_id, handler, api_type, ts_field, page_key):
    START_TIME = time.time()
    MAX_TIME = 900  # 15 minutes
    CRAWL = True
    syncs = 0
    total_time = 0
    avg_time = 0

    logger.info("User task for {}".format(user_iden))
    logger.info("Task description: {}".format(str(model)))

    ct_internal = model.objects.filter(user_iden=user_iden).count()
    period = 'day'
    oldest_date = None
    fb_api.FB_API(page_id, access_token)

    today = timezone.now()
    oldest_date = None

    if ct_internal > 0:

        # We want the day after our most recent as the start
        most_recent_date = getattr(model.objects.filter(
            user_iden=user_iden).latest(ts_field), ts_field)

        if most_recent_date >= today:
            most_recent_date = today - timezone.timedelta(hours=1)

        logger.info("Most recent {}".format(
            str(most_recent_date.strftime("%m/%d/%Y, %H:%M:%S"))))
        logger.info("Today {}".format(
            str(today.strftime("%m/%d/%Y, %H:%M:%S"))))

        today = str(int(today.timestamp()))
        most_recent_date = str(int(most_recent_date.timestamp()))

        response = API(period=period, since=most_recent_date, until=today)
        data = response["data"]
        init_elapsed = sync_response(
            handler, data, pk, user_iden, key, account_name, model)
        total_time += init_elapsed
        syncs += 1
        avg_time = total_time / syncs

        oldest_date = getattr(model.objects.filter(
            user_iden=user_iden).earliest(ts_field), ts_field, None)
        logger.info("oldest date for {}:{}".format(
            name[0], str(oldest_date.strftime("%m/%d/%Y, %H:%M:%S"))))
        if oldest_date:
            oldest_date -= timezone.timedelta(days=1)
        logger.info(str(oldest_date))

    if CRAWL:
        logger.info("-----CRAWLING-----")

        if oldest_date:
            ceiling = oldest_date

        else:
            ceiling = timezone.now()

        two_yrs_ago = timezone.now() - timezone.timedelta(days=2*365)
        if ceiling <= two_yrs_ago:
            logger.info("-----FINISHED CRAWLING-------")
            logger.info("Total_time: {}".format(total_time))
            logger.info("Avg Handler Time: {}".format(avg_time))
            return "success"
        floor = ceiling - timezone.timedelta(days=(3*30))

        logger.info("ceiling", ceiling)
        logger.info("floor", floor)

        since = str(int(floor.timestamp()))
        until = str(int(ceiling.timestamp()))

        response = API(period=period, since=since, until=until)

        data = response["data"]
        if api_type == 'insight' and len(data) > 0:
            keep_going = fb_ig.is_insight_data_within_two_years(data)
            logger.info(keep_going)
        elif api_type == 'post' and len(data) > 0:
            keep_going = fb_ig.is_fb_post_data_within_two_years(data)
            logger.info(keep_going)
        else:
            keep_going = True

        while keep_going:
            if (int(time.time() - START_TIME)) + avg_time > MAX_TIME:
                logger.info("-----CRAWL CUTOFF FROM MAX TIME------")
                logger.info("Total_time: {}".format(total_time))
                logger.info("Avg Handler Time: {}".format(avg_time))
                return "to be continued"

            logger.info("LOOPING")
            elapsed = sync_response(
                handler, data, pk, user_iden, key, account_name, model)
            total_time += elapsed
            syncs += 1
            avg_time = total_time / syncs

            if page_key == 'manual':
                ceiling = floor
                floor = ceiling - timezone.timedelta(days=(3*30))
                logger.info("ceiling", ceiling)
                logger.info("floor", floor)
                since = str(int(floor.timestamp()))
                until = str(int(ceiling.timestamp()))
                response = API(period=period, since=since, until=until)

            else:
                try:
                    next_page_url = response["paging"][page_key]
                except:
                    break
                response = requests.get(next_page_url).json()

            if 'data' not in response:
                err_msg = str(response)
                raise IOError(err_msg)

            else:
                data = response["data"]
                if api_type == 'insight' and len(data) > 0:
                    keep_going = fb_ig.is_insight_data_within_two_years(data)
                elif api_type == 'post':
                    keep_going = fb_ig.is_fb_post_data_within_two_years(data)
                else:
                    keep_going = False

    logger.info("-----FINISHED CRAWLING-------")
    logger.info("Total_time: {}".format(total_time))
    logger.info("Avg Handler Time: {}".format(avg_time))

    return "success"
