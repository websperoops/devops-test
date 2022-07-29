from django.conf.urls import url
from shopify_payments import views as sp_views

app_name = 'shopify_payments'
urlpatterns = [
    # url(r'^login', sp_views.ShopifyLoginView.as_view(), name='login'),
    # url(r'^login_success', sp_views.ShopifyLoginSuccessView.as_view(), name='login-success'),
    url(
        r'^buy_product/recurring_payment/(?P<tier_name>\w+)/(?P<recurring_period>\w+)/',
        sp_views.RecurringPaymentView.as_view(), name='recurring-payment'
    ),
    url(r'^accepted_payment/', sp_views.AcceptedPaymentView.as_view(), name='accepted_payment'),
    url(r'^change_tier/', sp_views.ChangeTierView.as_view(), name='change-tier'),
    url(r'^cancel_tier/', sp_views.CancelTierView.as_view(), name='cancel-tier'),
]
