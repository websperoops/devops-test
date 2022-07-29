from dashboards.models import (
    Integrations_ShipStation_Fulfillments, Integrations_ShipStation_OrderItems,
    Integrations_ShipStation_Orders, Integrations_ShipStation_Shipments,
    Integrations_ShipStation_Tags, Integrations_ShipStation_Warehouses
)

from rest_framework import serializers


class ShipStationFulfillmentsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_ShipStation_Fulfillments
        fields = [
            'user_iden',
            'orderId',
            'orderNumber',
            'customerEmail',
            'trackingNumber',
            'shipDate',
            'voidDate',
            'deliveryDate',
            'carrierCode',
            'fulfillmentProviderCode',
            'fulfillmentServiceCode'
        ]


class ShipStationOrderItemsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_ShipStation_OrderItems
        fields = [
            'user_iden',
            'orderId',
            'orderNumber',
            'orderItemId',
            'lineItemKey',
            'sku',
            'name',
            'imageUrl',
            'weight_value',
            'weight_units',
            'quantity',
            'unitPrice',
            'taxAmount',
            'shippingAmount',
            'warehouseLocation',
            'options',
            'productId',
            'fulfillmentSku',
            'adjustment',
            'upc',
            'createDate',
            'modifyDate'
        ]


class ShipStationOrdersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_ShipStation_Orders
        fields = [
            'user_iden',
            'orderId',
            'orderNumber',
            'orderKey',
            'createDate',
            'modifyDate',
            'paymentDate',
            'shipByDate',
            'orderStatus',
            'customerId',
            'customerUsername',
            'customerNotes',
            'internalNotes',
            'requestedShippingService',
            'packageCode',
            'tagIds',
            'userIds',
            'externallyFulfilled',
            'externallyFulfilledBy',
            'labelMessages',
            'shipTo',
            'shipTo_name',
            'shipTo_company',
            'shipTo_street1',
            'shipTo_street2',
            'shipTo_street3',
            'shipTo_city',
            'shipTo_state',
            'shipTo_postalCode',
            'shipTo_country',
            'shipTo_phone',
            'shipTo_residential',
            'items',
            'insuranceOptions_provider',
            'insuranceOptions_insureShipment',
            'insuranceOptions_insuredValue',
            'dimensions_units',
            'dimensions_length',
            'dimensions_width',
            'dimensions_height',
            'advancedOptions_warehouseId',
            'advancedOptions_nonMachineable',
            'advancedOptions_saturdayDelivery',
            'advancedOptions_containsAlchohol',
            'advancedOptions_mergedOrSplit',
            'advancedOptions_source'
        ]


class ShipStationShipmentsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_ShipStation_Shipments
        fields = [
            'user_iden',
            'shipmentId',
            'orderId',
            'orderKey',
            'userId',
            'customerEmail',
            'orderNumber',
            'createDate',
            'shipDate',
            'shipmentCost',
            'insuranceCost',
            'trackingNumber',
            'isReturnLabel',
            'batchNumber',
            'carrierCode',
            'serviceCode',
            'packageCode',
            'confirmation',
            'warehouseId',
            'voided',
            'voidDate',
            'marketplaceNotified',
            'notifyErrorMessage'
        ]


class ShipStationTagsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_ShipStation_Tags
        fields = [
            'user_iden',
            'tagId',
            'name',
            'color',
        ]


class ShipStationWarehousesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_ShipStation_Warehouses
        fields = [
            'user_iden',
            'warehouseId',
            'warehouseName',
            'originAddress',
            'returnAddress',
            'createDate',
            'isDefault'
        ]
