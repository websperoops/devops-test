from allauth.socialaccount import providers

from blocklight_api.urls import router as blocklight_api_router
from blocklight_api.views import TimeLineView

from dashboards.views import init_shopify_billing, redirect_all_unknown_paths, request_oauth_token

from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from importlib import import_module
from layout.views import connections_redirect, profile


admin.autodiscover()


def bad(request):
    """ Simulates a server error """
    1 / 0


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^quickbooks/login/callback/', request_oauth_token),
    url(r'^bad/$', bad),
    url(r'', include('layout.urls')),
    # url(r'^polls/', include('polls.urls')),
    url(r'^facebook/login/callback/$', include('allauth.urls')),
    # url(r'^google_auth', 'dashboards.views.google_index'),
    # url(r'^oauth2callback', 'dashboards.views.auth_return'),
    url(r'^accountsauth/', redirect_all_unknown_paths),
    url(r'^', include('allauth.urls')),
    url(r'^accounts/social/connections_redirect/', connections_redirect),
    url(r'^accounts/social/signup/', include('allauth.urls')),
    url(r'^accounts/social/connections/', init_shopify_billing),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/profile', profile),
    url(r'^avatar/', include('avatar.urls')),
    url(r'^dashboards/social', include('social.urls')),
    url(r'^dashboards/', include('dashboards.urls')),
    url(r'^favicon\.ico$', RedirectView.as_view(
        url='/static/images/favicon.ico')),
    url(r'^payments/', include('payments_router.urls', namespace='payments_router')),
    url(r'^stripe/', include('stripe_payments.urls', namespace='stripe_payments')),
    url(r'^shopify_payments/', include('shopify_payments.urls', namespace='shopify_payments')),
    url(r'^tiers/', include('user_tiers.urls')),
    path(r'api/v1/', include(blocklight_api_router.urls)),
    path(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url('timeline/consolidate', TimeLineView.as_view())
]

for provider in providers.registry.get_list():
    try:

        prov_mod = import_module(provider.get_package() + '.urls')
    except ImportError:
        continue
    prov_urlpatterns = getattr(prov_mod, 'urlpatterns', None)
    if prov_urlpatterns:
        urlpatterns += prov_urlpatterns
        print(prov_urlpatterns)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

    # static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
