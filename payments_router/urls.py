from django.conf.urls import url
from payments_router.views import RoutePaymentView, RouteChangeTierView

app_name='payments_router'
urlpatterns = [
    url(r'^route_payment/', RoutePaymentView.as_view(), name='route-payment'),
    url(r'^route_change/', RouteChangeTierView.as_view(), name='route-change'),
]
