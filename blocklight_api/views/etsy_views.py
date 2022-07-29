from .base_views import BaseDatasourceViewSet
from blocklight_api.serializers import etsy_serializers
from blocklight_api.serializers.core_serializers import ChartDataSerializer

from dashboards.models import(
    Integrations_Etsy_User,
    Integrations_Etsy_Ledger,
    Integrations_Etsy_Listing,
    Integrations_Etsy_Listing_Product,
    Integrations_Etsy_Receipt,
    Integrations_Etsy_Receipt_Payment,
    Integrations_Etsy_Receipt_Payment_Adjustment,
    Integrations_Etsy_Receipt_Payment_Adjustment_Item,
    Integrations_Etsy_Receipt_Shipment,
    Integrations_Etsy_Transaction,
    Integrations_Etsy_Transaction_Tag,
    Integrations_Etsy_Transaction_Material
)


class EtsyUserViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Etsy_User.objects.all()
    serializer_class = etsy_serializers.EtsyUserSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'join_tsz'

class EtsyLedgerViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Etsy_Ledger.objects.all()
    serializer_class = etsy_serializers.EtsyLedgerSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'create_date'

class EtsyListingViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Etsy_Listing.objects.all()
    serializer_class = etsy_serializers.EtsyListingSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'original_creation_tsz'

class EtsyListingProductViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Etsy_Listing_Product.objects.all()
    serializer_class = etsy_serializers.EtsyListingProductSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'listing_ref__user_iden'
    since_until_field = 'last_sync_time'

class EtsyReceiptViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Etsy_Receipt.objects.all()
    serializer_class = etsy_serializers.EtsyReceiptSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'creation_tsz'

class EtsyReceiptPaymentViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Etsy_Receipt_Payment.objects.all()
    serializer_class = etsy_serializers.EtsyReceiptPaymentSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'create_date'

class EtsyReceiptPaymentAdjustmentViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Etsy_Receipt_Payment_Adjustment.objects.all()
    serializer_class = etsy_serializers.EtsyReceiptPaymentAdjustmentSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'create_date'

class EtsyReceiptPaymentAdjustmentItemViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Etsy_Receipt_Payment_Adjustment_Item.objects.all()
    serializer_class = etsy_serializers.EtsyReceiptPaymentAdjustmentItemSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'create_date'

class EtsyReceiptShipmentViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Etsy_Receipt_Shipment.objects.all()
    serializer_class = etsy_serializers.EtsyReceiptShipmentSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'receipt_ref__user_iden'
    since_until_field = 'last_sync_time'

class EtsyTransactionViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Etsy_Transaction.objects.all()
    serializer_class = etsy_serializers.EtsyTransactionSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'creation_tsz'

class EtsyTransactionTagViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Etsy_Transaction_Tag.objects.all()
    serializer_class = etsy_serializers.EtsyTransactionTagSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'transaction_ref__user_iden'
    since_until_field = 'transaction_ref__creation_tsz'

class EtsyTransactionMaterialViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Etsy_Transaction_Material.objects.all()
    serializer_class = etsy_serializers.EtsyTransactionMaterialSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'transaction_ref__user_iden'
    since_until_field = 'transaction_ref__creation_tsz'
