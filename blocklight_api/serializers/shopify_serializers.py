from dashboards.models import(
    Integrations_Shopify_Order, Integrations_Shopify_Customer,
    Integrations_Shopify_Line_Item, Integrations_Shopify_Refund,
    Integrations_Shopify_Refund, Integrations_Shopify_Refund_Line_Item,
    Integrations_Shopify_Transaction, Integrations_Shopify_Abandoned_Checkouts,
    Integrations_Shopify_Abandoned_Checkout_Line_Items, Integrations_Shopify_Product,
    Integrations_Shopify_Product_Variant, Integrations_Shopify_Address,
    Integrations_Shopify_Shipping_Line, Integrations_Shopify_Shop_Discount_Code,
    Integrations_Shopify_Product_Image
)

from rest_framework import serializers


class ShopifyOrdersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Shopify_Order
        exclude = [
            'integration',
            'subtotal_price_set',
            'total_price_set',
            'total_tax_set',
            'total_discounts_set',
            'total_line_items_set',
            'url',
            'shop'
        ]


class ShopifyCustomersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Shopify_Customer
        exclude = [
            'integration',
            'url',
            'shop'
        ]


class ShopifyOrderLineItemsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Shopify_Line_Item
        exclude = [
            'price_set',
            'total_discount_set',
            'url'
        ]


class ShopifyRefundsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Shopify_Refund
        exclude = [
            'url'
        ]


class ShopifyRefundLineItemsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Shopify_Refund_Line_Item
        exclude = [
            'url',
            'subtotal_set',
            'total_tax_set'
        ]


class ShopifyTransactionsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Shopify_Transaction
        fields = [
            'id',
            'order_id',
            'transaction_id',
            'amount',
            'authorization',
            'created_at',
            'currency',
            'device_id',
            'error_code',
            'gateway',
            'kind',
            'location_id',
            'message',
            'parent_id',
            'processed_at',
            'source_name',
            'status',
            'test',
            'user_id',
            'order_ref_id',
            'order_ref',
            'refund_id',
            'refund_ref'
        ]


class ShopifyAbandonedCheckoutsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Shopify_Abandoned_Checkouts
        fields = [
            'id',
            'checkout_id',
            'user_iden',
            'created_at',
            'closed_at',
            'completed_at',
            'landing_site',
            'variant_id',
            'abandoned_checkout_url',
            'quantity',
            'subtotal_price',
            'total_price',
            'total_tax',
            'cart_token',
            'vendor',
            'fulfillment_service',
            'buyer_accepts_marketing',
            'taxable',
            'gift_card',
            'customer',
            'variant_inventory_management',
            'discount_codes',
            'product_exists',
            'fulfillable_quantity',
            'total_discounts',
            'gateway',
            'last_sync_time',
            'integration_id'
        ]


class ShopifyAbandonedCheckoutLineItemsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Shopify_Abandoned_Checkout_Line_Items
        fields = [
            'checkout',
            'fulfillment_service',
            'grams',
            'price',
            'product_id',
            'quantity',
            'requires_shipping',
            'sku',
            'title',
            'variant_id',
            'variant_title',
            'vendor'
        ]


class ShopifyProductsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Shopify_Product
        fields = [
            'id',
            'user_iden',
            'created_at',
            'product_id',
            'published_at',
            'published_scope',
            'title',
            'updated_at',
            'vendor',
            'last_sync_time',
            'integration_id',
            'product_type'
        ]


class ShopifyProductVariantsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Shopify_Product_Variant
        fields = [
            'barcode',
            'compare_at_price',
            'created_at',
            'fulfillment_service',
            'grams',
            'variant_id',
            'inventory_item_id',
            'inventory_management',
            'inventory_policy',
            'inventory_quantity',
            'option1',
            'option2',
            'option3',
            'position',
            'price',
            'product',
            'sku',
            'taxable',
            'tax_code',
            'title',
            'updated_at',
            'weight',
            'weight_unit'
        ]


class ShopifyAddressesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Shopify_Address
        fields = [
            'id',
            'address1',
            'address2',
            'city',
            'company',
            'country',
            'country_code',
            'first_name',
            'last_name',
            'latitude',
            'longitude',
            'name',
            'phone',
            'province',
            'zip'
        ]


class ShopifyShippingLinesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Shopify_Shipping_Line
        fields = [
            'order',
            'code',
            'price',
            'discounted_price',
            'source',
            'title'
        ]


class ShopifyShopDiscountCodesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Shopify_Shop_Discount_Code
        fields = [
            'discount_id',
            'code',
            'created_at',
            'updated_at',
            'usage_count'
        ]


class ShopifyProductImagesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Shopify_Product_Image
        fields = [
            'product',
            'product_image_id',
            'src',
            'width',
            'height',
            'created_at',
            'updated_at'
        ]


############## COMPLEX ENDPOINTS ########################


''' Metric-Shopify-Refunds-Marketing-Acceptance '''


class ShopifyBlInsightsRelatedOrderMarketingAcceptanceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Shopify_Order
        fields = [
            'id',
            'order_id',
            'created_at',
            'user_iden',
            'buyer_accepts_marketing'
        ]


class ShopifyBlInsightsRelatedRefundLineItemMarketingAcceptanceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Shopify_Refund_Line_Item
        fields = [
            'subtotal',
            'total_tax'
        ]


class ShopifyBlInsightsRefundMarketingAcceptanceSerializer(serializers.HyperlinkedModelSerializer):
    order = ShopifyBlInsightsRelatedOrderMarketingAcceptanceSerializer(read_only=True)
    line_items = ShopifyBlInsightsRelatedRefundLineItemMarketingAcceptanceSerializer(read_only=True, many=True)
    class Meta:
        model = Integrations_Shopify_Refund
        fields = [
            'id',
            'refund_id',
            'order',
            'created_at',
            'line_items'
        ]


''' Metric-Shopify-Customer-Last-Order-Info '''


class ShopifyBlInsightsRelatedOrderCustomerLastOrderInfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Shopify_Order
        fields = [
            'id',
            'order_id',
        ]


class ShopifyBlInsightsCustomerLastOrderInfoSerializer(serializers.HyperlinkedModelSerializer):
    def get_orders():
        if Integrations_Shopify_Order.objects.count() > 0:
            return ShopifyBlInsightsRelatedOrderCustomerLastOrderInfoSerializer(Integrations_Shopify_Order.objects.latest('created_at'), many=True)
        else:
            return None
    
    orders = get_orders()
    class Meta:
        model = Integrations_Shopify_Customer
        fields = [
            'id',
            'customer_id',
            'user_iden',
            'last_order_id',
            'created_at',
            'orders'
        ]


''' Metric-Shopify-Top-Customers '''


class ShopifyBlInsightsRelatedRefundLineItemsTopCustomersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Shopify_Refund_Line_Item
        fields = [
            'subtotal',
            'total_tax',
            'refund_id'
        ]


class ShopifyBlInsightsRelatedRefundsTopCustomersSerializer(serializers.HyperlinkedModelSerializer):
    line_items = ShopifyBlInsightsRelatedRefundLineItemsTopCustomersSerializer(read_only=True, many=True)
    class Meta:
        model = Integrations_Shopify_Refund
        fields = [
            'id',
            'refund_id',
            'order_id',
            'created_at',
            'line_items'
        ]


class ShopifyBlInsightsRelatedOrdersTopCustomersSerializer(serializers.HyperlinkedModelSerializer):
    refunds = ShopifyBlInsightsRelatedRefundsTopCustomersSerializer(read_only=True, many=True)
    class Meta:
        model = Integrations_Shopify_Order
        fields = [
            'id',
            'order_id',
            'user_iden',
            'total_discounts',
            'customer_ref_id',
            'refunds'
        ]


class ShopifyBlInsightsTopCustomersSerializer(serializers.HyperlinkedModelSerializer):
    orders = ShopifyBlInsightsRelatedOrdersTopCustomersSerializer(read_only=True, many=True)
    class Meta:
        model = Integrations_Shopify_Customer
        fields = [
            'id',
            'customer_id',
            'first_name',
            'last_name',
            'email',
            'orders_count',
            'total_spent',
            'orders'
        ]


''' Metric-Shopify-Top-Products '''


class ShopifyBlInsightsRelatedOrderTopProductsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Shopify_Order
        fields = [
            'id',
            'user_iden',
            'created_at'
        ]


class ShopifyBlInsightsRelatedLineItemsTopProductsSerializer(serializers.HyperlinkedModelSerializer):
    order=ShopifyBlInsightsRelatedOrderTopProductsSerializer(read_only=True)
    class Meta:
        model = Integrations_Shopify_Line_Item
        fields = [
            'order_id',
            'product_id',
            'title',
            'price',
            'quantity',
            'order'

        ]


class ShopifyBlInsightsTopProductsSerializer(serializers.HyperlinkedModelSerializer):
    line_items = ShopifyBlInsightsRelatedLineItemsTopProductsSerializer(read_only=True,many=True)
    class Meta:
        model = Integrations_Shopify_Product
        fields = [
            'id',
            'product_id',
            'line_items'
        ]


''' Metric-Shopify-Top-Customers-Never-Used-A-Discount '''


class ShopifyBlInsightsRelatedOrdersTopCustomersNeverUsedADiscountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Shopify_Order
        fields = [
            'user_iden',
            'created_at',
            'customer_ref_id',
            'total_discounts'
        ]


class ShopifyBlInsightsTopCustomersNeverUsedADiscountSerializer(serializers.HyperlinkedModelSerializer):
    orders = ShopifyBlInsightsRelatedOrdersTopCustomersNeverUsedADiscountSerializer(many=True)
    class Meta:
        model = Integrations_Shopify_Customer
        fields = [
            'id',
            'customer_id',
            'user_iden',
            'email',
            'orders_count',
            'first_name',
            'last_name',
            'total_spent',
            'orders'
        ]


''' Metric-Shopify-Refunds '''


class ShopifyBlInsightsRelatedOrdersRefundsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Shopify_Order
        fields = [
            'id',
            'order_id',
            'user_iden'
        ]


class ShopifyBlInsightsRelatedLineItemsRefundsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model  = Integrations_Shopify_Refund_Line_Item
        fields = [
            'subtotal',
            'total_tax',
            'refund_id',
        ]


class ShopifyBlInsightsRefundSerializer(serializers.HyperlinkedModelSerializer):

    line_items = ShopifyBlInsightsRelatedLineItemsRefundsSerializer(read_only=True,many=True)
    order = ShopifyBlInsightsRelatedOrdersRefundsSerializer(read_only=True)
    class Meta:
        model = Integrations_Shopify_Refund
        fields = [
            'id',
            'refund_id',
            'created_at',
            'order_id',
            'line_items',
            'order'
        ]
