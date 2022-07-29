from .base_views import BaseDatasourceViewSet
from blocklight_api.serializers import shipstation_serializers
from blocklight_api.serializers.core_serializers import ChartDataSerializer

from dashboards.models import (
    Integrations_ShipStation_Fulfillments, Integrations_ShipStation_OrderItems,
    Integrations_ShipStation_Orders, Integrations_ShipStation_Shipments,
    Integrations_ShipStation_Tags, Integrations_ShipStation_Warehouses
)


class ShipstationFulfillmentsViewSet(BaseDatasourceViewSet):
    queryset = Integrations_ShipStation_Fulfillments.objects.all()
    serializer_class = shipstation_serializers.ShipStationFulfillmentsSerializer  # noqa
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'last_sync_time'


class ShipstationOrderItemsViewSet(BaseDatasourceViewSet):
    queryset = Integrations_ShipStation_OrderItems.objects.all()
    serializer_class = shipstation_serializers.ShipStationOrderItemsSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'last_sync_time'


class ShipstationOrdersViewSet(BaseDatasourceViewSet):
    queryset = Integrations_ShipStation_Orders.objects.all()
    serializer_class = shipstation_serializers.ShipStationOrdersSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'last_sync_time'


class ShipstationShipmentsViewSet(BaseDatasourceViewSet):
    queryset = Integrations_ShipStation_Shipments.objects.all()
    serializer_class = shipstation_serializers.ShipStationShipmentsSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'last_sync_time'


class ShipstationTagsViewSet(BaseDatasourceViewSet):
    queryset = Integrations_ShipStation_Tags.objects.all()
    serializer_class = shipstation_serializers.ShipStationTagsSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'last_sync_time'


class ShipstationWarehousesViewSet(BaseDatasourceViewSet):
    queryset = Integrations_ShipStation_Warehouses.objects.all()
    serializer_class = shipstation_serializers.ShipStationWarehousesSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'last_sync_time'
