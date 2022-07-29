from __future__ import print_function

from ..integrations.integration import Integration

from ..models import Integrations_ShipStation_Shipments, Integrations_ShipStation_Orders, Integrations_ShipStation_Tags, \
    Integrations_ShipStation_Warehouses, BasicAuthRecords, Integrations_ShipStation_OrderItems

from celery import shared_task
from datetime import datetime
from django.utils import timezone
import logging
import requests
import socket


logger = logging.getLogger(__name__)


# TODO: Revisit this. Check if there is a better.
if socket.gethostname().startswith('dev'):
    DJANGO_HOST = "development"
elif socket.gethostname().startswith('www'):
    DJANGO_HOST = "production"
else:
    DJANGO_HOST = "localhost"


class ShipstationIntegration(Integration):

    def get_task(self, user):
        task = initialize_shipstation_syncworker_task
        tcount = BasicAuthRecords.objects.filter(integration_name='shipstation', user_iden=user.id).count()
        return task, tcount

    def get_params(self, auth_params):
        # # // BUILD LIST OF MODELS & SHOPIFY-API CALLS TO LOOP THRU NEEDED ENDPOINTS (ORDERS, PRODUCTS, CUSTOMERS)
        shipments = {
            'model': Integrations_ShipStation_Shipments,
            'API': buildCall(query='Shipments', last_sync_time=auth_params['last_sync_time'],
                             initialize=auth_params['initialize'], model=Integrations_ShipStation_Shipments,
                             auth_params=auth_params),
        }
        orders = {
            'model': Integrations_ShipStation_Orders,
            'API': buildCall(query='Orders', last_sync_time=auth_params['last_sync_time'],
                             initialize=auth_params['initialize'], model=Integrations_ShipStation_Orders,
                             auth_params=auth_params),
        }
        tags = {
            'model': Integrations_ShipStation_Tags,
            'API': buildCall(query='ListTags', last_sync_time=auth_params['last_sync_time'],
                             initialize=auth_params['initialize'], model=Integrations_ShipStation_Tags,
                             auth_params=auth_params),
        }
        warehouses = {
            'model': Integrations_ShipStation_Warehouses,
            'API': buildCall(query='Warehouses', last_sync_time=auth_params['last_sync_time'],
                             initialize=auth_params['initialize'], model=Integrations_ShipStation_Warehouses,
                             auth_params=auth_params),
        }
        apis = [
            {'name': 'orders', 'data': orders},
            {'name': 'tags', 'data': tags},
            {'name': 'warehouses', 'data': warehouses},
            {'name': 'shipments', 'data': shipments},
        ]
        return apis

    def set_sync_state(self, user_id, integration_name, celery_id):
        return super().set_sync_state(user_id, integration_name, celery_id)

    def build_auth_params(self, integration_name, user):
        return super().build_auth_params(integration_name, user)


@shared_task(time_limit=36000, name="initialize_shipstation_syncworker_task")
def initialize_shipstation_syncworker_task(integration, user):
    try:
        print("SYNC - SHIPSTATION - {}".format(user))
        task_id = initialize_shipstation_syncworker_task.request.id
        user_iden = user.id
        integration.set_sync_state(user_iden, 'shipstation', task_id)
        auth_params = integration.build_auth_params('shipstation', user)
        if auth_params != 'done':

            apis = integration.get_params(auth_params)

            # // BEGIN LOOP THROUGH ENDPOINTS
            i = 0
            for api in apis:
                i = i + 1
                name = api['name']
                data = api['data']
                model = data['model']
                API = data['API']
                SyncShipStation(auth_params['initialize'], model,
                                API, name, auth_params['user_iden'])
    except Exception as e:
        logger.warn("Following exception occurred for Shipstation integration of user " + str(user) + ": " + str(e))
        return 'failed'

    return 'done'


def SyncShipStation(initialize, model, ShipStationAPI, name, user_iden):
    import requests

    # IF THE USER ALREADY COMPLETED INITIAL SYNC
    ct_internal = len(model.objects.all())
    data = ShipStationAPI
    now_time = timezone.now()

    # PASS THE DATA FOUND ABOVE
    def Sync(data, model, name, now_time, user_iden, initialize):

        for row in data:
            x = 0  # RESET COUNTER
            i = 0  # RESET COUNTER

            # DEAL WITH ENDPOINT SPECIFIC LOGIC - shipments
            if name == 'shipments':
                if row == 'shipments':
                    shipments = data[row]
                    ttl_count = len(shipments)
                    for shipment in shipments:
                        i = i + 1
                        initialize_shipstation_syncworker_task.update_state(state='PROGRESS',
                                                                            meta={'current': i, 'total': ttl_count})
                        for key in shipment:
                            if key == 'shipmentId':
                                shipmentId = shipment[key]

                                try:
                                    model_entry, created = model.objects.get_or_create(shipmentId=shipmentId,
                                                                                       user_iden=user_iden)
                                    if created:
                                        SaveShipStationShipments(model_entry, now_time, user_iden, shipment)
                                except:

                                    check = model.objects.get_or_create(shipmentId=shipmentId,
                                                                        user_iden=user_iden)
                                    if len(check) > 1:
                                        check.delete()

            # DEAL WITH ENDPOINT SPECIFIC LOGIC - orders
            if name == 'orders':
                if row == 'orders':
                    orders = data[row]
                    ttl_count = len(orders)
                    for order in orders:
                        i = i + 1
                        items = {'orderItemId': None}
                        initialize_shipstation_syncworker_task.update_state(state='PROGRESS',
                                                                            meta={'current': i, 'total': ttl_count})
                        for key in order:
                            if key == 'orderId':
                                orderId = order[key]
                                check = model.objects.filter(orderId=orderId, user_iden=user_iden)
                                try:
                                    model_entry, created = model.objects.get_or_create(
                                        orderId=orderId, user_iden=user_iden)
                                    if created:
                                        SaveShipStationOrders(model_entry, now_time, user_iden, order)
                                    else:
                                        i = 0
                                        break
                                except:
                                    if len(check) > 1:
                                        check.delete()
                            if key == 'items':
                                items = order[key]
                                orderId = order['orderId']
                                for item in items:
                                    orderItemId = item['orderItemId']
                                    if DJANGO_HOST == 'localhost':  print(('orderItemId=', item['orderItemId']))
                                    check = Integrations_ShipStation_OrderItems.objects.filter(orderItemId=orderItemId,
                                                                                               user_iden=user_iden,
                                                                                               orderId=orderId)
                                    try:
                                        model_entry, created = Integrations_ShipStation_OrderItems.objects.get_or_create(
                                            orderItemId=orderItemId, user_iden=user_iden, orderId=orderId)
                                        if created:
                                            SaveShipStationOrderItems(model_entry, now_time, user_iden,
                                                                      item, orderId)
                                        else:
                                            i = 0
                                            break
                                    except:
                                        if len(check) > 1:
                                            check.delete()

            # DEAL WITH ENDPOINT SPECIFIC LOGIC - tags
            if name == 'tags':
                ttl_count = len(data)
                for tag in data:

                    i = i + 1
                    initialize_shipstation_syncworker_task.update_state(state='PROGRESS',
                                                                        meta={'current': i, 'total': ttl_count})
                    tagId = tag['tagId']
                    check = Integrations_ShipStation_Tags.objects.filter(tagId=tagId, user_iden=user_iden)
                    try:
                        model_entry, created = Integrations_ShipStation_Tags.objects.get_or_create(tagId=tagId,
                                                                                                   user_iden=user_iden)
                        if created:
                            SaveShipStationTags(model_entry, now_time, user_iden, tag)
                        else:
                            i = 0
                            break
                    except:
                        if len(check) > 1:
                            check.delete()

            # DEAL WITH ENDPOINT SPECIFIC LOGIC - warehouses
            if name == 'warehouses':
                ttl_count = len(data)
                for w in data:
                    i = i + 1
                    initialize_shipstation_syncworker_task.update_state(state='PROGRESS',
                                                                        meta={'current': i, 'total': ttl_count})
                    warehouseId = w['warehouseId']
                    check = model.objects.get_or_create(warehouseId=warehouseId, user_iden=user_iden)
                    try:
                        model_entry, created = Integrations_ShipStation_Warehouses.objects.get_or_create(
                            warehouseId=warehouseId, user_iden=user_iden)
                        if created:
                            SaveShipStationWarehouses(model_entry, now_time, user_iden, w)
                        else:
                            i = 0
                            break
                    except:
                        if len(check) > 1:
                            check.delete()

            if i == 500:
                import base64
                keys_data = BasicAuthRecords.objects.get(integration_name='shipstation', user_iden=user_iden)
                api_key = keys_data.api_key
                api_secret = keys_data.api_secret
                keySecret = api_key + ':' + api_secret
                base64auth_string = str(base64.b64encode(keySecret.encode('utf-8')), 'utf-8')
                # ************ BEGIN | CALL HTTP REQUESTS ****************
                base = 'https://ssapi.shipstation.com/'
                headers = {'Authorization': 'Basic ' + base64auth_string}

                # ************ DEFINE PARAMS ****************
                sort_key = 'CreateDate'
                if name in ['orders', 'shipments']:
                    latest = datetime.isoformat(model.objects.earliest('createDate').createDate)
                    latest, trash = latest.split('T')
                    queri = name.lower() + '?createDateEnd=' + str(
                        latest) + '&sortBy=CreateDate&sortDir=DESC&pageSize=500'
                    url = base + queri
                    data = requests.get(url, headers=headers).json()
                    if DJANGO_HOST == 'localhost':  print(('latest ss = ', latest, '\n'))
                    if DJANGO_HOST == 'localhost':  print(('ss url = ', url, '\n'))
                    Sync(data, model, name, now_time, user_iden, initialize)

    # INIT FIRST LOOP
    response = Sync(data, model, name, now_time, user_iden, initialize)
    return response


# buildCall
# change the record in DB (table = integrations_user_lastsync)
def buildCall(query, last_sync_time, initialize, model, auth_params):
    base = 'https://ssapi.shipstation.com/'
    headers = {'Authorization': 'Basic ' + auth_params['base64auth_string']}

    # ************ DEFINE PARAMS ****************
    sort_key = 'CreateDate'
    lil_q = query.lower()
    _en = lil_q + '?'
    ps = '&pageSize=500'

    if initialize == True:
        if query in ['Orders', 'Shipments']:
            queri = _en + lil_q + 'sortBy=' + sort_key + '&sortDir=DESC' + ps
        elif query == 'ListTags':
            queri = 'accounts/listtags'
        else:
            query == 'Warehouses'
            queri = query.lower()
    else:
        if query in ['Orders', 'Shipments']:
            try:
                latest = datetime.isoformat(
                    model.objects.latest('createDate').createDate)
                latest, trash = latest.split('T')
                queri = _en + lil_q + 'createDateStart=' + str(
                    latest) + '&sortBy=' + sort_key + '&sortDir=ASC' + ps
            except:
                queri = _en + lil_q + 'sortBy=' + sort_key + '&sortDir=DESC' + ps
                initialize = True
        elif query == 'ListTags':
            queri = 'accounts/listtags'
        else:
            query == 'Warehouses'
            queri = query.lower()
        if DJANGO_HOST == 'localhost':
            print('error in shipstation tasks.py')

    url = base + queri
    api = requests.get(url, headers=headers).json()

    return api


# GET /lists/{list_id}/members
# Get information about a specific list member, including a currently subscribed, unsubscribed, or bounced member.
def SaveShipStationShipments(model_entry, now_time, user_iden, shipment):
    row = shipment
    model_entry.user_iden = user_iden
    model_entry.orderId = row['orderId']
    model_entry.orderKey = row['orderKey']
    model_entry.userId = row['userId']
    model_entry.customerEmail = row['customerEmail']
    model_entry.orderNumber = row['orderNumber']
    model_entry.createDate = row['createDate']
    model_entry.shipDate = row['shipDate']
    model_entry.shipmentCost = row['shipmentCost']
    model_entry.insuranceCost = row['insuranceCost']
    model_entry.trackingNumber = row['trackingNumber']
    model_entry.isReturnLabel = row['isReturnLabel']
    model_entry.batchNumber = row['batchNumber']
    model_entry.carrierCode = row['carrierCode']
    model_entry.serviceCode = row['serviceCode']
    model_entry.packageCode = row['packageCode']
    model_entry.confirmation = row['confirmation']
    model_entry.warehouseId = row['warehouseId']
    model_entry.voided = row['voided']
    model_entry.voidDate = row['voidDate']
    model_entry.marketplaceNotified = row['marketplaceNotified']
    model_entry.notifyErrorMessage = row['notifyErrorMessage']
    model_entry.serviceCode = row['serviceCode']
    model_entry.serviceCode = row['serviceCode']
    model_entry.save()


def SaveShipStationOrders(model_entry, now_time, user_iden, order):
    row = order
    model_entry.user_iden = user_iden
    model_entry.orderId = row['orderId']
    model_entry.orderNumber = row['orderNumber']
    model_entry.orderKey = row['orderKey']
    model_entry.createDate = row['createDate']
    model_entry.modifyDate = row['modifyDate']
    model_entry.paymentDate = row['shipTo']
    model_entry.paymentDate = row['items']
    model_entry.paymentDate = row['paymentDate']
    model_entry.shipByDate = row['shipByDate']
    model_entry.orderStatus = row['orderStatus']
    model_entry.customerId = row['customerId']
    model_entry.customerUsername = row['customerUsername']
    model_entry.customerNotes = row['customerNotes']
    model_entry.internalNotes = row['internalNotes']
    model_entry.requestedShippingService = row['requestedShippingService']
    model_entry.packageCode = row['packageCode']
    model_entry.tagIds = row['tagIds']
    # model_entry.userIds = row['userIds']
    model_entry.externallyFulfilled = row['externallyFulfilled']
    model_entry.externallyFulfilledBy = row['externallyFulfilledBy']
    model_entry.labelMessages = row['labelMessages']
    model_entry.insuranceOptions_provider = row['insuranceOptions']['provider']
    model_entry.insuranceOptions_insureShipment = row['insuranceOptions']['insureShipment']
    model_entry.insuranceOptions_insuredValue = row['insuranceOptions']['insuredValue']
    if 'weight' in row:
        try:
            model_entry.weight_value = row['weight']['value']
            model_entry.weight_units = row['weight']['units']
        except:
            model_entry.weight_units = None
            model_entry.weight_value = None

    if 'dimensions' in row:
        try:
            model_entry.dimensions_units = row['dimensions']['units']
            model_entry.dimensions_length = row['dimensions']['length']
            model_entry.dimensions_width = row['dimensions']['width']
            model_entry.dimensions_height = row['dimensions']['height']
        except:
            model_entry.dimesnions_units = None
            model_entry.dimesnions_length = None
            model_entry.dimesnions_width = None
            model_entry.dimesnions_height = None

    if 'advancedOptions' in row:
        model_entry.advancedOptions_warehouseId = row['advancedOptions']['warehouseId']
        try:
            model_entry.advancedOptions_nonMachineable = row['advancedOptions']['nonMachineable']
            model_entry.advancedOptions_saturdayDelivery = row['advancedOptions']['saturdayDelivery']
            model_entry.advancedOptions_containsAlchohol = row['advancedOptions']['containsAlchohol']
            model_entry.advancedOptions_mergedOrSplit = row['advancedOptions']['mergedOrSplit']
            model_entry.advancedOptions_source = row['advancedOptions']['source']
        except:
            model_entry.advancedOptions_nonMachineable = False
            model_entry.advancedOptions_saturdayDelivery = False
            model_entry.advancedOptions_containsAlchohol = False
            model_entry.advancedOptions_mergedOrSplit = False
            model_entry.advancedOptions_source = None
    model_entry.save()


def SaveShipStationOrderItems(model_entry, now_time, user_iden, item, orderId):
    n = 0
    for key in item:
        row = item
        model_entry.user_iden = user_iden
        model_entry.last_sync_time = now_time
        model_entry.orderId = orderId
        if key == 'orderNumber':
            model_entry.orderNumber = row[key]
        if key == 'orderItemId':
            model_entry.orderItemId = row[key]
        if key == 'lineItemKey':
            model_entry.lineItemKey = row[key]
        if key == 'sku':
            model_entry.sku = row[key]
        if key == 'name':
            model_entry.name = row[key]
        if key == 'imageUrl':
            model_entry.imageUrl = row[key]
        if key == 'weight':
            if row[key] != None:
                for k in row[key]:
                    if k == 'value':
                        model_entry.weight_value = row[key][k]
                    if k == 'units':
                        model_entry.weight_units = row[key][k]
        if key == 'quantity':
            model_entry.quantity = row[key]
        if key == 'unitPrice':
            model_entry.unitPrice = row[key]
        if key == 'taxAmount':
            model_entry.taxAmount = row['taxAmount']
        if key == 'shippingAmount':
            model_entry.shippingAmount = row[key]
        if key == 'warehouseLocation':
            model_entry.warehouseLocation = row[key]
        if key == 'createDate':
            model_entry.createDate = row[key]
        if key == 'modifyDate':
            model_entry.modifyDate = row[key]
        if key == 'options':
            model_entry.options = row[key]
        if key == 'productId':
            model_entry.productId = row[key]
        if key == 'fulfillmentSku':
            model_entry.fulfillmentSku = row['fulfillmentSku']
        if key == 'adjustment':
            model_entry.adjustment = row['adjustment']
        if key == 'upc':
            model_entry.upc = row['upc']
    model_entry.save()


def SaveShipStationTags(model_entry, now_time, user_iden, tag):
    row = tag
    model_entry.last_sync_time = now_time
    model_entry.user_iden = user_iden
    model_entry.tagId = row['tagId']
    model_entry.name = row['name']
    model_entry.color = row['color']
    model_entry.save()


def SaveShipStationWarehouses(model_entry, now_time, user_iden, w):
    row = w
    model_entry.integration_name = 'shipstation'
    model_entry.last_sync_time = now_time
    model_entry.user_iden = user_iden
    model_entry.warehouseId = row['warehouseId']
    model_entry.warehouseName = row['warehouseName']
    model_entry.createDate = row['createDate']
    model_entry.isDefault = row['isDefault']
    model_entry.save()
