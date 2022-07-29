from blocklight_api.filters import InsightListFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import views, generics, mixins, viewsets
from django.db.models import Sum, OuterRef, Subquery, IntegerField
from django.db.models import Count
from .base_views import TimelineViewSet, BaseDatasourceViewSet
from blocklight_api.serializers.core_serializers import ChartDataSerializer
import hashlib
import datetime
import logging
from blocklight_api.models import (
    Integration
)

from blocklight_api.pagination import (
    TimelineResultsCustomPagination
)

from blocklight_api.serializers import (
    TimelineFeedShopifyOrderSerializer,
    TimelineFeedMailChimpCampaignReportSerializer,
    TimelineFeedShopifyAbandonedCheckoutSerializer,
    TimelineFeedQuickbooksAccountInfoSerializer,
    TimelineFeedQuickbooksBillSerializer,
    TimelineFeedEtsyOrderSerializer,
    TimelineFeedTwitterMentionSerializer,
    TimelineEntrySerializer,
    TimelineInsightsSerializer,
    TimelineFeedFacebookPagePostsSummarySerializer,
    TimelineFeedInstagramInsightsSummarySerializer,
    TimelineFeedInstagramStoriesSummarySerializer,
    TimelineInsightDataSerializer,
    TimelineFeedGoogleWebsiteViewsSerializer,
    TimelineFeedShopifyRefundsSerializer,
    TimelineFeedShopifySingleOrderCustomerSerializer
)

from dashboards.models import(
    Integrations_Shopify_Order,
    Integrations_MailChimp_CampaignReports,
    Integrations_Shopify_Abandoned_Checkouts,
    Integrations_Quickbooks_Account_Info,
    Integrations_Quickbooks_Bills,
    Integrations_Etsy_Receipt,
    Integrations_Twitter_Mentions,
    TimeLine_Entry,
    Integrations_Facebook_Page_Posts,
    Integrations_Facebook_Page_Post_Impressions,
    Integrations_Facebook_Page_Post_Engagements,
    Integrations_Facebook_Page_Post_Reactions,
    Integrations_Instagram_Media_Objects,
    Integrations_Instagram_Media_Insights_Engagements,
    Integrations_Instagram_Media_Insights_Impressions,
    Integrations_Instagram_Media_Insights_Reach,
    Integrations_Instagram_Media_Insights_Saved,
    Integrations_Instagram_Media_Insights_Video_Views,
    Integrations_Instagram_Media_Insights_Story_Exits,
    Integrations_Instagram_Media_Insights_Story_Replies,
    Integrations_Instagram_Media_Insights_Story_Taps_Fwd,
    Integrations_Instagram_Media_Insights_Story_Taps_Back,
    Integrations_Google_Website_Total,
    Integrations_Shopify_Refund_Line_Item,
    Integrations_Shopify_Line_Item
)

from dashboards.enums import CoreEnums

from django.core.paginator import Paginator
from django.utils import datastructures


logger = logging.getLogger(__name__)


class TimelineFeedShopifyOrderViewSet(TimelineViewSet):
    basename = "shopify_orders"
    src = 'shopify'
    route_name = "shopify_order_feed"
    serializer_class = TimelineFeedShopifyOrderSerializer
    ts_field = 'created_at'
    composite_key = ['order_id']
    format_kwarg = 'None'
    social_account_field = 'integration'

    def get_queryset(self):
        return Integrations_Shopify_Order.objects.filter(user_iden=self.request.user.id).order_by('-created_at')


class TimelineFeedShopifyAbandonedCheckoutViewSet(TimelineViewSet):
    basename = "carts"
    src = 'shopify'
    route_name = "shopify_abandoned_carts_feed"
    serializer_class = TimelineFeedShopifyAbandonedCheckoutSerializer
    ts_field = 'created_at'
    composite_key = ['checkout_id']
    format_kwarg = 'None'
    social_account_field = 'integration'

    def get_queryset(self):
        return Integrations_Shopify_Abandoned_Checkouts.objects.filter(user_iden=self.request.user.id).order_by('-created_at')

    @action(detail=False, methods=['POST'])
    def recover_cart(self, request, pk=None):
        return Response(
            status=200,
            data="sent recovery email"
        )


class TimelineFeedMailchimpCampaignReportViewSet(TimelineViewSet):
    basename = "campaigns"
    src = 'mailchimp'
    route_name = "mailchimp_campaign_reports_feed"
    ts_field = ['campaign_ref', 'send_time']
    composite_key = ['campaign_id']
    serializer_class = TimelineFeedMailChimpCampaignReportSerializer
    format_kwarg = 'None'

    def get_queryset(self):
        return Integrations_MailChimp_CampaignReports.objects.filter(user_iden=self.request.user.id).order_by('-create_time').exclude(opens=int("0"))


class TimelineFeedQuickbooksAccountInfoViewSet(TimelineViewSet):
    basename = "accounts"
    src = 'quickbooks'
    route_name = "quickbooks_account_info_feed"
    ts_field = 'last_update_time'
    composite_key = ['account_id', 'create_time',
                     'current_balance', 'name']
    serializer_class = TimelineFeedQuickbooksAccountInfoSerializer
    format_kwarg = 'None'

    def get_queryset(self):
        return Integrations_Quickbooks_Account_Info.objects.filter(user_iden=self.request.user.id).order_by('-last_update_time').exclude(active='False')


class TimelineFeedEtsyOrderViewSet(TimelineViewSet):
    basename = "etsy_orders"
    src = 'etsy'
    route_name = "etsy_order_feed"
    ts_field = "creation_tsz"
    composite_key = ['receipt_id']
    serializer_class = TimelineFeedEtsyOrderSerializer
    format_kwarg = 'None'

    def get_queryset(self):
        return Integrations_Etsy_Receipt.objects.filter(user_iden=self.request.user.id).order_by('-creation_tsz').exclude(buyer_adjusted_grandtotal='0.00')


class TimelineFeedQuickbooksBillViewSet(TimelineViewSet):
    basename = "bills"
    src = 'quickbooks'
    route_name = "quickbooks_bill_feed"
    ts_field = 'create_time'
    composite_key = ['bill_id', 'user_iden', 'account_name', 'vendor_name']
    serializer_class = TimelineFeedQuickbooksBillSerializer
    format_kwarg = 'None'

    def get_queryset(self):
        return Integrations_Quickbooks_Bills.objects.filter(user_iden=self.request.user.id).order_by('-create_time')


class TimelineFeedTwitterMentionViewSet(TimelineViewSet):
    basename = "twitter_mentions"
    src = 'twitter'
    route_name = "twitter_mentions_feed"
    ts_field = ['timestamp']
    composite_key = ['mention_id']
    serializer_class = TimelineFeedTwitterMentionSerializer
    format_kwarg = 'None'

    def get_queryset(self):
        return Integrations_Twitter_Mentions.objects.filter(user_iden=self.request.user.id).order_by('-timestamp')


class TimelineFeedFacebookPagePostsSummaryViewSet(TimelineViewSet):
    basename = "facebook_page_posts_summary"
    route_name = "facebook_page_posts_summary_feed"
    src = 'facebook'
    composite_key = ['post_id', 'user_iden']
    ts_field = ['created_time']
    serializer_class = TimelineFeedFacebookPagePostsSummarySerializer
    format_kwarg = 'None'

    def get_queryset(self):
        return Integrations_Facebook_Page_Posts.objects.filter(user_iden=self.request.user.id).order_by('-created_time')


class TimelineFeedInstagramInsightsSummaryViewSet(TimelineViewSet):
    basename = "instagram_insights_summary"
    route_name = "instagram_insights_summary_feed"
    src = 'instagram'
    composite_key = ['media_id', 'user_iden']
    ts_field = ['timestamp']
    serializer_class = TimelineFeedInstagramInsightsSummarySerializer
    format_kwarg = 'None'

    def get_queryset(self):
        return Integrations_Instagram_Media_Objects.objects.filter(user_iden=self.request.user.id, is_story=False).order_by('-timestamp')


class TimelineFeedInstagramStoriesSummaryViewSet(TimelineViewSet):
    basename = "instagram_stories_summary"
    route_name = "instagram_stories_summary_feed"
    src = 'instagram'
    composite_key = ['media_id', 'user_iden']
    ts_field = ['timestamp']
    serializer_class = TimelineFeedInstagramStoriesSummarySerializer
    format_kwarg = 'None'

    def get_queryset(self):
        return Integrations_Instagram_Media_Objects.objects.filter(user_iden=self.request.user.id, is_story=True).order_by('-timestamp')

class TimelineFeedGoogleWebsiteViewsViewSet(TimelineViewSet):
    basename = "google_website_views"
    route_name = "google_website_views_feed"
    src = 'google'
    composite_key = ['user_iden']
    ts_field = ['date_lt']
    serializer_class = TimelineFeedGoogleWebsiteViewsSerializer
    format_kwarg = 'None'

    def get_queryset(self):
        data = Integrations_Google_Website_Total.objects.filter(user_iden=self.request.user.id).order_by('-datehour')
        weekly_data = []
        i = 0
        if len(data) > 0:
            date = data[0].datehour
        else:
            return []
        # turn the time into 00:00:00
        date = datetime.datetime(year=date.year, month=date.month, day=date.day, hour=0, second=0)
        # find the nearest monday before the date
        last_monday = date - datetime.timedelta(days=date.weekday())
        views_in_week = 0

        while i < len(data):
            date = data[i].datehour
            # turn the time into 00:00:00
            date = datetime.datetime(year=date.year, month=date.month, day=date.day, hour=0, second=0)

            if date < last_monday:
                weekly_data.append({
                    'page_views' : views_in_week,
                    'date_gte' : last_monday,
                    'date_lt' : last_monday + datetime.timedelta(weeks=1),
                    'user_iden' : self.request.user.id,
                })
                # find the nearest monday before the date
                last_monday = date - datetime.timedelta(days=date.weekday())
                views_in_week = 0
            views_in_week += data[i].page_views
            i += 1

        return weekly_data

class TimelineFeedShopifyRefundsViewSet(TimelineViewSet):
    basename = "shopify_refunds"
    route_name = "shopify_refunds_feed"
    src = 'shopify'
    composite_key = ['refund_line_item_id','line_item_id']
    ts_field = ['refund_creation_time']
    serializer_class = TimelineFeedShopifyRefundsSerializer
    format_kwarg = 'None'

    def get_queryset(self):
        return Integrations_Shopify_Refund_Line_Item.objects.filter(line_item_ref__product_ref__user_iden=self.request.user.id).order_by('-refund__created_at')

class TimelineFeedShopifySingleOrderCustomerViewSet(TimelineViewSet):
    basename = "shopify_single_order_customer"
    route_name = "shopify_single_order_customer_feed"
    src = 'shopify'
    composite_key = ['line_item_id','order_order_id']
    ts_field = ['order_created_at']
    serializer_class = TimelineFeedShopifySingleOrderCustomerSerializer
    format_kwarg = 'None'

    def get_queryset(self):
        return Integrations_Shopify_Line_Item.objects.filter(order__user_iden=self.request.user.id, order__customer_ref__orders_count=1).order_by('-order__created_at')

class TimeLineView(generics.ListAPIView):
    basename = "timeline"
    route_name = "consolidate"
    queryset = []
    page_size = 100
    # paginate_by = None
    # paginate_by_param = None  # added to turn off pagination for requests that contain paginate_by_param
    # pagination_class = NullPaginationClass

    viewsets = [TimelineFeedShopifyOrderViewSet,
                TimelineFeedShopifyAbandonedCheckoutViewSet,
                TimelineFeedMailchimpCampaignReportViewSet,
                TimelineFeedQuickbooksAccountInfoViewSet,
                TimelineFeedEtsyOrderViewSet,
                TimelineFeedQuickbooksBillViewSet,
                TimelineFeedTwitterMentionViewSet,
                TimelineFeedFacebookPagePostsSummaryViewSet,
                TimelineFeedInstagramInsightsSummaryViewSet,
                TimelineFeedInstagramStoriesSummaryViewSet,
                TimelineFeedGoogleWebsiteViewsViewSet,
                TimelineFeedShopifyRefundsViewSet,
                TimelineFeedShopifySingleOrderCustomerViewSet
                ]

    @classmethod
    def get_extra_actions(cls):
        return []

    def get_nested(self, obj, layers):
        if type(layers) == str:
            return obj.get(layers, None)

        temp = obj
    
        for k in layers:
            if not temp:
                return None
            temp = temp.get(k, None)
        return temp

    def get_viewset_counts(self, request):
        totals = []
        for vs in self.viewsets:
            vs.request = request
            query_data = vs().get_queryset()
            if type(query_data) == list:
                if len(vs().get_queryset()) > 0:
                    totals.append(len(vs().filter_queryset(
                        vs().get_queryset())))
            else:
                if vs().get_queryset().count() > 0:
                    totals.append(vs().filter_queryset(
                        vs().get_queryset()).count())
        return sum(totals)

    def get_viewset_data(self, viewset, request, page, *args, **kwargs):

        modified_request_body = dict(request.GET)
        all_pages = []
        p = 1
        while True:
            modified_request_body["page"] = [p]
            request.GET = datastructures.MultiValueDict(
                modified_request_body)
            try:
                viewset.request = request
                vs = viewset()
                data = vs.list(viewset.request).data

                next_url = data['next']
                res = data["results"]

                all_pages.extend(res)
                if next_url and p < page and len(res) > 0:
                    p += 1
                else:
                    break

            except Exception as e:
                print(e)
                break

        return all_pages

    def create_hash_id(self, entry, keylist, route_name):
        raw_composite = route_name
        for key in keylist:
            v = entry.get(key, None)
            if not v:
                return None
            raw_composite += (entry.get(key, ""))

        hashedString = hashlib.md5(
            bytes(raw_composite, 'utf-8')).hexdigest()
        return hashedString

    def transform(self, viewset, request, page):
        
        purified = list(

            map(
                lambda entry: {
                    "insight": viewset.route_name,
                    "src": viewset.src,
                    "entry_id": self.create_hash_id(entry,
                                                    viewset.composite_key,
                                                    viewset.route_name),
                    "data": entry,
                    "ts": self.get_nested(entry, viewset.ts_field)

                },
                self.get_viewset_data(viewset, request, page)
            )
        )

        purified = list(
            filter(lambda obj: obj['entry_id'] is not None, purified))
        return purified

    def list(self, request, *args, **kwargs):

        try:
            page = int(request.GET["page"])
        except KeyError:
            page = 1

        responses = list(
            map(
                lambda vs: self.transform(vs, request, page),
                self.viewsets
            )
        )

        result = []
        for set in responses:
            result.extend(set)
        resp = sorted(
            result,
            key=lambda obj: obj["ts"]
        )[::-1]

        paginator = Paginator(resp, self.page_size)
        max_page = paginator.num_pages
        if len(resp) < self.page_size:
            pn = 1
        else:
            pn = page

        page_obj = paginator.get_page(pn)

        previousPG, nextPG = None, None
        url = self.request.build_absolute_uri()
        last = url.find("?")
        if last != -1:
            url = url[0:last]
        if pn > 1:
            previousPG = pn - 1
            previousPG = "{}?page={}".format(url, previousPG)

        if pn < max_page:
            nextPG = pn + 1
            nextPG = "{}?page={}".format(url, nextPG)

        return Response({
            "count": self.get_viewset_counts(request),
            "next": nextPG,
            "previous": previousPG,
            "results": list(page_obj)
        }
        )


views = [
    TimelineFeedShopifyOrderViewSet,
    TimelineFeedShopifyAbandonedCheckoutViewSet,
    TimelineFeedMailchimpCampaignReportViewSet,
    TimelineFeedQuickbooksAccountInfoViewSet,
    TimelineFeedQuickbooksBillViewSet,
    TimelineFeedEtsyOrderViewSet,
    TimelineFeedTwitterMentionViewSet,
    TimelineFeedFacebookPagePostsSummaryViewSet,
    TimelineFeedInstagramInsightsSummaryViewSet,
    TimelineFeedInstagramStoriesSummaryViewSet,
    TimelineFeedGoogleWebsiteViewsViewSet,
    TimelineFeedShopifyRefundsViewSet,
    TimelineFeedShopifySingleOrderCustomerViewSet
]


class TimeLineViewSet(BaseDatasourceViewSet):

    queryset = TimeLine_Entry.objects.all().order_by('-ts')
    social_account_field = 'integration'
    serializer_class = TimelineEntrySerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_id'
    since_until_field = 'ts'
    filterset_class = InsightListFilter
    main_timeline = True
    pagination_class = TimelineResultsCustomPagination


class TimeLineInsightsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    basename = "timeline_insights"
    route_name = "data"
    queryset = []

    @classmethod
    def get_extra_actions(cls):
        return []

    def list(self, request, *args, **kwargs):
        integration_list = Integration.objects.values('name').distinct()
        insight_list = [integration["name"] for integration in integration_list]
        # can probably clean this up
        response_data = {"data": {}}
        base_timeline_data = TimeLine_Entry.objects.values('insight').distinct()
        for insight in insight_list:
            for endpoint in base_timeline_data:
                endpoint = endpoint["insight"]
                endpoint_parsed = endpoint.split("_")
                if insight in endpoint_parsed:
                    if insight not in response_data["data"]:
                        response_data["data"][insight] = [endpoint]
                    else:
                        insight_list = response_data["data"][insight]
                        insight_list = insight_list.append(endpoint)
                        response_data.update({insight: insight_list})

        serializer = TimelineInsightDataSerializer(data=response_data)
        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response(serializer.errors)