from django.contrib.auth.models import User
from django.db import models

from user_tiers.models import Tier


class PaymentIntent(models.Model):
    """
    The Model to save Created PaymentIntents for Users.
    The records are there only until PaymentIntent is successful, then it's removed. (That's why OnoToOneField to User)
    """
    uid = models.CharField(max_length=40, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    tier = models.OneToOneField(Tier, on_delete=models.CASCADE, null=False)
    client_secret = models.CharField(max_length=100, editable=False)
    recurring_payment = models.BooleanField(default=False)

    def __str__(self):
        return "<PaymentIntent user-email: {} tier: {}_{} >".format(
            self.user.email, self.tier.name, self.tier.recurring_period
        )


class SetupIntent(models.Model):
    """
    Model to save created SetupIntents for Users.
    The record is kept only until SetupIntent is successful.
    """
    uid = models.CharField(max_length=40, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    client_secret = models.CharField(max_length=100, editable=False)
    tier = models.OneToOneField(Tier, on_delete=models.CASCADE, null=True)
    pay_after_succeeded = models.BooleanField(default=False)

    def __str__(self):
        return "<SetupIntent user-email: {} client_secret: {} >".format(self.user.email, self.client_secret)


class StripeCustomer(models.Model):
    """
    Model to keep card information(payment_method_id) of customers for monthly recurring payments.
    """
    customer_id = models.CharField(max_length=50, editable=False)
    payment_method_id = models.CharField(max_length=50, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)

    def __str__(self):
        return "<StripeCustomer user-email: {} customer_id: {} >".format(
            self.user.email,  self.customer_id)