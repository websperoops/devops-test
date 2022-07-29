from django.conf.urls import url
from stripe_payments import views as st_payments

app_name = 'stripe_payments'
urlpatterns = [
    #  url(
    #     r'^buy_product/one_time_payment/(?P<tier_name>\w+)/(?P<recurring_period>\w+)/',
    #     st_payments.OneTimePaymentView.as_view(),
    #     name='one-time-payment'
    # ),
    url(
        r'^buy_product/recurring_payment/(?P<tier_name>\w+)/(?P<recurring_period>\w+)/',
        st_payments.RecurringPaymentView.as_view(),
        name='recurring-payment'
    ),
    url(r'^change_credit_card/', st_payments.ChangeCreditCardView.as_view(), name='change-credit-card'),
    url(r'^webhook/', st_payments.WebHookView.as_view(), name='webhook'),
]
