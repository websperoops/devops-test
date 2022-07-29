from . import etsyAPI
from .etsyHandler import EtsyHandler
from dashboards.models import UserProfile
from datetime import date
from django.utils import timezone
import logging


logger = logging.getLogger(__name__)


def saveUserProfile(user_id, etsy_profile):
    user_profile = UserProfile.objects.get(user_id=user_id)
    if not user_profile.avatar:
        user_profile.avatar = etsy_profile.avatar_src_url

    if not user_profile.birthday:
        user_profile.birthday = date(int(etsy_profile.birth_year), int(etsy_profile.birth_month), int(etsy_profile.birth_day))

    user_profile.save()


def save_etsy(integration=None, user=None, task_id=None):
    logger.debug("SYNC - ETSY - {}".format(user))
    
    integration.set_sync_state(user.id, 'etsy', task_id)
    auth_params = integration.build_auth_params('etsy', user)
    request, etsy_id, apis = integration.get_params(user.id)

    # Sync User
    got_user = False
    while not got_user:
        try:
            [user_info, avatar_info] = etsyAPI.getUser(request, etsy_id)
            address_info = etsyAPI.getUserAddresses(request, etsy_id)
            shops_info = etsyAPI.getShops(request, etsy_id)
            got_user = True
        except Exception as e:
            raise e
            break

    user_profile = EtsyHandler.save_user(user_info, avatar_info, auth_params['pk'], timezone.now(), user.id)
    saveUserProfile(user.id, user_profile)
    user_addresses = EtsyHandler.save_user_addresses(address_info, auth_params['pk'], timezone.now(), user.id, user_profile)
    user_shops = EtsyHandler.save_shops(shops_info, auth_params['pk'], timezone.now(), user.id, user_profile)

    # Loop Through Endpoints
    for core_table, metadata in apis.items():
        model = metadata['model']
        API = metadata['API']
        handler = metadata['handler']

        status = SyncEtsy(auth_params['initialize'], model, API, auth_params['pk'], core_table, auth_params['user_iden'], handler, user.id, request, user_shops)
    
    return status


def SyncEtsy(initialize, model, EtsyAPI, pk, name, user_iden, handler, user_id, rq, shop_ids):
    def Sync(data, pk, user_iden, handler, shop_id, partition=None):
        print('SHOP')
        print(shop_id)
        size = len(list(data))
        ptr = 0
        EtsyHandler.logger = logger
        if partition and partition > 1 and size > partition:
            while ptr + partition <= (size):
                table_handler = handler(data[ptr:ptr+partition], pk, user_iden, shop_id)
                table_handler.save_all_objects()
                ptr += partition
        
        if ptr != size:
            table_handler = handler(data[ptr::], pk, user_iden, shop_id, rq)
            table_handler.save_all_objects()
    
    ct_internal = len(model.objects.filter(user_iden=user_iden))
    if initialize == False and ct_internal > 0:
        for shop_id in shop_ids:
            data = EtsyAPI(rq, shop_id)
            print('ETSY API ------------------------------------')
            print(EtsyAPI)
            print('Len Data:',len(data))
            print("new")
            Sync(data, pk, user_iden, handler, shop_id, None)
    else:
        print("crawl")
        lim = 10000000
        for shop_id in shop_ids:
            count = 0
            data = EtsyAPI(rq, shop_id, offset=count, limit = lim)
            while len(data) > 0:
                count+=len(data)
                print('ETSY API ------------------------------------')
                print(EtsyAPI)
                print('Len Data:',len(data))
                Sync(data, pk, user_iden, handler, shop_id, None)
                data = EtsyAPI(rq, shop_id, offset=count, limit = lim)

    return('success')
