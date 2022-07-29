from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse


class RoutePaymentView(LoginRequiredMixin, View):

    template_name = 'stripe_payments/recurring_payment.html'

    # TODO:  The way of routing is not fully secure. User could access directly the payment url which he wants, and
    #        overcome the payments done by shopify
    def get(self, request):
        if (
            ('tier' not in request.GET) or ('period' not in request.GET)
            or (not request.GET['tier']) or (not request.GET['period'])
        ):
            return "Parameters tier or period not passed"

        payments_app = 'shopify_payments' \
            if request.user.userprofile_set.last().signed_via_shopify \
            else 'stripe_payments'

        return redirect(reverse(
            '{}:recurring-payment'.format(payments_app),
            args=[request.GET['tier'], request.GET['period']]
        ))


class RouteChangeTierView(LoginRequiredMixin, View):

    template_name = 'stripe_payments/recurring_payment.html'

    # TODO:  The way of routing is not fully secure. User could access directly the payment url which he wants, and
    #        overcome the payments done by shopify
    def get(self, request):
        if (
            ('tier' not in request.GET) or ('recurring_period' not in request.GET)
            or (not request.GET['tier']) or (not request.GET['recurring_period'])
        ):
            return "Parameters tier or recurring_period not passed"

        payments_app = 'shopify_payments' \
            if request.user.userprofile_set.last().signed_via_shopify \
            else 'user_tiers'  # Yes, it is in user_tiers and not in stripe_payments

        return redirect(
            '{}?tier={}&recurring_period={}'.format(
                reverse('{}:change-tier'.format(payments_app)),
                request.GET['tier'],
                request.GET['recurring_period'],
            )
        )
