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

from rest_framework import serializers


class EtsyUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Etsy_User
        fields = [
            'user_iden',
            'avatar_src_url',
            'bio',
            'gender',
            'birth_month',
            'birth_day',
            'birth_year',
            'join_tsz',
            'country_id',
            'region',
            'city',
            'location',
            'lat',
            'lon',
            'transaction_buy_count',
            'transaction_sold_count',
            'is_seller',
            'image_url_75x75',
            'first_name',
            'last_name',
            'integration_id'
        ]

class EtsyLedgerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Etsy_Ledger
        fields = [
            'shop_id',
            'last_sync_time',
            'user_iden',
            'ledger_id',
            'currency',
            'create_date',
            'update_date'
        ]

class EtsyListingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Etsy_Listing
        fields = [
            'shop_id',
            'last_sync_time',
            'user_iden',
            'listing_id',
            'state',
            'user_id',
            'category_id',   
            'title',
            'description',
            'creation_tsz',
            'ending_tsz',
            'original_creation_tsz',
            'last_modified_tsz',
            'price',
            'currency_code',
            'quantity',
            'taxonomy_path',
            'taxonomy_id',
            'suggested_taxonomy_id',
            'shop_section_id',
            'featured_rank',
            'state_tsz',
            'views',
            'num_favorers',
            'shipping_template_id',
            'processing_min',
            'processing_max',
            'who_made', 
            'is_supply',
            'when_made',
            'item_weight',
            'item_weight_unit',
            'item_length', 
            'item_width',
            'item_height',
            'item_dimensions_unit',
            'is_private',
            'recipient',
            'occasion',
            'style', 
            'non_taxable',
            'is_customizable',
            'is_digital',
            'file_data',
            'can_write_inventory',
            'has_variations',
            'should_auto_renew',
            'language'
        ]

class EtsyListingProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Etsy_Listing_Product
        fields = [
            'product_id',
            'listing_id',
            'is_deleted',
            'sku'
        ]

class EtsyReceiptSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Etsy_Receipt
        fields = [
            'shop_id',
            'last_sync_time',
            'user_iden',
            'receipt_id',
            'receipt_type',
            'order_id',
            'seller_user_id',
            'buyer_user_id',
            'creation_tsz',
            'can_refund',
            'last_modified_tsz',
            'name',
            'first_line',
            'second_line',
            'city',
            'state',
            'zip',
            'formatted_address',
            'country_id',
            'payment_method',
            'payment_email',
            'message_from_seller',
            'message_from_buyer',
            'was_paid',
            'total_tax_cost',
            'total_vat_cost',
            'total_price',
            'total_shipping_cost',
            'currency_code',
            'message_from_payment',
            'was_shipped',
            'buyer_email',
            'seller_email',
            'is_gift',
            'needs_gift_wrap',
            'gift_message',
            'gift_wrap_price',
            'discount_amt',
            'subtotal',
            'grandtotal',
            'adjusted_grandtotal',
            'buyer_adjusted_grandtotal'
        ]

class EtsyReceiptPaymentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Etsy_Receipt_Payment
        fields = [
            'receipt_id',
            'user_iden',
            'payment_id',
            'buyer_user_id',
            'shop_id',
            'amount_gross',
            'amount_fees',
            'amount_net',
            'posted_gross',
            'posted_fees',
            'posted_net',
            'adjusted_gross',
            'adjusted_fees',
            'adjusted_net',
            'currency',
            'shop_currency',
            'buyer_currency',
            'shipping_user_id',
            'shipping_address_id',
            'billing_address_id',
            'status',
            'shipped_date',
            'create_date',
            'update_date'
        ]

class EtsyReceiptPaymentAdjustmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Etsy_Receipt_Payment_Adjustment
        fields = [
            'payment_id',
            'user_iden',
            'payment_adjustment_id',
            'status',
            'is_success',
            'user_id',
            'reason_code',
            'total_adjustment_amount',
            'shop_total_adjustment_amount',
            'buyer_total_adjustment_amount',
            'total_fee_adjustment_amount',
            'create_date',
            'update_date'
        ]

class EtsyReceiptPaymentAdjustmentItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Etsy_Receipt_Payment_Adjustment_Item
        fields = [
            'payment_adjustment_id',
            'user_iden',
            'payment_adjustment_item_id',
            'adjustment_type',
            'amount',
            'transaction_id',
            'create_date'
        ]

class EtsyReceiptShipmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Etsy_Receipt_Shipment
        fields = [
            'carrier_name',
            'receipt_shipping_id',
            'tracking_code',
            'tracking_url',
            'buyer_note',
            'notification_date',
            'receipt_id'
        ]

class EtsyTransactionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Etsy_Transaction
        fields = [
            'shop_id',
            'last_sync_time',
            'user_iden',
            'transaction_id',
            'title',
            'description',
            'seller_user_id',
            'buyer_user_id',
            'creation_tsz',
            'paid_tsz',
            'shipped_tsz',
            'price',
            'currency_code',
            'quantity',
            'image_listing_id',
            'receipt_id',
            'shipping_cost',
            'is_digital',
            'file_data',
            'listing_id',
            'is_quick_sale',
            'seller_feedback_id',
            'buyer_feedback_id',
            'transaction_type',
            'url'
        ]

class EtsyTransactionTagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Etsy_Transaction_Tag
        fields = [
            'tag',
            'transaction_ref_id'
        ]

class EtsyTransactionMaterialSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Etsy_Transaction_Material
        fields = [
            'material',
            'transaction_ref_id'
        ]
