from django.conf.urls import url
from user_tiers.views import ChangeTierView, TierCancelView, RequestedTierCancelView, CancelRequestedTierCancelView, \
    SubscriptionInfoView


app_name = 'user_tiers'

urlpatterns = [
    url(r'^change_tier/', ChangeTierView.as_view(), name='change-tier'),
    url(r'^request_cancel_tier/', TierCancelView.as_view(), name='cancel-tier'),
    url(r'^cancel_requested_cancel_tier/', CancelRequestedTierCancelView.as_view(),
        name='cancel-requested-cancel-tier'),
    url(r'^cancel_requested_tier/', RequestedTierCancelView.as_view(), name='cancel-requested-tier'),
    url(r'^subscription_info/', SubscriptionInfoView.as_view(), name='subscription-info'),
]