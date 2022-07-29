from django.contrib import admin
from stripe_payments.models import PaymentIntent, SetupIntent, StripeCustomer


admin.site.register(PaymentIntent)
admin.site.register(SetupIntent)
admin.site.register(StripeCustomer)