# NOTE: When creating a new shopify serializer,
# DUE to multiple stores you MUST include the integration_id
# field in the fields list, this is imperative to the timeline pipeline job

from dashboards.models import (
    Integrations_Shopify_Customer,
    Integrations_Shopify_Line_Item,
    Integrations_Shopify_Order,
    Integrations_MailChimp_Campaigns,
    Integrations_MailChimp_CampaignReports,
    Integrations_Shopify_Abandoned_Checkouts,
    Integrations_Shopify_Abandoned_Checkout_Line_Items,
    Integrations_Shopify_Product,
    Integrations_Shopify_Product_Variant,
    Integrations_Shopify_Product_Image,
    Integrations_Shopify_Shipping_Line,
    Integrations_Quickbooks_Account_Info,
    Integrations_Quickbooks_Bills,
    Integrations_Quickbooks_Bill_Line_Items,
    Integrations_Etsy_Receipt,
    Integrations_Twitter_Mentions,
    TimeLine_Entry,
    Integrations_Facebook_Page_Posts,
    Integrations_Instagram_Media_Objects,
    Integrations_Google_Website_Total,
    Integrations_Shopify_Refund_Line_Item,
)

from rest_framework import serializers


class TimelineEntrySerializer(serializers.HyperlinkedModelSerializer):
    data = serializers.JSONField(read_only=True)

    class Meta:
        model = TimeLine_Entry
        fields = [
            'id',
            'integration',
            'insight',
            'data',
            'ts',
            'user_id'
        ]


class TimelineInsightsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = TimeLine_Entry
        fields = [
            'insight'
        ]

class TimelineInsightDataSerializer(serializers.Serializer):
    data = serializers.DictField(
        child = serializers.ListField(
            child = serializers.CharField(max_length=50)
        )
    )

class TimelineFeedShopifyCustomerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Shopify_Customer
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone'
        ]


class TimelineFeedShopifyLineItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Shopify_Line_Item
        fields = [
            'name',
            'title',
            'quantity',
            'price'
        ]


class TimelineFeedShopifyShippingLinesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Shopify_Shipping_Line
        fields = [
            'discounted_price'
        ]


class TimelineFeedShopifyOrderSerializer(serializers.HyperlinkedModelSerializer):
    customer_ref = TimelineFeedShopifyCustomerSerializer(read_only=True)
    line_items = TimelineFeedShopifyLineItemSerializer(
        read_only=True, many=True)
    lines = TimelineFeedShopifyShippingLinesSerializer(
        read_only=True, many=True)
    line_items_count = serializers.SerializerMethodField()
    store_name = serializers.SerializerMethodField()
    domain = serializers.SerializerMethodField()

    class Meta:
        model = Integrations_Shopify_Order

        fields = [
            'user_iden',
            'integration_id',
            'order_number',
            'order_id',
            'store_name',
            'domain',
            'total_line_items_price',
            'total_discounts',
            'subtotal_price',
            'total_tax',
            'email',
            'total_price',
            'created_at',
            'customer_ref',
            'line_items_count',
            'line_items',
            'lines'
        ]

    def get_store_name(self, obj):
        return obj.integration.extra_data.get('shop', {}).get('name', None)

    def get_domain(self, obj):
        return obj.integration.extra_data.get('shop', {}).get('myshopify_domain', None)

    def get_line_items_count(self, obj):
        return sum(x.quantity for x in list(obj.line_items.all()))


class TimelineFeedShopifyProductImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Shopify_Product_Image
        fields = [
            'product_image_id',
            'position',
            'src'
        ]


class TimelineFeedShopifyProductSerializer(serializers.HyperlinkedModelSerializer):
    images = TimelineFeedShopifyProductImageSerializer(
        many=True, read_only=True)

    class Meta:
        model = Integrations_Shopify_Product
        fields = [
            "product_id",
            "user_iden",
            'images'
        ]


class TimelineFeedShopifyProductVariantSerializer(serializers.HyperlinkedModelSerializer):
    image = TimelineFeedShopifyProductImageSerializer(read_only=True)

    class Meta:
        model = Integrations_Shopify_Product_Variant
        fields = [
            'variant_id',
            'title',
            'image'
        ]


class TimelineFeedShopifyAbandonedCheckoutLineItemSerializer(serializers.HyperlinkedModelSerializer):

    product_ref = TimelineFeedShopifyProductSerializer(read_only=True)
    variant_ref = TimelineFeedShopifyProductVariantSerializer(read_only=True)

    class Meta:
        model = Integrations_Shopify_Abandoned_Checkout_Line_Items
        fields = [
            'title',
            'quantity',
            'price',
            'product_ref',
            'variant_ref'
        ]


class TimelineFeedShopifyAbandonedCheckoutSerializer(serializers.HyperlinkedModelSerializer):
    customer_ref = TimelineFeedShopifyCustomerSerializer(read_only=True)
    line_items = TimelineFeedShopifyAbandonedCheckoutLineItemSerializer(
        read_only=True, many=True)
    line_items_count = serializers.SerializerMethodField()

    class Meta:
        model = Integrations_Shopify_Abandoned_Checkouts
        fields = [
            'user_iden',
            'integration_id',
            'subtotal_price',
            'total_discounts',
            'total_tax',
            'shipping_price',
            'total_line_items_price',
            'total_price',
            'created_at',
            'abandoned_checkout_url',
            'customer_ref',
            'line_items_count',
            'line_items',
            'checkout_id',
            'id'
        ]

    def get_line_items_count(self, obj):
        return sum(x.quantity for x in list(obj.line_items.all()))


class TimelineFeedMailChimpCampaignSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_MailChimp_Campaigns
        fields = [
            'title',
            'preview_text',
            'subject_line',
            'archive_url',
            'send_time'
        ]


class TimelineFeedMailChimpCampaignReportSerializer(serializers.HyperlinkedModelSerializer):
    campaign_ref = TimelineFeedMailChimpCampaignSerializer(
        read_only=True, many=False)

    class Meta:
        model = Integrations_MailChimp_CampaignReports
        fields = [
            'user_iden',
            'campaign_id',
            'open_rate',
            'unique_opens',
            'click_rate',
            'clicks',
            'total_spent',
            'total_revenue',
            'campaign_ref'
        ]


class TimelineFeedQuickbooksAccountInfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Quickbooks_Account_Info
        fields = [
            'user_iden',
            'account_id',
            'create_time',
            'last_update_time',
            'current_balance',
            'name'
        ]


class TimelineFeedQuickbooksBillLineItemsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Quickbooks_Bill_Line_Items
        fields = [
            'user_iden',
            'item_id',
            'item_name',
            'description',
            'amount',
            'unit_price',
            'quantity'
        ]


class TimelineFeedQuickbooksBillSerializer(serializers.HyperlinkedModelSerializer):
    line_items = TimelineFeedQuickbooksBillLineItemsSerializer(
        read_only=True, many=True)

    class Meta:
        model = Integrations_Quickbooks_Bills
        fields = [
            'bill_id',
            'user_iden',
            'due_date',
            'balance',
            'create_time',
            'last_update_time',
            'account_name',
            'vendor_name',
            'line_items'

        ]

    def get_line_items_count(self, obj):
        return sum(x.quantity for x in list(obj.line_items.all()))


class TimelineFeedEtsyOrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Etsy_Receipt
        fields = [
            'name',
            'buyer_adjusted_grandtotal',
            'creation_tsz',
            'receipt_id',
            'user_iden'
        ]


class TimelineFeedTwitterMentionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Twitter_Mentions
        fields = [
            'user_iden',
            'mention_id',
            'text',
            'timestamp'
        ]


def aggregate_values_by_title(queryset, key, value):
    totals = {}
    for obj in queryset:
        title, val = obj[key], obj[value]
        if title not in totals:
            totals[title] = val
        else:
            totals[title] += val
    return totals


class TimelineFeedFacebookPagePostsSummarySerializer(serializers.HyperlinkedModelSerializer):
    total_impressions = serializers.SerializerMethodField()
    total_reactions = serializers.SerializerMethodField()
    total_engagement = serializers.SerializerMethodField()
    impressions = serializers.SerializerMethodField()
    reactions = serializers.SerializerMethodField()
    engagement = serializers.SerializerMethodField()

    class Meta:
        model = Integrations_Facebook_Page_Posts
        fields = [
            'post_id',
            'user_iden',
            'permalink',
            'full_picture',
            'message',
            'total_impressions',
            'total_reactions',
            'total_engagement',
            'impressions',
            'reactions',
            'engagement',
            'created_time'
        ]

    def get_total_impressions(self, obj):
        values = obj.integrations_facebook_page_post_impressions_set.values_list(
            'value', flat=True)
        return sum(map(int, values))

    def get_total_reactions(self, obj):
        values = obj.integrations_facebook_page_post_reactions_set.values_list(
            'value', flat=True)
        return sum(map(int, values))

    def get_total_engagement(self, obj):
        values = obj.integrations_facebook_page_post_engagements_set.values_list(
            'value', flat=True)
        return sum(map(int, values))

    def get_impressions(self, obj):
        post_impressions = obj.integrations_facebook_page_post_impressions_set.values(
            'title', 'value')
        return aggregate_values_by_title(post_impressions, 'title', 'value')

    def get_reactions(self, obj):
        post_reactions = obj.integrations_facebook_page_post_reactions_set.values(
            'title', 'value')
        return aggregate_values_by_title(post_reactions, 'title', 'value')

    def get_engagement(self, obj):
        post_engagements = obj.integrations_facebook_page_post_engagements_set.values(
            'title', 'value')
        return aggregate_values_by_title(post_engagements, 'title', 'value')


class TimelineFeedInstagramInsightsSummarySerializer(serializers.HyperlinkedModelSerializer):
    total_engagement = serializers.SerializerMethodField()
    total_impressions = serializers.SerializerMethodField()
    total_reach = serializers.SerializerMethodField()
    total_saved = serializers.SerializerMethodField()
    total_video_views = serializers.SerializerMethodField()

    class Meta:
        model = Integrations_Instagram_Media_Objects
        fields = [
            'media_id',
            'user_iden',
            'caption',
            'comments_count',
            'permalink',
            'total_engagement',
            'total_impressions',
            'total_reach',
            'total_saved',
            'total_video_views',
            'timestamp',
            'media_url'
        ]

    def get_total_engagement(self, obj):
        values = obj.integrations_instagram_media_insights_engagements_set.values_list(
            'value', flat=True)
        return sum(map(int, values))

    def get_total_impressions(self, obj):
        values = obj.integrations_instagram_media_insights_impressions_set.values_list(
            'value', flat=True)
        return sum(map(int, values))

    def get_total_reach(self, obj):
        values = obj.integrations_instagram_media_insights_reach_set.values_list(
            'value', flat=True)
        return sum(map(int, values))

    def get_total_saved(self, obj):
        values = obj.integrations_instagram_media_insights_saved_set.values_list(
            'value', flat=True)
        return sum(map(int, values))

    def get_total_video_views(self, obj):
        values = obj.integrations_instagram_media_insights_video_views_set.values_list(
            'value', flat=True)
        return sum(map(int, values))


class TimelineFeedInstagramStoriesSummarySerializer(serializers.HyperlinkedModelSerializer):
    total_exits = serializers.SerializerMethodField()
    total_replies = serializers.SerializerMethodField()
    total_taps_fwd = serializers.SerializerMethodField()
    total_taps_back = serializers.SerializerMethodField()

    class Meta:
        model = Integrations_Instagram_Media_Objects
        fields = [
            'media_id',
            'user_iden',
            'caption',
            'comments_count',
            'permalink',
            'total_exits',
            'total_replies',
            'total_taps_fwd',
            'total_taps_back',
            'timestamp',
            'media_url'
        ]

    def get_total_exits(self, obj):
        values = obj.integrations_instagram_media_insights_story_exits_set.values_list(
            'value', flat=True)
        return sum(map(int, values))

    def get_total_replies(self, obj):
        values = obj.integrations_instagram_media_insights_story_replies_set.values_list(
            'value', flat=True)
        return sum(map(int, values))

    def get_total_taps_fwd(self, obj):
        values = obj.integrations_instagram_media_insights_story_taps_fwd_set.values_list(
            'value', flat=True)
        return sum(map(int, values))

    def get_total_taps_back(self, obj):
        values = obj.integrations_instagram_media_insights_story_taps_back_set.values_list(
            'value', flat=True)
        return sum(map(int, values))

class TimelineFeedGoogleWebsiteViewsSerializer(serializers.HyperlinkedModelSerializer):
    date_gte = serializers.DateTimeField()
    date_lt = serializers.DateTimeField()

    class Meta:
        model = Integrations_Google_Website_Total
        fields = [
            'page_views',
            'user_iden',
            'date_gte',
            'date_lt'
        ]

class TimelineFeedShopifyRefundsSerializer(serializers.HyperlinkedModelSerializer):
    product_sku = serializers.CharField(source='line_item_ref.sku', read_only=True)
    product_title = serializers.CharField(source='line_item_ref.title', read_only=True)
    product_name = serializers.CharField(source='line_item_ref.name', read_only=True)
    refund_creation_time = serializers.DateTimeField(source='refund.created_at', read_only=True)

    class Meta:
        model = Integrations_Shopify_Refund_Line_Item
        fields = [
            'refund_line_item_id',
            'line_item_id',
            'quantity',
            'restock_type',
            'subtotal',
            'total_tax',

            'product_sku',
            'product_title',
            'product_name',

            'refund_creation_time'
        ]

class TimelineFeedShopifySingleOrderCustomerSerializer(serializers.HyperlinkedModelSerializer):
    # Integrations_Shopify_Order
    order_created_at = serializers.DateTimeField(source='order.created_at', read_only=True)
    order_order_id = serializers.CharField(source='order.order_id', read_only=True)
    order_total_price = serializers.DecimalField(max_digits=10, decimal_places=2, default=0, source='order.total_price', read_only=True)
    order_total_tax = serializers.DecimalField(max_digits=10, decimal_places=2, source='order.total_tax', read_only=True)
    order_total_discounts = serializers.DecimalField(max_digits=10, decimal_places=2, source='order.total_discounts', read_only=True)
    order_total_line_items_price = serializers.DecimalField(max_digits=10, decimal_places=2, default=0, source='order.total_line_items_price', read_only=True)
    order_total_tip_received = serializers.DecimalField(max_digits=12, decimal_places=2, source='order.total_tip_received', read_only=True)
    order_user_iden = serializers.CharField(source='order.user_iden', read_only=True)

    # Integrations_Shopify_Customer
    customer_first_name = serializers.CharField(source='order.customer_ref.first_name', read_only=True)
    customer_last_name = serializers.CharField(source='order.customer_ref.last_name', read_only=True)
    customer_state = serializers.CharField(source='order.customer_ref.state', read_only=True)
    customer_total_spent = serializers.CharField(source='order.customer_ref.total_spent', read_only=True)
    customer_orders_count = serializers.CharField(source='order.customer_ref.orders_count', read_only=True)

    class Meta:
        model = Integrations_Shopify_Line_Item
        fields = [
            # Integrations_Shopify_Line_Item
            'line_item_id',
            'price',
            'product_id',
            'quantity',
            'sku',
            'title',
            'name',

            # Integrations_Shopify_Order
            'order_created_at',
            'order_order_id',
            'order_total_price',
            'order_total_tax',
            'order_total_discounts',
            'order_total_line_items_price',
            'order_total_tip_received',
            'order_user_iden',

            # Integrations_Shopify_Customer
            'customer_first_name',
            'customer_last_name',
            'customer_state',
            'customer_total_spent',
            'customer_orders_count'
        ]