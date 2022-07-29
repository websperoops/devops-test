from __future__ import absolute_import

from .views import *
from blocklight import settings
from dashboards.views import DashboardV2View

from django.conf.urls import url, include
from django.conf.urls.static import static


urlpatterns = [
    # url(r"^account/", include("account.urls")),
    url(r'^(?P<pk>\d+)/quickbooks/', quickbooks),
    url(r'^(?P<pk>\d+)/shopify/', shopify, name='shopify'),
    url(r'^(?P<pk>\d+)/facebook/', facebook),
    url(r'^(?P<pk>\d+)/twitter/', twitter),
    url(r'twitter/', twitter),
    url(r'social/', include('social.urls')),
    url(r'send_abandoned_cart_email', send_abandoned_cart_email),
    url(r'^(?P<pk>\d+)/mailchimp/', mailchimp),
    url(r'^(?P<pk>\d+)/google/', google),
    url(r'^sync', sync_wait),
    url(r'v2/', DashboardV2View.as_view(), name='dashboard_v2_view'),
    url(r'v2/(?P<pk>\d+)/', DashboardV2View.as_view(), name='dashboard_v2_view'),
    url(r'^(?P<pk>\d+)/view/tabview/', TabView.as_view(), name='tab_view'),
    url(r'^(?P<id>\d+)/tabadd/', TabAdd.as_view()),
    url(r'^(?P<id>\d+)/widgetadd/', WidgetAdd.as_view()),
    url(r'^(?P<id>\d+)/reportadd/', ReportAdd.as_view()),
    url(r'^(?P<pk>\d+)/modify/', modify_dash),
    url(r'^(?P<pk>\d+)/tabdelete/$', TabDelete.as_view(), name='tab_del'),
    url(r'^(?P<pk>\d+)/widgetdelete/$', WidgetDelete.as_view(), name='widget_del'),
    url(r'^integrate/shopify/', shopify_connect, name='integrate-shopify'),
    url(r'^integrations/', integrations, name='dashboards_integrations'),
    url(r'^shopify/toggle', toggle_shopify_account),
    url(r'^shopify/shop_id', get_selected_shopify_shop),
    url(r'user_iden/', get_user_id),
    url(r'^remove/google', remove_google),
    url(r'^remove/shopify', remove_shopify),
    url(r'^remove/mailchimp', remove_mailchimp),
    url(r'^remove/shipstation', remove_shipstation),
    url(r'^remove/instagram', remove_instagram),
    url(r'^remove/facebook', remove_facebook),
    url(r'^remove/twitter', remove_twitter),
    url(r'^remove/quickbooks', remove_quickbooks),
    url(r'^remove/etsy', remove_etsy),
    url(r'^shopify/gdpr/shop/redact', shopify_gdpr_shop_redact),
    url(r'^shopify/gdpr/customers/redact', shopify_gdpr_customers_redact),
    url(r'^shopify/gdpr/customers/data_request', shopify_gdpr_customers_data_request),
    url(r'^addshipstation', connectshipstation),
    url(r'^billing/declined', billing_declined),
    url(r'^shopify_signup/', shopify_signup),
    # url(r'^connectshipstation', connectshipstation),
    url(r'^homepage/', homepage, name='homepage'),
    url(r'^feedback/', feedback, name='feedback'),
    url(r'^feedback_sent/', feedback_sent, name='feedback_sent'),
    url(r'^profile/', profile, name='profile'),
    url(r'^change_password/$', change_password,
        name='change_password'),
    url(r'^modify/integrations/', ModIntegrations.as_view(), name="mod_integrate"),
    url(r'^integration_sync_status/', integration_sync_status),
    url(r'^$', dash, name="dash_home"),
    url(regex=r'^chart_data_json/$', view=chart_data_json, name='chart_data_json', ),
    url(regex=r'^stats_json/$', view=stats_json, name='stats_json', ),
    url(regex=r'^connect_google/$', view=connect_google, name='connect_google', ),
    url(
        regex=r'^update_integration_settings/$',
        view=update_integration_settings,
        name='update_integration_settings',
    ),
    url(
        regex=r'^manual_sync/$',
        view=manual_sync,
        name='manual_sync',
    ),
    url(
        regex=r'^chart_feedback/$',
        view=chart_feedback,
        name='chart_feedback',
    ),
    url(
        regex=r'^save_theme_color/$',
        view=save_theme_color,
        name='save_theme_color',
    )
]
# Route for media files in local development.
if settings.DEBUG:
    # This serves static files and media files.
    urlpatterns = urlpatterns + \
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
