from django.conf import settings
from django.conf.urls import *
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from layout.views import *
import layout.views as core_views

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls


admin.autodiscover()


urlpatterns = [
    url(r'^$', home),
    # url(r'^about/', about),
    url(r'^support/', support),
    url(r'^privacy/', privacy),
    url(r'^contact/', contact),
    url(r'^login/', login),
    url(r'^login_activated/', login_activated),
    url(r'^router/', router),
    url(r'^faq/', faq),
    url(r'^tos/', tos),
    url(r'^roadmap/', roadmap),
    url(r'^bbm/', bbm),
    url(r'^about/', about),
    url(r'^bap/', bap),
    url(r'^use_cases/', use_cases),
    url(r'^admin/', admin.site.urls),
    url(r'^signup/', signup),
    url(r'^signup_complete/', signup_complete, name='signup_complete'),
    url(r'^signup_failure/', signup_failure, name='signup_failure'),
    path(r'^accounts/activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        core_views.activate, name='activate'),
    url(r'^set_password/', set_password),
    url(r'^accounts/password/reset/', forgot_password),
    path(r'^accounts/password/key/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        password_reset_key, name='email_key'),
    url(r'^accounts/password/reset_complete/', forgot_password_complete, name='forgot_password_complete'),
    url(r'^accounts/new_password/', new_password, name = 'new_password'),
    url(r'^cms/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
    url(r'^pages/', include(wagtail_urls)),
    url(r'^blog/', include(wagtail_urls)),
]

# Route for media files in local development.
if settings.DEBUG:
    # This serves static files and media files.
    urlpatterns = urlpatterns + \
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
