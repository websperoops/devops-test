from .base_views import BaseDatasourceViewSet

from blocklight_api.serializers import shopify_serializers
from blocklight_api.serializers.core_serializers import ChartDataSerializer

from dashboards.models import(
    Integrations_Shopify_Order, Integrations_Shopify_Customer,
    Integrations_Shopify_Line_Item, Integrations_Shopify_Refund,
    Integrations_Shopify_Refund_Line_Item,
    Integrations_Shopify_Transaction, Integrations_Shopify_Abandoned_Checkouts,
    Integrations_Shopify_Abandoned_Checkout_Line_Items, Integrations_Shopify_Product,
    Integrations_Shopify_Product_Variant, Integrations_Shopify_Address,
    Integrations_Shopify_Shipping_Line, Integrations_Shopify_Shop_Discount_Code,
    Integrations_Shopify_Product_Image
)

from decimal import Decimal
from django.db.models import Q, Sum


class ShopifyOrdersViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Shopify_Order.objects.all()
    serializer_class = shopify_serializers.ShopifyOrdersSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'created_at'
    social_account_field = 'integration'


class ShopifyCustomersViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Shopify_Customer.objects.all()
    serializer_class = shopify_serializers.ShopifyCustomersSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'created_at'
    social_account_field = 'integration'


class ShopifyOrderLineItemsViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Shopify_Line_Item.objects.all()
    serializer_class = shopify_serializers.ShopifyOrderLineItemsSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'order__user_iden'
    since_until_field = 'created_at'
    social_account_field = 'order__integration'


class ShopifyRefundsViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Shopify_Refund.objects.all()
    serializer_class = shopify_serializers.ShopifyRefundsSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'order__user_iden'
    since_until_field = 'created_at'
    social_account_field = 'integration'


class ShopifyRefundLineItemsViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Shopify_Refund_Line_Item.objects.all()
    serializer_class = shopify_serializers.ShopifyRefundLineItemsSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'refund__order__user_iden'
    since_until_field = 'created_at'
    social_account_field = 'refund__integration'


class ShopifyTransactionsViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Shopify_Transaction.objects.all()
    serializer_class = shopify_serializers.ShopifyTransactionsSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'order_ref__user_iden'
    since_until_field = 'created_at'
    social_account_field = 'order_ref__integration'


class ShopifyAbandonedCheckoutsViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Shopify_Abandoned_Checkouts.objects.all()
    serializer_class = shopify_serializers.ShopifyAbandonedCheckoutsSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'created_at'
    social_account_field = 'integration'


class ShopifyAbandonedCheckoutLineItemsViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Shopify_Abandoned_Checkout_Line_Items.objects.all()
    serializer_class = shopify_serializers.ShopifyAbandonedCheckoutLineItemsSerializer  # noqa
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'checkout__user_iden'
    since_until_field = 'created_at'
    social_account_field = 'checkout__integration'


class ShopifyProductsViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Shopify_Product.objects.all()
    serializer_class = shopify_serializers.ShopifyProductsSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'created_at'
    social_account_field = 'integration'


class ShopifyProductVariantsViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Shopify_Product_Variant.objects.all()
    serializer_class = shopify_serializers.ShopifyProductVariantsSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'product__user_iden'
    since_until_field = 'created_at'
    social_account_field = 'product__integration'


class ShopifyOrderAddressesViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Shopify_Address.objects.all()
    serializer_class = shopify_serializers.ShopifyAddressesSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'order_billing_address__user_iden'
    since_until_field = 'created_at'


class ShopifyCustomerAddressesViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Shopify_Address.objects.all()
    serializer_class = shopify_serializers.ShopifyAddressesSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'Integrations_Shopify_Customer__set__user_iden'
    since_until_field = 'created_at'


class ShopifyShippingLinesViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Shopify_Shipping_Line.objects.all()
    serializer_class = shopify_serializers.ShopifyShippingLinesSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'order__user_iden'
    since_until_field = 'created_at'
    social_account_field = 'order__integration'


class ShopifyShopDiscountCodesViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Shopify_Shop_Discount_Code.objects.all()
    serializer_class = shopify_serializers.ShopifyShopDiscountCodesSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'price_rule__user_iden'
    since_until_field = 'created_at'
    social_account_field = 'price_rule__integration'


class ShopifyProductImagesViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Shopify_Product_Image.objects.all()
    serializer_class = shopify_serializers.ShopifyProductImagesSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'product__user_iden'
    since_until_field = 'created_at'
    social_account_field = 'product__integration'


class ShopifyBlInsightsRefundMarketingAcceptanceViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Shopify_Refund.objects.all()
    serializer_class = shopify_serializers.ShopifyBlInsightsRefundMarketingAcceptanceSerializer  # noqa
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'order__user_iden'
    since_until_field = 'created_at'
    social_account_field = 'integration'


class ShopifyBlInsightsCustomerLastOrderInfoViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Shopify_Customer.objects.filter(
        ~Q(last_order_id=None)
    )
    serializer_class = shopify_serializers.ShopifyBlInsightsCustomerLastOrderInfoSerializer  # noqa
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'created_at'
    social_account_field = 'integration'


class ShopifyBlInsightsTopCustomersViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Shopify_Customer.objects.all()
    serializer_class = shopify_serializers.ShopifyBlInsightsTopCustomersSerializer  # noqa
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'created_at'
    social_account_field = 'integration'


class ShopifyBlInsightsTopProductsViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Shopify_Product.objects.all()
    serializer_class = shopify_serializers.ShopifyBlInsightsTopProductsSerializer  # noqa
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'created_at'
    social_account_field = 'integration'


class ShopifyBlInsightsTopCustomersNeverUsedADiscountViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Shopify_Customer.objects.annotate(discount_sum=Sum(
        'orders__total_discounts')).exclude(~Q(discount_sum=Decimal("0.00")))
    serializer_class = shopify_serializers.ShopifyBlInsightsTopCustomersNeverUsedADiscountSerializer  # noqa
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'created_at'
    social_account_field = 'integration'


class ShopifyBlInsightsRefundsViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Shopify_Refund.objects.all()
    serializer_class = shopify_serializers.ShopifyBlInsightsRefundSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'order__user_iden'
    since_until_field = 'created_at'
    social_account_field = 'integration'
