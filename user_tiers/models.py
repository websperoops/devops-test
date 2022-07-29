from django.contrib.auth.models import User
from django.db import models


class Tier(models.Model):
    """
    A model to hold representations of each tier Blocklight offers.
    """

    RECURRING_PERIOD_CHOICES = (
        ('yearly', 'Yearly'),
        ('monthly', 'Monthly'),
    )

    name = models.CharField(max_length=100)
    public_name = models.CharField(max_length=100)

    price = models.IntegerField(blank=False, null=False)
    level_num = models.IntegerField(blank=False, null=False)  # this number serves to determine upgrades or downgrades
    recurring_period = models.CharField(max_length=15, choices=RECURRING_PERIOD_CHOICES)

    def __str__(self):
        return "<Tier name: {} recurring_period: {} price: {}>".format(self.name, self.recurring_period, self.price)


class UserTier(models.Model):
    """
    A model for each users current tier.
    """

    tier = models.ForeignKey(Tier, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    valid_since = models.DateField(null=False)
    valid_until = models.DateField(null=True)  # null means unlimited
    payments_start_date = models.DateField(null=True, blank=True)  # we use it to determine next payment date
    last_payment_date = models.DateField(null=True, blank=True)
    requested_tier_change = models.ForeignKey(Tier, on_delete=models.CASCADE, null=True, blank=True, related_name='+')
    requested_cancel = models.BooleanField(default=False)

    def __str__(self):
        return "<UserTier tier: {}_{} user_email: {} valid_since: {} valid_until: {}>".format(
            self.tier.name, self.tier.recurring_period, self.user.email, self.valid_since, self.valid_until)
