from .shopifyHandler import ShopifyHandler
from .utils import shopify_api_request

from celery import shared_task, group

from dashboards.integrations.utils.dashboard_sync_complete import dashboard_sync_complete
from dashboards.integrations.utils.handler import Handler
from dashboards.integrations.utils.log_util import create_integration_logger
from dashboards.models import Integrations_Shopify_Order, Integrations_Shopify_Shop
from datetime import datetime
from django.utils import timezone
import shopify
import time


logger = create_integration_logger(__name__, "shopify")
Handler.logger = logger

TOTAL_TIME = 0
THRESHOLD = 850


def save_shopify(integration=None, user=None, task_id=None):

    try:
        RESULTS = []
        logger.debug("SYNC - SHOPIFY - {}".format(user))
        user_iden = user.id
        integration.set_sync_state(user_iden, 'shopify', task_id)
        account_auth_param_list = integration.build_auth_params(
            'shopify', user)

        for auth_params in account_auth_param_list:
            result = Sync_Shopify_Shop_Data.si(
                auth_params, integration, user_iden)
            RESULTS.append(result)

        group(RESULTS).delay()

    except Exception as e:
        logger.warn(
            "Following exception occurred for Shopify integration of user " + str(user) + ": " + str(e))
        logger.exception("The exception: ", exc_info=True)
        raise e

    return "success"


@shared_task(name="Sync_Shopify_Store_Data")
def Sync_Shopify_Shop_Data(auth_params, integration, user_iden):

    apis = integration.get_params(auth_params)
    # api request to get the shop within the current API context (see ShopifyIntegration)
    # api request to get the shop within the current API context (see ShopifyIntegration)
    shop_info = shopify_api_request(shopify.Shop.current, logger, user_iden)
    shop = ShopifyHandler.save_shop(
        shop_info, auth_params['account_id'], timezone.now(), user_iden)
    shop_pk_id = shop.id
    for core_table, metadata in apis.items():
        model = metadata['model']
        API = metadata['API']

        handler = metadata['handler']
        statuses = metadata['status']

        status = SyncShopify(auth_params['initialize'], model, API, auth_params['account_id'], core_table,
                             auth_params['user_iden'], handler, shop_info.id, statuses)

        if status == "to be continued":
            return status

        if 'one_off' in metadata:
            one_off_task = Sync_Shopify_One_Off_Data.si(
                core_table, model, shop_pk_id, metadata['one_off'], user_iden, integration, auth_params)
            one_off_task.delay()
            return "finished"

    return status


@shared_task(name="Sync_Shopify_One_Off_Data")
def Sync_Shopify_One_Off_Data(parent_table_name, parent_table, shop_pk_id, one_off_apis, user_iden, integration, auth_params):
    integration.get_params(auth_params)
    key_field = parent_table_name + '_id'
    all_parents = parent_table.objects.filter(
        shop_id=shop_pk_id, user_iden=user_iden).order_by('-updated_at')
    lists = {}
    for parent in all_parents:
        api_param = getattr(parent, key_field, None)
        if api_param:
            kwargs = {key_field: api_param}
            for core_table, metadata in one_off_apis.items():

                if core_table not in lists:
                    lists[core_table] = []

                API = metadata['API']
                results = shopify_api_request(
                    API.find, logger, user_iden, **kwargs)
                for obj in results:
                    if core_table == 'refund' or core_table == 'transaction':
                        obj.order_id = api_param
                    lists[core_table].append(obj)

    shop_ref = Integrations_Shopify_Shop.objects.get(id=shop_pk_id)
    integration_id = shop_ref.integration_id
    shop_id = shop_ref.shop_id

    for core_table, metadata in one_off_apis.items():
        data = lists[core_table]
        handler = metadata['handler']
        table_handler = handler(data, integration_id, user_iden, shop_id)
        table_handler.save_all_objects()

    dashboard_sync_complete('shopify', user_iden)
    logger.info("task triggered")
    return 'finished'


def iter_data(data, partition=None):
    size_of_data = len(data)
    if partition and size_of_data > partition:
        print("iterating though data")
        for idx in range(0, size_of_data, partition):
            start_point = idx
            end_point = idx + partition

            if size_of_data > end_point:
                chunk = data[start_point:end_point]
            else:
                chunk = data[start_point::]

            yield chunk

    else:
        print("all data")
        yield data


def sync_data(data, pk, user_iden, handler, shop_id, resource_time, resource_batches):
    global TOTAL_TIME
    global THRESHOLD

    average_time = resource_time / resource_batches if resource_batches > 0 else 0
    if TOTAL_TIME + average_time > THRESHOLD:
        return None

    start_time = time.time()
    table_handler = handler(data, pk, user_iden, shop_id)
    table_handler.save_all_objects()
    elapsed = time.time() - start_time
    TOTAL_TIME += elapsed

    average_time = (resource_time + elapsed) / (resource_batches + 1)
    logger.info(f"TOTAL TIME: {TOTAL_TIME}")
    logger.info(f"TOTAL RESOURCE TIME: {resource_time}")
    logger.info(f"AVG RESOURCE TIME: {average_time}")
    logger.info(f"MOST RECENT BATCH TIME: {elapsed}")
    logger.info(f"RESOURCE BATCHES SYNCED: {resource_batches + 1}")

    return elapsed


def SyncShopify(initialize, model, ShopifyAPI, pk, name, user_iden, handler, shop_id, statuses):

    def log_status(total, avg, elapsed):
        logger.info(f"TOTAL TIME: {total}")
        logger.info(f"AVG TIME: {avg}")
        logger.info(f"ELAPSED: {elapsed}")
    # Function to use handler for batch transactions
    resource_time = 0
    resource_batches = 0

    """

    Args:
        initialize: boolean value indicating if user has completed the initial sync
        model: model which is being synced
        ShopifyAPI: shopify resource used to call Shopify API
        pk:
        name:
        user_iden:

    Returns: If sync was successful returns string "done"
    """

    ct_internal = len(model.objects.filter(integration_id=pk))
    oldest_record = None
    if initialize == False and ct_internal > 0:

        last_creation = datetime.isoformat(
            model.objects.latest('created_at').created_at)
        last_updated = datetime.isoformat(
            model.objects.latest('updated_at').updated_at)

        for status_field in statuses:
            if status_field:
                data_created = shopify_api_request(
                    ShopifyAPI.find, logger, user_iden, created_at_min=last_creation, limit=250)
                data_updated = shopify_api_request(
                    ShopifyAPI.find, logger, user_iden, updated_at_min=last_updated, limit=250)
            else:
                data_created = shopify_api_request(
                    ShopifyAPI.find, logger, user_iden, created_at_min=last_creation, limit=250, status=status_field)
                data_updated = shopify_api_request(
                    ShopifyAPI.find, logger, user_iden, updated_at_min=last_updated, limit=250, status=status_field)

            data = data_created + data_updated
            logger.info("-----NEW------")
            result = sync_data(list(data), pk, user_iden, handler,
                               shop_id, resource_time, resource_batches)
            if not result:
                return "to be continued"
            else:
                resource_time += result
                resource_batches += 1
        try:
            oldest_record = datetime.isoformat(model.objects.filter(
                user_iden=user_iden).exclude(created_at=None).order_by('created_at')[0].created_at)
        except IndexError as e:
            oldest_record = None

    logger.info("-----CRAWLING------")
    INIT_RECORD_CAP = 25000
    SLEEPTIME = 0
    REQ_LIMIT = 250
    partition = REQ_LIMIT
    records_synced = 0
    ShopifyAPI.find()
    for status_field in statuses:
        if status_field:
            if oldest_record:
                data = shopify_api_request(
                    ShopifyAPI.find, logger, user_iden, limit=REQ_LIMIT, status=status_field, created_at_max=oldest_record)
            else:
                data = shopify_api_request(
                    ShopifyAPI.find, logger, user_iden, limit=REQ_LIMIT, status=status_field)
        else:
            if oldest_record:
                data = shopify_api_request(
                    ShopifyAPI.find, logger, user_iden, limit=REQ_LIMIT, created_at_max=oldest_record)
            else:
                data = shopify_api_request(
                    ShopifyAPI.find, logger, user_iden, limit=REQ_LIMIT)

        for chunk in iter_data(list(data), partition=partition):
            result = sync_data(list(chunk), pk, user_iden,
                               handler, shop_id, resource_time, resource_batches)
            if not result:
                return "to be continued"
            else:
                resource_time += result
                resource_batches += 1

        while records_synced <= INIT_RECORD_CAP:

            try:
                data = shopify_api_request(
                    data.next_page, logger, user_iden, no_cache=True)
                for chunk in iter_data(list(data), partition=partition):
                    result = sync_data(
                        list(chunk), pk, user_iden, handler, shop_id, resource_time, resource_batches)
                    print(result)
                    if not result:
                        return "to be continued"
                    else:
                        resource_time += result
                        resource_batches += 1

                records_synced += len(data)
                SLEEPTIME = 0

            except IndexError as e:
                logger.warning("IndexError")
                logger.warning(e)
                break

            except AttributeError as e:
                logger.warning("AttributeError")
                logger.warning(e)
                break

    return 'success'
