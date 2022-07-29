# flake8: noqa
from blocklight_api.views import (
    timeline_view_list,
    shopify_views, mailchimp_views,
    google_views, facebook_views,
    instagram_views, shipstation_views,
    twitter_views, core_views, timeline_views,
    etsy_views, quickbooks_views, TimeLineView
)
from blocklight_api.views.timeline_views import TimeLineViewSet, TimeLineInsightsViewSet

from rest_framework import routers


router = routers.DefaultRouter()

router.register(r'users', core_views.UserViewSet)
router.register(r'user_profiles', core_views.UserProfileViewSet)
router.register(r'integrations', core_views.IntegrationViewSet)
router.register(r'social_accounts', core_views.SocialAccountViewSet)

router.register(r'active_subscription', core_views.ActiveSubViewSet,
                basename='active_subscription')

router.register(r'data_sources', core_views.DataSourcesViewSet)

router.register(r'charts', core_views.ChartsViewSet)
router.register(r'chart_types', core_views.ChartTypeViewSet)
router.register(r'time_ranges', core_views.TimeRangeViewSet)
router.register(r'metrics', core_views.MetricViewSet)
router.register(r'dashboards', core_views.DashboardsViewSet)
router.register(r'dashboards_layouts', core_views.DashboardsLayoutsViewSet)
router.register(r'predefined_integrations',
                core_views.PredefinedIntegrationViewSet)
router.register(r'predefined_metrics', core_views.PredefinedMetricViewSet)
router.register(r'predefined_metric_types',
                core_views.PredefinedMetricTypesViewSet)
router.register(r'predefined_chart_types',
                core_views.PredefinedChartTypesViewSet)
router.register(r'predefined_time_ranges',
                core_views.PredefinedTimeRangeViewSet)
router.register(r'summary_integrations', core_views.SummaryIntegrationViewSet)
router.register(r'summary_metrics', core_views.SummaryMetricViewSet)
router.register(r'summary_time_ranges', core_views.SummaryTimeRangeViewSet)


router.register(r'topsocial_integrations',
                core_views.TopSocialIntegrationViewSet)
router.register(r'topsocial_metrics', core_views.TopSocialMetricViewSet)
router.register(r'topsocial_timeranges', core_views.TopSocialTimeRangeViewSet)


router.register(r'shopify_customers', shopify_views.ShopifyCustomersViewSet)
router.register(r'shopify_customer_addresses',
                shopify_views.ShopifyCustomerAddressesViewSet)
router.register(r'shopify_orders', shopify_views.ShopifyOrdersViewSet)
router.register(r'shopify_order_addresses',
                shopify_views.ShopifyOrderAddressesViewSet)
router.register(r'shopify_order_line_items',
                shopify_views.ShopifyOrderLineItemsViewSet)
router.register(r'shopify_refunds', shopify_views.ShopifyRefundsViewSet)
router.register(r'shopify_refund_line_items',
                shopify_views.ShopifyRefundLineItemsViewSet)
router.register(r'shopify_order_line_items',
                shopify_views.ShopifyOrderLineItemsViewSet)
router.register(r'shopify_transactions',
                shopify_views.ShopifyTransactionsViewSet)
router.register(r'shopify_abandoned_checkouts',
                shopify_views.ShopifyAbandonedCheckoutsViewSet)
router.register(r'shopify_abandoned_checkout_line_items',
                shopify_views.ShopifyAbandonedCheckoutLineItemsViewSet)
router.register(r'shopify_product_images',
                shopify_views.ShopifyProductImagesViewSet)
router.register(r'shopify_products', shopify_views.ShopifyProductsViewSet)
router.register(r'shopify_product_variants',
                shopify_views.ShopifyProductVariantsViewSet)
router.register(r'shopify_shipping_lines',
                shopify_views.ShopifyShippingLinesViewSet)
router.register(r'shopify_shop_discount_codes',
                shopify_views.ShopifyShopDiscountCodesViewSet)
router.register(r'shopify_bl_insights_refunds_marketing_acceptance',
                shopify_views.ShopifyBlInsightsRefundMarketingAcceptanceViewSet, basename="refund_marketing_acceptance")
router.register(r'shopify_bl_insights_customer_last_order_info',
                shopify_views.ShopifyBlInsightsCustomerLastOrderInfoViewSet, basename="last_order_info")
router.register(r'shopify_bl_insights_top_customers',
                shopify_views.ShopifyBlInsightsTopCustomersViewSet, basename="top_customers")
router.register(r'shopify_bl_insights_top_products',
                shopify_views.ShopifyBlInsightsTopProductsViewSet, basename="top_products")
router.register(r'shopify_bl_insights_top_customer_never_used_a_discount',
                shopify_views.ShopifyBlInsightsTopCustomersNeverUsedADiscountViewSet, basename="never_user_a_discount")
router.register(r'shopify_bl_insights_all_refunds',
                shopify_views.ShopifyBlInsightsRefundsViewSet, basename="all_refunds")

router.register(r'mailchimp_campaign_reports',
                mailchimp_views.MailchimpCampaignReportsViewSet)
router.register(r'mailchimp_campaigns',
                mailchimp_views.MailchimpCampaignsViewSet)
router.register(r'mailchimp_list_members',
                mailchimp_views.MailchimpListMembersViewSet)
router.register(r'mailchimp_lists', mailchimp_views.MailchimpListsViewSet)
router.register(r'mailchimp_list_stats',
                mailchimp_views.MailchimpListStatsViewSet)
router.register(r'mailchimp_bl_insights_campaigns',
                mailchimp_views.MailchimpBlInsightsCampaignsViewSet, basename='campaign_insights')

router.register(r'google_analytics_accounts',
                google_views.GoogleAnalyticsAccountsViewSet)
router.register(r'google_web_properties',
                google_views.GoogleWebPropertiesViewSet)
router.register(r'google_profiles', google_views.GoogleProfilesViewSet)
router.register(r'google_page_titles', google_views.GooglePageTitlesViewSet)
router.register(r'google_geolocations', google_views.GoogleGeolocationsViewSet)
router.register(r'google_mediums', google_views.GoogleMediumsViewSet)
router.register(r'google_social_networks',
                google_views.GoogleSocialNetworksViewSet)
router.register(r'google_sources', google_views.GoogleSourcesViewSet)
router.register(r'google_user_types', google_views.GoogleUserTypesViewSet)
router.register(r'google_website_totals',
                google_views.GoogleWebsiteTotalsViewSet)

router.register(r'facebook_demographics',
                facebook_views.FacebookDemographicsViewSet)
router.register(r'facebook_engagements',
                facebook_views.FacebookEngagementsViewSet)
router.register(r'facebook_impressions',
                facebook_views.FacebookImpressionsViewSet)
router.register(r'facebook_posts', facebook_views.FacebookPostsViewSet)
router.register(r'facebook_reactions', facebook_views.FacebookReactionsViewSet)
router.register(r'facebook_views', facebook_views.FacebookViewsViewSet)

router.register(r'facebook_page_posts',
                facebook_views.FacebookPagePostsViewSet)
router.register(r'facebook_page_post_impressions',
                facebook_views.FacebookPagePostImpressionsViewSet, basename="impressions")
router.register(r'facebook_page_post_engagements',
                facebook_views.FacebookPagePostEngagementsViewSet, basename="engagements")
router.register(r'facebook_page_post_reactions',
                facebook_views.FacebookPagePostReactionsViewSet, basename="reactions")

router.register(r'instagram_followers',
                instagram_views.InstagramFollowersViewSet)
router.register(r'instagram_impressions',
                instagram_views.InstagramImpressionsViewSet)
router.register(r'instagram_reaches', instagram_views.InstagramReachesViewSet)

router.register(r'instagram_media_objects',
                instagram_views.InstagramMediaObjectsViewSet)
router.register(r'instagram_media_insights_engagements',
                instagram_views.InstagramMediaInsightsEngagementsViewSet)
router.register(r'instagram_media_insights_impressions',
                instagram_views.InstagramMediaInsightsImpressionsViewSet)
router.register(r'instagram_media_insights_reach',
                instagram_views.InstagramMediaInsightsReachViewSet)

router.register(r'instagram_media_insights_saved',
                instagram_views.InstagramMediaInsightsSavedViewSet)
router.register(r'instagram_media_insights_video_views',
                instagram_views.InstagramMediaInsightsVideoViewsViewSet)
router.register(r'instagram_media_insights_story_exits',
                instagram_views.InstagramMediaInsightsStoryExitsViewSet)
router.register(r'instagram_media_insights_story_replies',
                instagram_views.InstagramMediaInsightsStoryRepliesViewSet)
router.register(r'instagram_media_insights_story_taps_fwd',
                instagram_views.InstagramMediaInsightsStoryTapsFwdViewSet)
router.register(r'instagram_media_insights_story_taps_back',
                instagram_views.InstagramMediaInsightsStoryTapsBackViewSet)

router.register(r'shipstation_fulfillments',
                shipstation_views.ShipstationFulfillmentsViewSet)
router.register(r'shipstation_order_items',
                shipstation_views.ShipstationOrderItemsViewSet)
router.register(r'shipstation_orders',
                shipstation_views.ShipstationOrdersViewSet)
router.register(r'shipstation_shipments',
                shipstation_views.ShipstationShipmentsViewSet)
router.register(r'shipstation_tags', shipstation_views.ShipstationTagsViewSet)
router.register(r'shipstation_warehouses',
                shipstation_views.ShipstationWarehousesViewSet)

router.register(r'twitter_mentions', twitter_views.TwitterMentionsViewSet)

router.register(r'etsy_users', etsy_views.EtsyUserViewSet,
                basename='etsy_users')
router.register(r'etsy_ledgers', etsy_views.EtsyLedgerViewSet,
                basename='etsy_ledgers')
router.register(r'etsy_listings', etsy_views.EtsyListingViewSet,
                basename='etsy_listing')
router.register(r'etsy_listing_products',
                etsy_views.EtsyListingProductViewSet, basename='etsy_listing_products')
router.register(r'etsy_receipts', etsy_views.EtsyReceiptViewSet,
                basename='etsy_receipts')
router.register(r'etsy_receipt_payments',
                etsy_views.EtsyReceiptPaymentViewSet, basename='etsy_receipt_payments')
router.register(r'etsy_receipt_payment_adjustments',
                etsy_views.EtsyReceiptPaymentAdjustmentViewSet, basename='etsy_receipt_adjustments')
router.register(r'etsy_receipt_payment_adjustment_items',
                etsy_views.EtsyReceiptPaymentAdjustmentItemViewSet, basename='etsy_receipt_adjustment_items')
router.register(r'etsy_receipt_shipments',
                etsy_views.EtsyReceiptShipmentViewSet, basename='etsy_receipt_shipments')
router.register(r'etsy_transactions',
                etsy_views.EtsyTransactionViewSet, basename='etsy_transactions')
router.register(r'etsy_transaction_tags',
                etsy_views.EtsyTransactionTagViewSet, basename='etsy_tags')
router.register(r'etsy_transaction_materials',
                etsy_views.EtsyTransactionMaterialViewSet, basename='etsy_materials')

router.register(r'quickbooks_accounts',
                quickbooks_views.QuickbooksAccountViewSet, basename='quickbooks_accounts')
router.register(r'quickbooks_company_info',
                quickbooks_views.QuickbooksCompanyViewSet, basename='quickbooks_company_info')
router.register(r'quickbooks_bills',
                quickbooks_views.QuickbooksBillViewSet, basename='quickbooks_bills')
router.register(r'quickbooks_bill_line_items',
                quickbooks_views.QuickbooksBillLineItemViewSet, basename='quickbooks_bill_line_items')
router.register(r'quickbooks_ledger_reports',
                quickbooks_views.QuickbooksLedgerReportViewSet, basename='quickbooks_ledger_reports')
router.register(r'quickbooks_ledger_expenses',
                quickbooks_views.QuickbooksLedgerExpenseViewSet, basename='quickbooks_ledger_expenses')


# TODO: Decide on using above method, or below

for view in timeline_view_list:
    router.register("timeline/"+view.route_name, view, basename=view.basename)

router.register(r'business_timeline', TimeLineViewSet,
                basename='business_timeline')

router.register(r'timeline_insights', TimeLineInsightsViewSet,
                basename='timeline_insights')
