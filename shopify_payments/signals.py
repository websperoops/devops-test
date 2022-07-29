import django.dispatch

shopify_payment_successful = django.dispatch.Signal(providing_args=["user"])
