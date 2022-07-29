import django.dispatch

stripe_payment_successful = django.dispatch.Signal(providing_args=["user"])
setup_intent_successful = django.dispatch.Signal(providing_args=["customer"])
