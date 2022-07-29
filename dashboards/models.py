from allauth.socialaccount.models import SocialAccount
from blocklight_api.models import LoyaltyCode
from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone
from allauth.socialaccount.fields import JSONField
import logging
import pytz


logger = logging.getLogger(__name__)


class TruncatingCharField(models.CharField):
    def get_prep_value(self, value):
        value = super(TruncatingCharField, self).get_prep_value(value)
        if value:
            if len(value) > self.max_length:
                logger.warning(
                    f"Had to truncate value {value} for field \"{self.verbose_name}\" in table {self.model}")
            return value[:self.max_length]
        return value


class UserProfile(models.Model):
    objects = models.Manager()
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    signed_via_shopify = models.BooleanField(default=False)
    avatar = models.TextField(null=True)
    logo = models.TextField(null=True)
    birthday = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=30, null=True, blank=True)
    business_name = models.CharField(max_length=50, null=True, blank=True)
    business_website = models.CharField(max_length=60, null=True, blank=True)
    business_details = models.CharField(max_length=500, null=True, blank=True)
    industry_type = models.CharField(max_length=30, null=True, blank=True)
    product_type = models.CharField(max_length=30, null=True, blank=True)
    employee_count = models.CharField(max_length=30, null=True, blank=True)
    sales_interest = models.BooleanField(default=False)
    finance_interest = models.BooleanField(default=False)
    marketing_interest = models.BooleanField(default=False)
    social_interest = models.BooleanField(default=False)
    other_interest = models.BooleanField(default=False)
    other_description = models.CharField(max_length=50, null=True, blank=True)
    is_owner = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    google_view_id = models.CharField(max_length=20, null=True, blank=True)
    location = models.CharField(max_length=30, null=True, blank=True)
    recovery_email = models.CharField(max_length=30, null=True, blank=True)
    job_title = models.CharField(max_length=30, null=True, blank=True)
    email_verified = models.BooleanField(default=False)
    loyalty_code = models.ForeignKey(
        LoyaltyCode, on_delete=models.PROTECT, null=True)
    accept_tos = models.BooleanField(default=False)
    forgot_password = models.BooleanField(default=False)
    email_notifications_on = models.BooleanField(default=True)
    text_notifications_on = models.BooleanField(default=False)
    light_theme = models.BooleanField(default=False)
    has_integrated_social_account = models.BooleanField(default=False)
    has_visited_dashboard = models.BooleanField(default=False)
    has_completed_profile = models.BooleanField(default=False)
    affiliate_code = models.TextField(blank=True, null=True)
    affiliate_uses = models.IntegerField(blank=True, null=True)
    last_shown_affiliate_modal = models.DateTimeField(blank=True, null=True)


# User Feedback
class Feedback(models.Model):
    objects = models.Manager()
    user_iden = models.CharField(max_length=30, null=True, blank=True)
    username = models.CharField(max_length=30, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    business_name = models.CharField(max_length=50, null=True, blank=True)
    feedback_type = models.CharField(max_length=30, null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    topic = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)


class Dashboard(models.Model):
    objects = models.Manager()
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    current_dashboard = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    is_published = models.BooleanField(default=True)
    is_blocklight_stock = models.BooleanField(default=False)
    tab_index = models.IntegerField(null=True, blank=True)
    last_viewed_date = models.DateTimeField(blank=True, null=True)
    published_date = models.DateTimeField(blank=True, null=True)

    # default_dash = models.CharField(max_length=30)

    def get_absolute_url(self):
        return reverse('dash_view', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        super(Dashboard, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.title) + "-" + str(self.id)
            self.save()

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def __getitem__(self, key):
        return self.field


class Tab(models.Model):
    title = models.CharField(max_length=200)
    dashboard = models.ForeignKey('Dashboard', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=200, unique=True)
    created_date = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        super(Tab, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = "default" + "-" + str(self.id)
            self.save()

    def __str__(self):
        return self.title


class Widget(models.Model):
    objects = models.Manager()
    user_iden = models.CharField(max_length=30, null=True, blank=True)
    is_blocklight_default = models.BooleanField(default=False)
    is_blocklight_generic = models.BooleanField(default=False)
    is_user_added = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    is_homepage_summary = models.BooleanField(default=False)
    is_favorite = models.BooleanField(default=False)

    metric = models.CharField(max_length=50, null=True, blank=True)
    display_name = models.CharField(max_length=100, null=True, blank=True)
    integration = models.CharField(max_length=50, null=True, blank=True)
    supported_options = models.TextField(blank=True, null=True)
    current_option = models.TextField(blank=True, null=True)
    supported_chart_types = models.TextField(null=True, blank=True)
    current_chart_type = models.CharField(max_length=50, null=True, blank=True)
    supported_time_periods = models.TextField(null=True, blank=True)
    current_time_period = models.CharField(
        max_length=50, null=True, blank=True)

    dashboard = models.CharField(max_length=50, null=True, blank=True)
    x_position = models.IntegerField(null=True, blank=True)
    y_position = models.IntegerField(null=True, blank=True)
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)

    # Kept from old version - not sure if necessary
    title = models.CharField(max_length=100)
    tab = models.ForeignKey(
        'Tab', on_delete=models.CASCADE, null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True)
    element = models.ForeignKey(
        'Element', on_delete=models.CASCADE, null=True, blank=True)
    report = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)

    # def save(self, *args, **kwargs):
    #    super(Widget, self).save(*args, **kwargs)
    #    if not self.slug:
    #        self.slug = str(self.id)
    #        self.save()

    # def publish(self):
    #    self.published_date = timezone.now()
    #    self.save()

    # def __str__(self):
    #    return self.title


class Report(models.Model):
    title = models.CharField(max_length=200)
    transaction_id = models.CharField(max_length=200, default=1)
    country = models.CharField(max_length=2, default='us')
    raw_data = models.TextField()
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    # additional_data = models.TextField()

    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Element(models.Model):
    title = models.CharField(max_length=200)
    key = models.CharField(max_length=10, default=1)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Unit(models.Model):
    name = models.CharField(unique=True, max_length=6)
    user_iden = models.CharField(max_length=50, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __unicode__(self):
        return self.name


# Performance boosting models
'''
Cache for fast chart loading
TODO: - need to edit to match updated views.py
'''


class Integrations_ChartData(models.Model):
    objects = models.Manager()
    last_sync_time = models.DateTimeField(default=timezone.now, null=True)
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    integration_name = models.CharField(max_length=20, null=True, blank=True)
    chart_key = models.CharField(max_length=500, blank=True, null=True)
    dataset = models.TextField(blank=True, null=True)
    user_iden = models.CharField(max_length=50, null=True, blank=True)


# Sync timer model
class Integrations_UserSettings(models.Model):
    objects = models.Manager()
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    integration_name = models.CharField(max_length=20, null=True, blank=True)
    user_iden = models.CharField(max_length=50, null=True, blank=True)
    is_autosync = models.BooleanField(default=True)
    autosync_timer = models.CharField(max_length=20, null=True, blank=True)
    options = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        try:
            user = User.objects.get(id=self.user_iden)
        except User.DoesNotExist:
            user = None

        return "<{}: {} - {} - {}>".format(
            self.__class__.__name__,
            self.integration_name,
            user.email if user else None,
            self.user_iden
        )


# Sync timer model
class Integrations_User_LastSync(models.Model):
    objects = models.Manager()
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    last_sync_time = models.DateTimeField(default=timezone.now, null=True)
    integration_name = models.CharField(
        max_length=20, null=True, blank=True, unique=False)
    dataset = models.TextField(blank=True, null=True)
    user_iden = models.CharField(max_length=50, null=True, blank=True)
    celery_key = models.CharField(max_length=100, null=True, blank=True)
    sync_is_active = models.BooleanField(default=False)
    initialize = models.BooleanField(default=False)
    checkpoint = models.CharField(max_length=10, null=True, blank=True)


# Time Stamped
class TimeStampedModel(models.Model):
    """
    Abstract base class that provides self-updating 'created' and 'modified'
    fields.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# Shopify models
class BasicAuthRecords(models.Model):
    user_iden = models.CharField(max_length=50, default='X')
    integration_name = models.CharField(max_length=50, null=True, blank=True)
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    api_key = models.CharField(max_length=50, null=True, blank=True)
    api_secret = models.CharField(max_length=50, null=True, blank=True)
    base64auth_string = models.CharField(max_length=200, null=True, blank=True)


class BlocklightBilling_Recurring_Shopify(models.Model):
    objects = models.Manager()
    user_account = models.CharField(max_length=5, null=True, blank=True)
    charge_id = models.CharField(max_length=50, null=True, blank=True)
    name = models.TextField(blank=True, null=True)
    api_client_id = models.CharField(max_length=50, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=50, null=True, blank=True)
    confirmation_url = models.TextField(blank=True, null=True)
    return_url = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, null=True)
    updated_at = models.DateTimeField(default=timezone.now, null=True)
    test = models.NullBooleanField(default=False)
    trial_days = models.CharField(max_length=2, null=True, blank=True)
    decorated_return_url = models.TextField(blank=True, null=True)


# See https://developers.google.com/analytics/devguides/config/mgmt/v3/mgmtReference/management/accountSummaries
# to see how account summaries are retunred
class Integrations_Google_Analytics_Account(models.Model):
    objects = models.Manager()
    social_account = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=False)
    name = TruncatingCharField(max_length=1024)
    account_id = models.CharField(max_length=64)


class Integrations_Google_Web_Property(models.Model):
    objects = models.Manager()
    account = models.ForeignKey(
        Integrations_Google_Analytics_Account, on_delete=models.CASCADE, null=False)
    property_id = models.CharField(max_length=30)
    internal_id = models.CharField(max_length=30)
    name = TruncatingCharField(max_length=1024)
    website_url = TruncatingCharField(max_length=1024)


# Corresponds to a View
class Integrations_Google_Profile(models.Model):
    objects = models.Manager()
    web_property = models.ForeignKey(
        Integrations_Google_Web_Property, on_delete=models.CASCADE, null=False)
    view_id = models.CharField(max_length=30, null=False)
    name = TruncatingCharField(max_length=255)
    time_zone = models.CharField(max_length=255, default="UTC")

    def __str__(self):
        return "{}(name: {}, user_id: {} user_email: {})".format(
            super(Integrations_Google_Profile, self).__str__(),
            self.name,
            self.web_property.account.social_account.user_id,
            User.objects.get(
                id=self.web_property.account.social_account.user_id)
        )


class Integrations_Google_Metric(models.Model):
    """
    Abstract base class for all models of Google Metrics.
    Includes a foreignKey reference to a Google Profile
    """
    objects = models.Manager()
    profile = models.ForeignKey(
        Integrations_Google_Profile, on_delete=models.CASCADE, null=False, db_index=True)
    last_sync_time = models.DateTimeField(default=timezone.now)
    # start_date = models.CharField(max_length=50, null=True, blank=True)
    # TODO maybe remove or add additional validation
    user_iden = models.CharField(max_length=50, null=True, blank=True)
    datehour = models.DateTimeField(null=True, db_index=True)

    class Meta:
        abstract = True  # make this an abstract class


class Integrations_Google_Medium(Integrations_Google_Metric):
    medium = TruncatingCharField(max_length=255, null=False)
    users = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('profile', 'datehour', 'medium')

    @classmethod
    def sync(cls, profile, data):
        """
        Syncs data to the table. Data is assumed to be from a report made from using Google Analytics API
        Args:
            profile: An instance of Integrations_Google_Profile
            data: a dictionary containing keys: "ga:medium", "ga:users"
        """
        datehour = pytz.timezone(profile.time_zone).localize(
            datetime.strptime(data["ga:dateHour"], "%Y%m%d%H"))
        entry, created = cls.objects.get_or_create(
            profile=profile, datehour=datehour, medium=data["ga:medium"])
        entry.user_iden = entry.profile.web_property.account.social_account.user_id
        entry.users = int(data["ga:users"])
        entry.last_sync_time = timezone.now()
        entry.save()

    @classmethod
    def create_obj(cls, data, profile, user_iden, datehour, last_sync_time):
        return cls(profile=profile, last_sync_time=last_sync_time, user_iden=user_iden, datehour=datehour,
                   medium=data["ga:medium"], users=int(data["ga:users"]))

    @staticmethod
    def get_dimensions_used():
        """
        Returns:
            A list of Google Analytics dimensions in the form of 'name' = <dimension name>
        """
        return [{"name": dim} for dim in ["ga:medium", "ga:dateHour"]]

    @staticmethod
    def get_metrics_used():
        """
        Returns:
            A list of Google Analytics metrics in the form of 'expression' = <metric name>
        """
        return [{'expression': metric} for metric in ["ga:users"]]


class Integrations_Google_Source(Integrations_Google_Metric):
    source = TruncatingCharField(max_length=50, null=False)
    has_social_referral = models.BooleanField(default=False)
    users = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('profile', 'datehour',
                           'source', 'has_social_referral')

    @classmethod
    def sync(cls, profile, data):
        """
        Syncs data to the table. Data is assumed to be from a report made from using Google Analytics API
        Args:
            profile: An instance of Integrations_Google_Profile
            start_date:
            data: a dictionary containing keys: "ga:source", "ga:hasSocialSourceReferral", and "ga:users"
        """
        has_social = True if data["ga:hasSocialSourceReferral"] == "Yes" else False
        datehour = pytz.timezone(profile.time_zone).localize(
            datetime.strptime(data["ga:dateHour"], "%Y%m%d%H"))
        entry, created = cls.objects.get_or_create(profile=profile, datehour=datehour, source=data["ga:source"],
                                                   has_social_referral=has_social)
        entry.user_iden = entry.profile.web_property.account.social_account.user_id
        entry.users = int(data["ga:users"])
        entry.last_sync_time = timezone.now()
        entry.save()

    @classmethod
    def create_obj(cls, data, profile, user_iden, datehour, last_sync_time):
        has_social = True if data["ga:hasSocialSourceReferral"] == "Yes" else False
        return cls(profile=profile, last_sync_time=last_sync_time, user_iden=user_iden, datehour=datehour,
                   source=data["ga:source"], has_social_referral=has_social, users=int(data["ga:users"]))

    @staticmethod
    def get_dimensions_used():
        """
        Returns:
            A list of Google Analytics dimensions in the form of 'name' = <dimension name>
        """
        return [{"name": dim} for dim in ["ga:source", "ga:hasSocialSourceReferral", "ga:dateHour"]]

    @staticmethod
    def get_metrics_used():
        """
        Returns:
            A list of Google Analytics metrics in the form of 'expression' = <metric name>
        """
        return [{'expression': metric} for metric in ["ga:users"]]


class Integrations_Google_Social_Network(Integrations_Google_Metric):
    social_network = TruncatingCharField(max_length=255, null=False)
    users = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('profile', 'datehour', 'social_network')

    @classmethod
    def sync(cls, profile, data):
        """
        Syncs data to the table. Data is assumed to be from a report made from using Google Analytics API
        Args:
            profile: An instance of Integrations_Google_Profile
            start_date:
            data: a dictionary containing keys: "ga:socialNetwork",  and "ga:users"
        """
        datehour = pytz.timezone(profile.time_zone).localize(
            datetime.strptime(data["ga:dateHour"], "%Y%m%d%H"))
        entry, created = cls.objects.get_or_create(profile=profile, datehour=datehour,
                                                   social_network=data["ga:socialNetwork"])
        entry.user_iden = entry.profile.web_property.account.social_account.user_id
        entry.users = int(data["ga:users"])
        entry.last_sync_time = timezone.now()
        entry.save()

    @classmethod
    def create_obj(cls, data, profile, user_iden, datehour, last_sync_time):
        return cls(profile=profile, last_sync_time=last_sync_time, user_iden=user_iden, datehour=datehour,
                   social_network=data["ga:socialNetwork"], users=int(data["ga:users"]))

    @staticmethod
    def get_dimensions_used():
        """
        Returns:
            A list of Google Analytics dimensions in the form of 'name' = <dimension name>
        """
        return [{"name": dim} for dim in ["ga:socialNetwork", "ga:dateHour"]]

    @staticmethod
    def get_metrics_used():
        """
        Returns:
            A list of Google Analytics metrics in the form of 'expression' = <metric name>
        """
        return [{'expression': metric} for metric in ["ga:users"]]


class Integrations_Google_Page_Title(Integrations_Google_Metric):
    page_title = TruncatingCharField(max_length=255, null=False)
    page_views = models.PositiveIntegerField(default=0)
    unique_page_views = models.PositiveIntegerField(default=0)
    time_on_page = models.BigIntegerField(default=0)
    exits = models.PositiveIntegerField(default=0)
    sessions = models.PositiveIntegerField(default=0)
    screen_views = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('profile', 'datehour', 'page_title')

    @classmethod
    def sync(cls, profile, data):
        """
        Syncs data to the table. Data is assumed to be from a report made from using Google Analytics API
        Args:
            profile: An instance of Integrations_Google_Profile
            data: a dictionary containing keys: "ga:pageTitle",ga:pageviews, "ga:pageviewsPerSession", "ga:timeOnPage,
            "ga:avgTimeOnPage", "ga:exits", and "ga:exitRate"
        """
        datehour = pytz.timezone(profile.time_zone).localize(
            datetime.strptime(data["ga:dateHour"], "%Y%m%d%H"))
        entry, created = cls.objects.get_or_create(
            profile=profile, datehour=datehour, page_title=data["ga:pageTitle"])
        entry.user_iden = entry.profile.web_property.account.social_account.user_id
        entry.page_views = int(data.get("ga:pageviews", entry.page_views))
        entry.unique_page_views = int(
            data.get("ga:uniquePageviews", entry.unique_page_views))
        entry.time_on_page = int(
            float(data.get("ga:timeOnPage", entry.time_on_page)))
        entry.exits = int(data.get("ga:exits", entry.exits))
        entry.sessions = int(data.get("ga:sessions", entry.sessions))
        entry.screen_views = int(
            data.get("ga:screenviews", entry.screen_views))
        entry.last_sync_time = timezone.now()
        entry.save()

    @classmethod
    def create_obj(cls, data, profile, user_iden, datehour, last_sync_time):
        return cls(profile=profile, last_sync_time=last_sync_time, user_iden=user_iden, datehour=datehour,
                   page_title=data["ga:pageTitle"], page_views=int(
                       data.get("ga:pageviews")),
                   unique_page_views=int(data.get("ga:uniquePageviews")),
                   time_on_page=int(float(data.get("ga:timeOnPage"))), exits=int(data.get("ga:exits", 0)),
                   sessions=int(data.get("ga:sessions", 0)), screen_views=int(data.get("ga:screenviews", 0)))

    @staticmethod
    def get_dimensions_used():
        """
        Returns:
            A list of Google Analytics dimensions in the form of 'name' = <dimension name>
        """
        return [{"name": dim} for dim in ["ga:pageTitle", "ga:dateHour"]]

    @staticmethod
    def get_metrics_used():
        """
        Returns:
            A list of Google Analytics metrics in the form of 'expression' = <metric name>
        """
        return [{'expression': metric} for metric in
                ["ga:pageviews", "ga:uniquePageviews", "ga:timeOnPage", "ga:exits", "ga:sessions", "ga:screenviews"]]


class Integrations_Google_User_Type(Integrations_Google_Metric):
    user_type = TruncatingCharField(max_length=255)
    users = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('profile', 'datehour', 'user_type')

    @classmethod
    def sync(cls, profile, data):
        """
        Syncs data to the table. Data is assumed to be from a report made from using Google Analytics API
        Args:
            profile: An instance of Integrations_Google_Profile
            data: a dictionary containing keys corresponding to a google analytics metric name
        """
        datehour = pytz.timezone(profile.time_zone).localize(
            datetime.strptime(data["ga:dateHour"], "%Y%m%d%H"))
        entry, created = cls.objects.get_or_create(
            profile=profile, user_type=data["ga:userType"], datehour=datehour)
        entry.users = int(data["ga:users"])
        entry.user_iden = entry.profile.web_property.account.social_account.user_id
        entry.last_sync_time = timezone.now()
        entry.save()

    @classmethod
    def create_obj(cls, data, profile, user_iden, datehour, last_sync_time):
        return cls(profile=profile, last_sync_time=last_sync_time, user_iden=user_iden, datehour=datehour,
                   user_type=data["ga:userType"], users=int(data["ga:users"]))

    @staticmethod
    def get_dimensions_used():
        """
        Returns:
            A list of Google Analytics dimensions in the form of 'name' = <dimension name>
        """
        return [{"name": dim} for dim in ["ga:userType", "ga:dateHour"]]

    @staticmethod
    def get_metrics_used():
        """
        Returns:
            A list of Google Analytics metrics in the form of 'expression' = <metric name>
        """
        return [{'expression': metric} for metric in ["ga:users"]]


class Integrations_Google_Website_Total(Integrations_Google_Metric):
    page_views = models.PositiveIntegerField(default=0)
    unique_page_views = models.PositiveIntegerField(default=0)
    time_on_page = models.BigIntegerField(default=0)
    exits = models.PositiveIntegerField(default=0)
    sessions = models.PositiveIntegerField(default=0)
    bounces = models.PositiveIntegerField(default=0)
    hits = models.PositiveIntegerField(default=0)
    screen_views = models.PositiveIntegerField(default=0)
    session_duration = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('profile', 'datehour')

    @classmethod
    def sync(cls, profile, data):
        """
        Syncs data to the table. Data is assumed to be from a report made from using Google Analytics API
        Args:
            profile: An instance of Integrations_Google_Profile
            data: a dictionary containing keys corresponding to a google analytics metric name
        """
        datehour = pytz.timezone(profile.time_zone).localize(
            datetime.strptime(data["ga:dateHour"], "%Y%m%d%H"))
        entry, created = cls.objects.get_or_create(
            profile=profile, datehour=datehour)
        entry.user_iden = entry.profile.web_property.account.social_account.user_id
        entry.page_views = int(data.get("ga:pageviews", entry.page_views))
        entry.unique_page_views = int(
            data.get("ga:uniquePageviews", entry.unique_page_views))
        entry.time_on_page = int(
            float(data.get("ga:timeOnPage", entry.time_on_page)))
        entry.exits = int(data.get("ga:exits", entry.exits))
        entry.sessions = int(data.get("ga:sessions", entry.sessions))
        entry.bounces = int(data.get("ga:bounces", entry.bounces))
        entry.hits = int(data.get("ga:hits", entry.hits))
        entry.sessions = int(data.get("ga:sessions", entry.sessions))
        entry.screen_views = int(
            data.get("ga:screenviews", entry.screen_views))
        entry.session_duration = int(
            float(data.get("ga:sessionDuration", entry.session_duration)))
        entry.last_sync_time = timezone.now()
        entry.save()

    @classmethod
    def create_obj(cls, data, profile, user_iden, datehour, last_sync_time):
        return cls(profile=profile, last_sync_time=last_sync_time, user_iden=user_iden, datehour=datehour,
                   page_views=int(data.get("ga:pageviews", 0)),
                   unique_page_views=int(data.get("ga:uniquePageviews", 0)),
                   time_on_page=int(float(data.get("ga:timeOnPage", 0.0))), exits=int(data.get("ga:exits", 0)),
                   sessions=int(data.get("ga:sessions", 0)), bounces=int(data.get("ga:bounces", 0)),
                   hits=int(data.get("ga:hits", 0)), screen_views=int(data.get("ga:screenviews", 0)),
                   session_duration=int(float(data.get("ga:sessionDuration", 0.0))))

    @staticmethod
    def get_dimensions_used():
        """
        Returns:
            A list of Google Analytics dimensions in the form of 'name' = <dimension name>
        """
        return [{"name": dim} for dim in ["ga:dateHour"]]

    @staticmethod
    def get_metrics_used():
        """
        Returns:
            A list of Google Analytics metrics in the form of 'expression' = <metric name>
        """
        return [{'expression': metric} for metric in
                ["ga:pageviews", "ga:uniquePageviews", "ga:timeOnPage", "ga:exits", "ga:sessions", "ga:bounces",
                 "ga:hits", "ga:screenviews", "ga:sessionDuration"]]


class Integrations_Google_Geolocation(Integrations_Google_Metric):
    continent = TruncatingCharField(
        max_length=32, null=False, default="(not set)")
    sub_continent = TruncatingCharField(
        max_length=128, null=False, default="(not set)")
    country = TruncatingCharField(
        max_length=64, null=False, default="(not set)")
    region = TruncatingCharField(
        max_length=255, null=False, default="(not set)")
    city = TruncatingCharField(max_length=255, null=False, default="(not set)")
    users = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('profile', 'datehour', 'continent',
                           'sub_continent', 'country', 'region', 'city')

    @classmethod
    def sync(cls, profile, data):
        """
        Syncs data to the table. Data is assumed to be from a report made from using Google Analytics API
        Args:
            profile: An instance of Integrations_Google_Profile
            data: a dictionary containing keys corresponding to a google analytics metric name
        """
        datehour = pytz.timezone(profile.time_zone).localize(
            datetime.strptime(data["ga:dateHour"], "%Y%m%d%H"))
        continent = data["ga:continent"]
        sub_continent = data["ga:subContinent"]
        country = data["ga:country"]
        region = data["ga:region"]
        city = data["ga:city"]
        entry, created = cls.objects.get_or_create(profile=profile, datehour=datehour, continent=continent,
                                                   sub_continent=sub_continent, country=country, region=region,
                                                   city=city)
        entry.user_iden = entry.profile.web_property.account.social_account.user_id
        entry.users = data["ga:users"]
        entry.last_sync_time = timezone.now()
        entry.save()

    @classmethod
    def create_obj(cls, data, profile, user_iden, datehour, last_sync_time):
        return cls(profile=profile, last_sync_time=last_sync_time, user_iden=user_iden, datehour=datehour,
                   continent=data["ga:continent"], sub_continent=data["ga:subContinent"], country=data["ga:country"],
                   region=data["ga:region"], city=data["ga:city"], users=int(data["ga:users"]))

    @staticmethod
    def get_metrics_used():
        """
        Returns:
            A list of Google Analytics metrics in the form of 'expression' = <metric name>
        """
        return [{'expression': metric} for metric in ["ga:users"]]

    @staticmethod
    def get_dimensions_used():
        """
        Returns:
            A list of Google Analytics dimensions in the form of 'name' = <dimension name>
        """
        return [{"name": dim} for dim in
                ["ga:dateHour", "ga:continent", "ga:subContinent", "ga:country", "ga:region", "ga:city"]]


##############################################################
# ShipStation - Shipments
# https://shipstation.docs.apiary.io/#reference/shipments
# ##############################################################
class Integrations_ShipStation_Shipments(models.Model):
    objects = models.Manager()
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    user_iden = models.CharField(max_length=50, null=True, blank=True)
    last_sync_time = models.DateTimeField(default=timezone.now, null=True)
    shipmentId = models.CharField(max_length=50, null=True, blank=True)
    orderId = models.CharField(max_length=50, null=True, blank=True)
    orderKey = models.CharField(max_length=50, null=True, blank=True)
    userId = models.CharField(max_length=50, null=True, blank=True)
    customerEmail = models.EmailField(max_length=100, null=True, blank=True)
    orderNumber = models.CharField(max_length=50, null=True, blank=True)
    createDate = models.DateTimeField(default=None, null=True, blank=True)
    shipDate = models.DateTimeField(default=None, null=True, blank=True)
    shipmentCost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    insuranceCost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    trackingNumber = models.CharField(max_length=100, null=True, blank=True)
    isReturnLabel = models.BooleanField(default=False)
    batchNumber = models.CharField(max_length=50, null=True, blank=True)
    carrierCode = models.CharField(max_length=50, null=True, blank=True)
    serviceCode = models.CharField(max_length=50, null=True, blank=True)
    packageCode = models.CharField(max_length=50, null=True, blank=True)
    confirmation = models.CharField(max_length=50, null=True, blank=True)
    warehouseId = models.CharField(max_length=50, null=True, blank=True)
    voided = models.BooleanField(default=False)
    voidDate = models.DateTimeField(default=None, null=True, blank=True)
    marketplaceNotified = models.BooleanField(default=False)
    notifyErrorMessage = models.TextField(blank=True, null=True)


##############################################################
# ShipStation - FulFillments
# https://shipstation.docs.apiary.io/#reference/orders
# ##############################################################
class Integrations_ShipStation_Fulfillments(models.Model):
    # objects = models.Manager()
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    user_iden = models.CharField(max_length=50, null=True, blank=True)
    last_sync_time = models.DateTimeField(default=timezone.now, null=True)
    orderId = models.CharField(max_length=50, null=True, blank=True)
    orderNumber = models.CharField(max_length=50, null=True, blank=True)
    customerEmail = models.CharField(max_length=50, null=True, blank=True)
    trackingNumber = models.CharField(max_length=100, null=True, blank=True)
    shipDate = models.DateTimeField(default=None, null=True, blank=True)
    voidDate = models.DateTimeField(default=None, null=True, blank=True)
    deliveryDate = models.DateTimeField(default=None, null=True, blank=True)
    carrierCode = models.CharField(max_length=50, null=True, blank=True)
    fulfillmentProviderCode = models.CharField(
        max_length=50, null=True, blank=True)
    fulfillmentServiceCode = models.CharField(
        max_length=50, null=True, blank=True)


# ##############################################################
# # ShipStation - OrderItems
# # https://shipstation.docs.apiary.io/#reference/orders
# # ##############################################################
# class Integrations_ShipStation_OrderItems(models.Model):
#     # objects = models.Manager()
#     integration = models.ForeignKey(SocialAccount, on_delete=models.CASCADE, null=True)
#     user_iden = models.CharField(max_length=50, null=True, blank=True)
#     last_sync_time = models.DateTimeField(default=timezone.now, null=True)
#
#     orderItemId
#     lineItemKey
#     sku
#     name
#     imageUrl
#     weight
#     quantity
#     unitPrice
#     taxAmount
#     shippingAmount
#     warehouseLocation
#     options
#     productId
#     fulfillmentSku
#     adjustment
#     upc
#     "createDate": "2016-01-18T15:28:28.67",
#     "modifyDate": "2016-01-18T15:28:28.67"
#
# },


# ShipStation - OrderItems
# https://shipstation.docs.apiary.io/#reference/orders
class Integrations_ShipStation_OrderItems(models.Model):
    # objects = models.Manager()
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    user_iden = models.CharField(max_length=50, null=True, blank=True)
    last_sync_time = models.DateTimeField(default=timezone.now, null=True)

    orderId = models.CharField(max_length=50, null=True, blank=True)
    orderNumber = models.CharField(max_length=50, null=True, blank=True)
    orderItemId = models.CharField(max_length=50, null=True, blank=True)
    lineItemKey = models.CharField(max_length=50, null=True, blank=True)
    sku = models.CharField(max_length=500, null=True, blank=True)
    name = models.CharField(max_length=500, null=True, blank=True)
    imageUrl = models.TextField(null=True, blank=True)
    weight_value = models.CharField(max_length=50, null=True, blank=True)
    weight_units = models.CharField(max_length=50, null=True, blank=True)
    quantity = models.CharField(max_length=50, null=True, blank=True)
    unitPrice = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    taxAmount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    shippingAmount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    warehouseLocation = models.CharField(max_length=50, null=True, blank=True)
    options = models.CharField(max_length=500, null=True, blank=True)
    productId = models.CharField(max_length=500, null=True, blank=True)
    fulfillmentSku = models.CharField(max_length=500, null=True, blank=True)
    adjustment = models.BooleanField(default=False)
    upc = models.CharField(max_length=500, null=True, blank=True)
    createDate = models.DateTimeField(default=None, null=True, blank=True)
    modifyDate = models.DateTimeField(default=None, null=True, blank=True)


# ShipStation - Orders
# https://shipstation.docs.apiary.io/#reference/orders
class Integrations_ShipStation_Orders(models.Model):
    # objects = models.Manager()
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    user_iden = models.CharField(max_length=50, null=True, blank=True)
    last_sync_time = models.DateTimeField(default=timezone.now, null=True)
    orderId = models.CharField(max_length=50, null=True, blank=True)
    orderNumber = models.CharField(max_length=50, null=True, blank=True)
    orderKey = models.CharField(max_length=50, null=True, blank=True)
    createDate = models.DateTimeField(default=None, null=True, blank=True)
    modifyDate = models.DateTimeField(default=None, null=True, blank=True)
    paymentDate = models.DateTimeField(default=None, null=True, blank=True)
    shipByDate = models.DateTimeField(default=None, null=True, blank=True)
    orderStatus = models.CharField(max_length=50, null=True, blank=True)
    customerId = models.CharField(max_length=50, null=True, blank=True)
    customerUsername = models.CharField(max_length=50, null=True, blank=True)
    customerNotes = models.TextField(blank=True, null=True)
    internalNotes = models.TextField(blank=True, null=True)
    requestedShippingService = models.CharField(
        max_length=200, null=True, blank=True)
    packageCode = models.CharField(max_length=50, null=True, blank=True)
    tagIds = models.CharField(max_length=50, null=True, blank=True)
    userIds = models.CharField(max_length=50, null=True, blank=True)
    externallyFulfilled = models.BooleanField(default=False)
    externallyFulfilledBy = models.CharField(
        max_length=100, null=True, blank=True)
    labelMessages = models.TextField(blank=True, null=True)

    shipTo = models.TextField(blank=True, null=True)
    shipTo_name = models.TextField(blank=True, null=True)
    shipTo_company = models.TextField(blank=True, null=True)
    shipTo_street1 = models.TextField(blank=True, null=True)
    shipTo_street2 = models.TextField(blank=True, null=True)
    shipTo_street3 = models.TextField(blank=True, null=True)
    shipTo_city = models.TextField(blank=True, null=True)
    shipTo_state = models.TextField(blank=True, null=True)
    shipTo_postalCode = models.CharField(max_length=50, null=True, blank=True)
    shipTo_country = models.CharField(max_length=5, null=True, blank=True)
    shipTo_phone = models.CharField(max_length=20, null=True, blank=True)
    shipTo_residential = models.BooleanField(default=False)

    items = models.TextField(blank=True, null=True)

    insuranceOptions_provider = models.CharField(
        max_length=100, null=True, blank=True)
    insuranceOptions_insureShipment = models.BooleanField(default=False)
    insuranceOptions_insuredValue = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)

    dimensions_units = models.CharField(max_length=50, null=True, blank=True)
    dimensions_length = models.CharField(max_length=50, null=True, blank=True)
    dimensions_width = models.CharField(max_length=50, null=True, blank=True)
    dimensions_height = models.CharField(max_length=50, null=True, blank=True)

    advancedOptions_warehouseId = models.CharField(
        max_length=50, null=True, blank=True)
    advancedOptions_nonMachineable = models.BooleanField(default=False)
    advancedOptions_saturdayDelivery = models.BooleanField(default=False)
    advancedOptions_containsAlchohol = models.BooleanField(default=False)
    advancedOptions_mergedOrSplit = models.BooleanField(default=False)
    advancedOptions_source = models.CharField(
        max_length=50, null=True, blank=True)


# ShipStation - Tags
# https://shipstation.docs.apiary.io/#reference/shipments
class Integrations_ShipStation_Tags(models.Model):
    # objects = models.Manager()
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    user_iden = models.CharField(max_length=50, null=True, blank=True)
    last_sync_time = models.DateTimeField(default=timezone.now, null=True)
    tagId = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    color = models.CharField(max_length=50, null=True, blank=True)
    last_sync_time = models.DateTimeField(default=timezone.now, null=True)


# ShipStation - Warehouses
# https://shipstation.docs.apiary.io/#reference/warehouses
class Integrations_ShipStation_Warehouses(models.Model):
    # objects = models.Manager()
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    user_iden = models.CharField(max_length=50, null=True, blank=True)
    last_sync_time = models.DateTimeField(default=timezone.now, null=True)
    warehouseId = models.CharField(max_length=50, null=True, blank=True)
    warehouseName = models.CharField(max_length=50, null=True, blank=True)
    originAddress = models.CharField(max_length=50, null=True, blank=True)
    returnAddress = models.CharField(max_length=50, null=True, blank=True)
    createDate = models.CharField(max_length=50, null=True, blank=True)
    isDefault = models.CharField(max_length=50, null=True, blank=True)
    last_sync_time = models.DateTimeField(default=timezone.now, null=True)


# https://help.shopify.com/en/api/reference/store-properties/shop
class Integrations_Shopify_Shop(models.Model):
    objects = models.Manager()
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    user_iden = models.CharField(max_length=50, null=True, blank=True)
    last_sync_time = models.DateTimeField(default=timezone.now, null=True)
    address1 = models.CharField(max_length=255, null=True)
    address2 = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255, null=True)
    country_code = models.CharField(max_length=2, null=True)
    country_name = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(null=True)
    customer_email = models.EmailField(null=True)
    currency = models.CharField(max_length=3, null=False, default="USD")
    domain = models.CharField(max_length=255, null=True)
    eligible_for_payments = models.NullBooleanField(null=True)
    email = models.EmailField(null=True)
    force_ssl = models.NullBooleanField(null=True)
    has_discounts = models.NullBooleanField(null=True)
    has_gift_cards = models.NullBooleanField(null=True)
    has_storefront = models.NullBooleanField(null=True)
    iana_timezone = models.CharField(max_length=255, null=False, default="UTC")
    shop_id = models.CharField(max_length=32, null=False)
    latitude = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    money_format = models.TextField(max_length=32, null=True)
    name = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=20, null=True)
    plan_display_name = models.CharField(max_length=255, null=True)
    plan_name = models.CharField(max_length=255, null=True)
    primary_locale = models.CharField(max_length=4, null=True)
    province = models.CharField(max_length=255, null=True)
    province_code = models.CharField(max_length=4, null=True)
    shop_owner = models.CharField(max_length=255, null=True)
    source = models.CharField(max_length=255, null=True)
    tax_shipping = models.NullBooleanField(null=True)
    updated_at = models.DateTimeField(null=True)
    weight_unit = models.CharField(max_length=20, null=True)
    zip = models.CharField(max_length=128, null=True)

    class Meta:
        unique_together = ('integration', 'shop_id')


class Integrations_Shopify_Shop_Price_Rule(models.Model):
    objects = models.Manager()
    rule_id = models.TextField(max_length=32, null=False)
    user_iden = models.CharField(max_length=50, null=True)
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    shop = models.ForeignKey(Integrations_Shopify_Shop,
                             on_delete=models.CASCADE, null=True)
    allocation_method = models.TextField(null=True)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)
    customer_selection = models.TextField(null=True)
    ends_at = models.DateTimeField(null=True)
    entitled_collection_ids = models.TextField(null=True)
    entitled_country_ids = models.TextField(null=True)
    entitled_product_ids = models.TextField(null=True)
    entitled_variant_ids = models.TextField(null=True)
    once_per_customer = models.BooleanField(default=False)
    prerequisite_customer_ids = models.TextField(null=True)
    min_prerequisite_quantity_range = models.IntegerField(null=True)
    prerequisite_saved_search_ids = models.TextField(null=True)
    max_prerequisite_shipping_price_range = models.DecimalField(
        max_digits=10, decimal_places=2, null=True)
    min_prerequisite_subtotal_range = models.DecimalField(
        max_digits=10, decimal_places=2, null=True)
    starts_at = models.DateTimeField(null=True)
    target_selection = models.TextField(null=True)
    target_type = models.TextField(null=True)
    title = models.TextField(null=True)
    usage_limit = models.IntegerField(null=True)
    prerequisite_product_ids = models.TextField(null=True)
    prerequisite_variant_ids = models.TextField(null=True)
    prerequisite_collection_ids = models.TextField(null=True)
    value = models.TextField(null=True)
    value_type = models.TextField(null=True)
    prerequisite_quantity = models.IntegerField(null=True)
    entitled_quantity = models.IntegerField(null=True)
    allocation_limit = models.IntegerField(null=True)
    last_sync_time = models.DateTimeField(default=timezone.now)


class Integrations_Shopify_Shop_Discount_Code(models.Model):
    objects = models.Manager()
    price_rule = models.ForeignKey(
        Integrations_Shopify_Shop_Price_Rule, on_delete=models.CASCADE, null=True)
    discount_id = models.TextField(max_length=32, null=False)
    code = models.TextField(max_length=140, null=True)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)
    usage_count = models.IntegerField()
    last_sync_time = models.DateTimeField(default=timezone.now, null=True)


class Integrations_Shopify_Money_Set(models.Model):
    objects = models.Manager()
    shop_money_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True)
    shop_money_currency_code = models.CharField(max_length=3, null=True)
    presentment_money_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True)
    presentment_money_currency_code = models.CharField(max_length=3, null=True)


class Integrations_Shopify_Address(models.Model):
    objects = models.Manager()
    address_id = TruncatingCharField(max_length=32, null=True)
    address1 = TruncatingCharField(max_length=255, null=True, default=None)
    address2 = TruncatingCharField(max_length=255, null=True, default=None)
    city = TruncatingCharField(max_length=255, null=True, default=None)
    company = TruncatingCharField(max_length=255, null=True, default=None)
    country = TruncatingCharField(max_length=255, null=True, default=None)
    country_code = TruncatingCharField(
        max_length=2, null=True, default=None)  # ISO 3166-1 code
    first_name = TruncatingCharField(max_length=255, null=True, default=None)
    last_name = TruncatingCharField(max_length=255, null=True, default=None)
    latitude = models.DecimalField(max_digits=10, decimal_places=4, null=True,)
    longitude = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    name = TruncatingCharField(max_length=255, null=True, default=None)
    phone = TruncatingCharField(max_length=32, null=True, default=None)
    province = TruncatingCharField(max_length=255, null=True, default=None)
    zip = TruncatingCharField(max_length=128, null=True, default=None)

    # NOTE the unique constraint had to be removed because it was too long, hence it is up to the programmer to be diligent with this.
    # DO NOT use .create, always use get_or_create()
    # class Meta:
    #     unique_together = (
    #         'address1', 'address2', 'city', 'company', 'country', 'country_code', 'first_name', 'last_name', 'name',
    #         'phone', 'province', 'zip')


# https://help.shopify.com/api/reference/customer
class Integrations_Shopify_Customer(models.Model):
    objects = models.Manager()
    user_iden = models.CharField(max_length=50, null=True)
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    shop = models.ForeignKey(
        Integrations_Shopify_Shop, on_delete=models.CASCADE, null=True
    )
    last_sync_time = models.DateTimeField(default=timezone.now, null=True)
    accepts_marketing = models.NullBooleanField()
    currency = models.CharField(max_length=3, default="USD")  # ISO 4217 code
    created_at = models.DateTimeField(null=True)
    default_address_1 = models.TextField(null=True)
    default_address_2 = models.TextField(null=True)
    default_address_city = models.TextField(null=True)
    default_address_company = models.TextField(null=True)
    default_address_first_name = models.TextField(null=True)
    default_address_last_name = models.TextField(null=True)
    default_address_phone = models.TextField(null=True)
    default_address_province = models.TextField(null=True)
    default_address_zip = models.TextField(null=True)
    default_address_name = models.TextField(null=True)
    default_address_province_code = models.TextField(null=True)
    default_address_country_code = models.TextField(null=True)
    default_address_latitude = models.TextField(null=True)
    default_address_longitude = models.TextField(null=True)
    email = TruncatingCharField(max_length=255, null=True)
    first_name = TruncatingCharField(max_length=255, null=True, blank=True)
    customer_id = TruncatingCharField(max_length=32, null=False)
    last_name = TruncatingCharField(max_length=255, null=True, blank=True)
    last_order_id = models.CharField(max_length=32, null=True)
    last_order_name = TruncatingCharField(
        max_length=255, null=True, blank=True)
    orders_count = models.IntegerField(null=True)
    phone = TruncatingCharField(max_length=32, null=True, blank=True)
    state = TruncatingCharField(
        max_length=255, null=True, blank=True)  # TODO add valid options
    tags = models.TextField(null=True)
    tax_exempt = models.NullBooleanField()
    total_spent = models.DecimalField(
        max_digits=10, decimal_places=2, null=True)
    updated_at = models.DateTimeField(null=True)

    class Meta:
        unique_together = ('integration', 'customer_id')


class Integrations_Shopify_Customer_Address(models.Model):
    objects = models.Manager()
    # null is true because records already exist
    customer_address_id = models.CharField(max_length=32, null=True)
    customer = models.ForeignKey(
        Integrations_Shopify_Customer, on_delete=models.CASCADE, null=False)
    address = models.ForeignKey(
        Integrations_Shopify_Address, on_delete=models.CASCADE, null=False)
    default = models.BooleanField(default=False)

    class Meta:
        unique_together = ('customer', 'customer_address_id')


# https://help.shopify.com/api/reference/product
class Integrations_Shopify_Product(models.Model):
    objects = models.Manager()
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    shop = models.ForeignKey(
        Integrations_Shopify_Shop, on_delete=models.CASCADE, null=True
    )
    user_iden = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(null=True)
    product_id = models.CharField(max_length=32, null=False, blank=False, default=131313131313,
                                  unique=True)  # TODO remove default
    product_type = TruncatingCharField(max_length=255, null=True, blank=True)
    published_at = models.DateTimeField(null=True)
    published_scope = TruncatingCharField(max_length=255, null=True)
    title = TruncatingCharField(max_length=255, null=True, blank=True)
    updated_at = models.DateTimeField(null=True)
    vendor = TruncatingCharField(max_length=255, null=True)
    last_sync_time = models.DateTimeField(null=True)


class Integrations_Shopify_Product_Tag(models.Model):
    objects = models.Manager()
    product = models.ForeignKey(
        Integrations_Shopify_Product, on_delete=models.CASCADE, null=False)
    tag = TruncatingCharField(max_length=255, null=False)


class Integrations_Shopify_Product_Option(models.Model):
    objects = models.Manager()
    option_id = models.CharField(max_length=32, null=False)
    product = models.ForeignKey(
        Integrations_Shopify_Product, on_delete=models.CASCADE, null=False)
    name = TruncatingCharField(max_length=255, null=True)
    position = models.PositiveSmallIntegerField(null=True)


class Integrations_Shopify_Product_Option_Value(models.Model):
    objects = models.Manager()
    option = models.ForeignKey(
        Integrations_Shopify_Product_Option, on_delete=models.CASCADE, null=False)
    value = TruncatingCharField(max_length=255, null=False)


class Integrations_Shopify_Product_Image(models.Model):
    objects = models.Manager()
    product = models.ForeignKey(Integrations_Shopify_Product,
                                null=False, on_delete=models.CASCADE, related_name="images")
    product_image_id = models.TextField(null=True)
    src = models.CharField(max_length=255, null=False)
    position = models.CharField(max_length=32, null=True)
    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)


class Integrations_Shopify_Product_Variant(models.Model):
    objects = models.Manager()
    barcode = models.CharField(max_length=255, null=True)
    compare_at_price = models.DecimalField(
        max_digits=12, decimal_places=2, null=True)
    created_at = models.DateTimeField(null=True)
    fulfillment_service = TruncatingCharField(max_length=255, null=True)
    grams = models.PositiveIntegerField(null=True)
    variant_id = models.CharField(max_length=64, null=False)
    inventory_item_id = models.CharField(max_length=64, null=True)
    inventory_management = TruncatingCharField(max_length=255, null=True)
    inventory_policy = TruncatingCharField(max_length=20, null=True)
    inventory_quantity = models.IntegerField(null=True)
    option1 = TruncatingCharField(max_length=255, null=True)
    option2 = TruncatingCharField(max_length=255, null=True)
    option3 = TruncatingCharField(max_length=255, null=True)
    position = models.PositiveIntegerField(null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    product = models.ForeignKey(
        Integrations_Shopify_Product, on_delete=models.CASCADE, null=False)
    sku = TruncatingCharField(max_length=75, null=True)
    taxable = models.BooleanField(default=False)
    tax_code = TruncatingCharField(max_length=255, null=True)
    title = TruncatingCharField(max_length=255, null=True)
    updated_at = models.DateTimeField(null=True)
    weight = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    weight_unit = TruncatingCharField(max_length=32, null=True)
    image = models.ForeignKey(
        Integrations_Shopify_Product_Image, on_delete=models.CASCADE, null=True)


class Integrations_Shopify_Variant_Presentment_Price(models.Model):
    objects = models.Manager()
    variant = models.ForeignKey(
        Integrations_Shopify_Product_Variant, on_delete=models.CASCADE, null=False)
    price_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0)
    price_currency_code = TruncatingCharField(max_length=3, default="USD")
    compare_at_price_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0)
    compare_at_price_currency_code = TruncatingCharField(
        max_length=3, default="USD")


# https://help.shopify.com/api/reference/order
class Integrations_Shopify_Order(models.Model):
    objects = models.Manager()
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    shop = models.ForeignKey(
        Integrations_Shopify_Shop, on_delete=models.CASCADE, null=True
    )
    billing_address_1 = models.TextField(null=True)
    billing_address_2 = models.TextField(null=True)
    billing_address_city = models.TextField(null=True)
    billing_address_company = models.TextField(null=True)
    billing_address_first_name = models.TextField(null=True)
    billing_address_last_name = models.TextField(null=True)
    billing_address_phone = models.TextField(null=True)
    billing_address_province = models.TextField(null=True)
    billing_address_zip = models.TextField(null=True)
    billing_address_name = models.TextField(null=True)
    billing_address_province_code = models.TextField(null=True)
    billing_address_country_code = models.TextField(null=True)
    billing_address_latitude = models.TextField(null=True)
    billing_address_longitude = models.TextField(null=True)
    shipping_address_1 = models.TextField(null=True)
    shipping_address_2 = models.TextField(null=True)
    shipping_address_city = models.TextField(null=True)
    shipping_address_company = models.TextField(null=True)
    shipping_address_first_name = models.TextField(null=True)
    shipping_address_last_name = models.TextField(null=True)
    shipping_address_phone = models.TextField(null=True)
    shipping_address_province = models.TextField(null=True)
    shipping_address_zip = models.TextField(null=True)
    shipping_address_name = models.TextField(null=True)
    shipping_address_province_code = models.TextField(null=True)
    shipping_address_country_code = models.TextField(null=True)
    shipping_address_latitude = models.TextField(null=True)
    shipping_address_longitude = models.TextField(null=True)
    browser_ip = models.GenericIPAddressField(null=True)
    buyer_accepts_marketing = models.BooleanField(default=False)
    cancel_reason = models.TextField(null=True)
    cancelled_at = models.DateTimeField(default=timezone.now, null=True)
    cart_token = TruncatingCharField(max_length=255, null=True)
    closed_at = models.DateTimeField(default=timezone.now, null=True)
    created_at = models.DateTimeField(null=True)
    currency = TruncatingCharField(max_length=4, null=True)
    customer_ref = models.ForeignKey(
        Integrations_Shopify_Customer, on_delete=models.SET_NULL, null=True, related_name="orders")
    customer_locale = TruncatingCharField(max_length=10, blank=True, null=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    financial_status = TruncatingCharField(
        max_length=20, null=True, blank=True)
    fulfillment_status = TruncatingCharField(max_length=20, null=True)
    # TODO Remove since this is deprecated?
    gateway = models.TextField(blank=True, null=True)
    order_id = models.CharField(max_length=64, null=False)
    landing_site = models.TextField(max_length=200, null=True)
    location_id = models.CharField(max_length=64, null=True)
    name = TruncatingCharField(max_length=20, null=True)
    order_number = models.BigIntegerField(null=True)
    phone = TruncatingCharField(max_length=32, null=True)
    presentment_currency = TruncatingCharField(max_length=3, null=True)
    processed_at = models.DateTimeField(null=True)
    processing_method = TruncatingCharField(
        max_length=1000, blank=True, null=True)
    referring_site = models.TextField(blank=True, null=True)
    ship_address = models.TextField(null=True)
    source_name = TruncatingCharField(max_length=128, null=True)
    subtotal_price = models.DecimalField(
        max_digits=12, decimal_places=2, null=True)
    subtotal_price_set = models.ForeignKey(Integrations_Shopify_Money_Set, on_delete=models.SET_NULL, null=True,
                                           related_name="orders_subtotal_price_set")
    tags = TruncatingCharField(max_length=100, null=True)
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    total_price_set = models.ForeignKey(Integrations_Shopify_Money_Set, on_delete=models.SET_NULL, null=True,
                                        related_name="orders_total_price_set")
    total_tax = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    total_tax_set = models.ForeignKey(Integrations_Shopify_Money_Set, on_delete=models.SET_NULL, null=True,
                                      related_name="orders_total_tax_set")
    total_discounts = models.DecimalField(
        max_digits=10, decimal_places=2, null=True)
    total_discounts_set = models.ForeignKey(Integrations_Shopify_Money_Set, on_delete=models.SET_NULL, null=True,
                                            related_name="orders_total_discounts_set")
    total_line_items_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    total_line_items_set = models.ForeignKey(Integrations_Shopify_Money_Set, on_delete=models.SET_NULL, null=True,
                                             related_name="orders_total_line_items_set")

    total_weight = models.DecimalField(
        max_digits=10, decimal_places=2, null=True)
    total_tip_received = models.DecimalField(
        max_digits=12, decimal_places=2, null=True)
    updated_at = models.DateTimeField(null=True)

    # TODO set up refunds
    user_iden = models.CharField(max_length=50, null=True, blank=True)
    last_sync_time = models.DateTimeField(default=timezone.now, null=True)

    class Meta:
        unique_together = ('integration', 'order_id')


class Integrations_Shopify_Tax_Line(models.Model):
    objects = models.Manager()
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    price_set = models.ForeignKey(
        Integrations_Shopify_Money_Set, on_delete=models.SET_NULL, null=True)
    rate = models.DecimalField(max_digits=3, decimal_places=2, null=True)
    title = TruncatingCharField(max_length=255, null=True)


class Integrations_Shopify_Shipping_Line(models.Model):
    objects = models.Manager()
    order = models.ForeignKey(
        Integrations_Shopify_Order, on_delete=models.CASCADE, null=False, related_name="lines")
    code = TruncatingCharField(max_length=255, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    price_set = models.ForeignKey(
        Integrations_Shopify_Money_Set, on_delete=models.CASCADE, null=True)
    discounted_price = models.DecimalField(
        max_digits=12, decimal_places=2, null=True)
    discounted_price_set = models.DecimalField(
        max_digits=12, decimal_places=2, null=True)
    source = TruncatingCharField(max_length=255, null=True)
    title = TruncatingCharField(max_length=255, null=True)


class Integrations_Shopify_Discount_Application(models.Model):
    objects = models.Manager()
    order = models.ForeignKey(
        Integrations_Shopify_Order, on_delete=models.CASCADE, null=False)
    allocation_method = TruncatingCharField(max_length=10, null=True)
    code = TruncatingCharField(max_length=100, null=True)
    description = TruncatingCharField(max_length=255, null=True)
    target_selection = TruncatingCharField(max_length=15, null=True)
    target_type = TruncatingCharField(max_length=20, null=True)
    title = TruncatingCharField(max_length=100, null=True)
    type = TruncatingCharField(max_length=20, null=True)
    value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    value_type = TruncatingCharField(max_length=20, null=True)


class Integrations_Shopify_Discount_Code(models.Model):
    objects = models.Manager()
    order = models.ForeignKey(
        Integrations_Shopify_Order, on_delete=models.CASCADE, null=False)
    code = TruncatingCharField(max_length=128, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    type = TruncatingCharField(max_length=20, null=True)


class Integrations_Shopify_Fulfillment(models.Model):
    objects = models.Manager()
    order = models.ForeignKey(
        Integrations_Shopify_Order, on_delete=models.CASCADE, null=False)
    created_at = models.DateTimeField(null=True)
    fulfillment_id = models.CharField(max_length=64, null=False)
    location_id = models.CharField(max_length=64, null=True)
    name = TruncatingCharField(max_length=20, null=True)
    status = TruncatingCharField(max_length=20, null=True)
    shipment_status = TruncatingCharField(max_length=30, null=True)
    service = TruncatingCharField(max_length=30, null=True)
    tracking_company = TruncatingCharField(max_length=255, null=True)
    tracking_number = TruncatingCharField(max_length=255, null=True)
    updated_at = models.DateTimeField(default=None, null=True, blank=True)
    receipt_testcase = models.BooleanField(default=False)
    receipt_authorization = TruncatingCharField(max_length=20, null=True)

    class Meta:
        unique_together = ('order', 'fulfillment_id')


class Integrations_Shopify_Line_Item(models.Model):
    objects = models.Manager()
    order = models.ForeignKey(
        Integrations_Shopify_Order, on_delete=models.CASCADE, null=False, related_name="line_items")
    fulfillment = models.ForeignKey(
        Integrations_Shopify_Fulfillment, on_delete=models.CASCADE, null=True)
    fulfillable_quantity = models.PositiveIntegerField(null=True)
    fulfillment_service = TruncatingCharField(max_length=255, null=True)
    fulfillment_status = TruncatingCharField(max_length=255, null=True)
    grams = models.PositiveIntegerField(null=True)
    line_item_id = models.CharField(max_length=64, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    product_id = models.CharField(max_length=64, null=True)
    product_ref = models.ForeignKey(
        Integrations_Shopify_Product, on_delete=models.SET_NULL, null=True, related_name="line_items")
    quantity = models.PositiveIntegerField(null=True)
    requires_shipping = models.NullBooleanField()
    sku = TruncatingCharField(max_length=255, null=True)  # stock-keeping-unit
    title = TruncatingCharField(max_length=255, null=True)
    variant_id = TruncatingCharField(max_length=32, null=True)
    variant_ref = models.ForeignKey(
        Integrations_Shopify_Product_Variant, on_delete=models.CASCADE, null=True)
    variant_title = TruncatingCharField(max_length=255, null=True)
    vendor = TruncatingCharField(max_length=255, null=True)
    name = TruncatingCharField(max_length=255, null=True)
    gift_card = models.NullBooleanField()
    price_set = models.ForeignKey(Integrations_Shopify_Money_Set, on_delete=models.SET_NULL, null=True,
                                  related_name='%(class)s_price_set_Line_Items')
    taxable = models.NullBooleanField()
    total_discount_set = models.ForeignKey(Integrations_Shopify_Money_Set, on_delete=models.SET_NULL, null=True,
                                           related_name='%(class)s_total_discount_set_Line_Items')

    class Meta:
        unique_together = ('order', 'line_item_id')


class Integrations_Shopify_Line_Item_Properties(models.Model):
    objects = models.Manager()
    line_item = models.ForeignKey(
        Integrations_Shopify_Line_Item, on_delete=models.CASCADE, null=False)
    name = TruncatingCharField(max_length=128, null=True)
    value = TruncatingCharField(max_length=255, null=True)


class Integrations_Shopify_Line_Item_Disc_Allocations(models.Model):
    class Meta:
        db_table = 'dashboards_integrations_shopify_line_item_disc_allocations'
       
    objects = models.Manager()
    line_item = models.ForeignKey(
        Integrations_Shopify_Line_Item, on_delete=models.CASCADE, null=False)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)
    discount_application_index = models.PositiveIntegerField(null=True)
    amount_set = models.ForeignKey(
        Integrations_Shopify_Money_Set, on_delete=models.SET_NULL, null=True)


# class Integrations_Shopify_Line_Item_Tax_Line(models.Model):
#     objects = models.Manager()
#     line_item = models.ForeignKey(Integrations_Shopify_Line_Item, on_delete=models.CASCADE, null=False)
#     title = models.CharField(max_length=100, null=True)
#     price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
#     price_set = models.ForeignKey(Integrations_Shopify_Money_Set, on_delete=models.SET_NULL, null=True)
#     rate = models.DecimalField(max_digits=6, decimal_places=2, null=True)


# Abandoned Checkouts /admin/checkouts.json
class Integrations_Shopify_Abandoned_Checkouts(models.Model):
    objects = models.Manager()
    checkout_id = models.CharField(max_length=50, blank=True, null=True)
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    shop = models.ForeignKey(
        Integrations_Shopify_Shop, on_delete=models.CASCADE, null=True
    )
    user_iden = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(null=True)
    closed_at = models.DateTimeField(null=True)
    completed_at = models.DateTimeField(null=True)
    landing_site = models.CharField(max_length=1024, blank=True, null=True)
    variant_id = models.CharField(max_length=50, blank=True, null=True)
    abandoned_checkout_url = models.TextField(blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    subtotal_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    total_line_items_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    shipping_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    total_tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cart_token = models.TextField(blank=True, null=True)
    vendor = models.TextField(blank=True, null=True)
    fulfillment_service = models.CharField(
        max_length=20, blank=True, null=True)
    buyer_accepts_marketing = models.BooleanField(default=True)
    taxable = models.BooleanField(default=True)
    gift_card = models.BooleanField(default=False)
    customer = models.TextField(blank=True, null=True)
    customer_ref = models.ForeignKey(
        Integrations_Shopify_Customer, on_delete=models.CASCADE, null=True)
    variant_inventory_management = models.CharField(
        max_length=20, blank=True, null=True)
    discount_codes = models.TextField(blank=True, null=True)
    product_exists = models.BooleanField(default=False)
    fulfillable_quantity = models.IntegerField(blank=True, null=True)
    total_discounts = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    gateway = models.CharField(max_length=50, blank=True, null=True)
    last_sync_time = models.DateTimeField(default=timezone.now, null=True)
    updated_at = models.DateTimeField(default=timezone.now, null=True)


class Integrations_Shopify_Abandoned_Checkout_Line_Items(models.Model):
    class Meta:
        db_table = 'dashboards_integrations_shopify_abndnd_chkout_line_items'
        
    objects = models.Manager()
    checkout = models.ForeignKey(Integrations_Shopify_Abandoned_Checkouts,
                                 on_delete=models.CASCADE, null=True, related_name="line_items")
    fulfillment_service = models.CharField(
        max_length=20, blank=True, null=True)
    grams = models.PositiveIntegerField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # remains as a fk contraint in the database
    product_id = models.CharField(max_length=50, blank=True, null=True)

    # product_id field in the table for shopify
    p_id = models.CharField(max_length=64, blank=True, null=True)
    product_ref = models.ForeignKey(
        Integrations_Shopify_Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    requires_shipping = models.BooleanField(default=True)
    sku = models.CharField(max_length=50, blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    # remains as fk constraint in database
    variant_id = models.CharField(max_length=50, blank=True, null=True)

    # variant_id field in the table for shopify
    v_id = models.CharField(max_length=64, blank=True, null=True)
    variant_ref = models.ForeignKey(
        Integrations_Shopify_Product_Variant, on_delete=models.CASCADE, null=True)

    variant_title = models.TextField(blank=True, null=True)
    vendor = models.TextField(blank=True, null=True)


class Integrations_Shopify_OrderItems(models.Model):  # TODO remove, not used
    objects = models.Manager()
    customer_id = models.CharField(
        max_length=20, null=False, blank=False, default=0, unique=False)
    order_id = models.CharField(max_length=50, blank=True, null=True)
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    user_iden = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    line_item_id = models.CharField(max_length=50, blank=True, null=True)
    variant_id = models.CharField(max_length=50, blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sku = models.CharField(max_length=50, blank=True, null=True)
    variant_title = models.TextField(blank=True, null=True)
    vendor = models.TextField(blank=True, null=True)
    fulfillment_service = models.CharField(
        max_length=20, blank=True, null=True)
    requires_shipping = models.BooleanField(default=True)
    taxable = models.BooleanField(default=True)
    gift_card = models.BooleanField(default=False)
    name = models.TextField(blank=True, null=True)
    variant_inventory_management = models.CharField(
        max_length=20, blank=True, null=True)
    properties = models.TextField(blank=True, null=True)
    product_exists = models.BooleanField(default=False)
    fulfillable_quantity = models.IntegerField(blank=True, null=True)
    total_discount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    fulfillment_status = models.CharField(max_length=50, blank=True, null=True)
    last_sync_time = models.DateTimeField(default=timezone.now, null=True)
    product_id = models.CharField(max_length=50, blank=True, null=True)


class Integrations_Shopify_Currency_Exchange_Adjustment(models.Model):
    objects = models.Manager()
    adjustment_id = models.CharField(max_length=32, null=False)
    adjustment = models.DecimalField(
        max_digits=12, decimal_places=2, null=True)
    original_amount = models.DecimalField(
        max_digits=12, decimal_places=2, null=True)
    final_amount = models.DecimalField(
        max_digits=12, decimal_places=2, null=True)
    currency = TruncatingCharField(max_length=3, null=True)


class Integrations_Shopify_Refund(models.Model):
    objects = models.Manager()
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(
        Integrations_Shopify_Order, on_delete=models.CASCADE, null=False, related_name="refunds")
    refund_id = models.CharField(max_length=64, blank=True, null=True)
    created_at = models.DateTimeField(null=True)
    processed_at = models.DateTimeField(null=True)
    note = TruncatingCharField(max_length=255, null=True)
    restock = models.NullBooleanField(null=True)
    user_id = models.CharField(max_length=32, null=True)  # user id in shopify

    class Meta:
        unique_together = ('refund_id', 'order')


class Integrations_Shopify_Transaction(models.Model):
    objects = models.Manager()
    order_ref = models.ForeignKey(
        Integrations_Shopify_Order, on_delete=models.CASCADE, null=False)
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    order_id = models.CharField(max_length=64, blank=True, null=True)
    refund_id = models.TextField(null=True)
    refund_ref = models.ForeignKey(
        Integrations_Shopify_Refund, on_delete=models.CASCADE, null=True)
    transaction_id = models.CharField(max_length=64, null=False)
    amount = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    authorization = TruncatingCharField(max_length=255, null=True)
    created_at = models.DateTimeField(null=True)
    currency = TruncatingCharField(max_length=3, default="USD")
    device_id = models.CharField(max_length=64, null=True)
    error_code = TruncatingCharField(max_length=64, null=True)
    gateway = TruncatingCharField(max_length=64, null=True)
    kind = TruncatingCharField(max_length=128, null=True)
    location_id = models.CharField(max_length=64, null=True)
    message = TruncatingCharField(max_length=255, null=True)
    receipt = TruncatingCharField(max_length=255, null=True)
    parent_id = models.CharField(max_length=64, null=True)
    processed_at = models.DateTimeField(null=True)
    source_name = TruncatingCharField(max_length=255, null=True)
    status = TruncatingCharField(max_length=16, null=True)
    test = models.BooleanField(default=False)
    user_id = models.CharField(max_length=32, null=True)
    last_sync_time = models.DateTimeField(default=timezone.now, null=True)

    class Meta:
        unique_together = ('transaction_id', 'order_ref')


class Integrations_Shopify_Refund_Order_Adjustment(models.Model):
    objects = models.Manager()
    order_adjustment_id = models.CharField(max_length=64, null=False)
    order_id = models.CharField(max_length=64, null=True)
    order_ref = models.ForeignKey(
        Integrations_Shopify_Order, on_delete=models.CASCADE, null=True)
    refund_id = models.CharField(max_length=64, null=True)
    refund_ref = models.ForeignKey(
        Integrations_Shopify_Refund, on_delete=models.CASCADE, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    tax_amount = models.DecimalField(
        max_digits=12, decimal_places=2, null=True)
    kind = TruncatingCharField(max_length=255, null=True)
    reason = TruncatingCharField(max_length=255, null=True)
    amount_set = models.ForeignKey(Integrations_Shopify_Money_Set, on_delete=models.SET_NULL, null=True,
                                   related_name="order_adjustment_amount_set")
    tax_amount_set = models.ForeignKey(Integrations_Shopify_Money_Set, on_delete=models.SET_NULL, null=True,
                                       related_name="order_adjustment_tax_amount_set")


class Integrations_Shopify_Refund_Line_Item(models.Model):
    objects = models.Manager()
    refund_line_item_id = models.CharField(max_length=64, null=False)
    refund = models.ForeignKey(
        Integrations_Shopify_Refund, on_delete=models.CASCADE, null=False, related_name="line_items")
    line_item_id = models.CharField(max_length=64, null=False)
    line_item_ref = models.ForeignKey(
        Integrations_Shopify_Line_Item, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(null=True)
    location_id = models.CharField(max_length=64, null=True)
    restock_type = TruncatingCharField(max_length=255, null=True)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    total_tax = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    subtotal_set = models.ForeignKey(Integrations_Shopify_Money_Set, on_delete=models.SET_NULL, null=True,
                                     related_name="refund_line_item_subtotal_set")
    total_tax_set = models.ForeignKey(Integrations_Shopify_Money_Set, on_delete=models.SET_NULL, null=True,
                                      related_name="refund_line_item_stotal_tax_set")

    class Meta:
        unique_together = ('refund_line_item_id', 'refund')


# Mailchimp models
# Campaigns
class Integrations_MailChimp_Campaigns(models.Model):
    # objects = Integrations_MailChimp_CampaignsManager()
    objects = models.Manager()

    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    user_iden = models.CharField(max_length=50, null=True, blank=True)
    from_name = models.CharField(max_length=50, blank=True, null=True)
    subject_line = models.CharField(max_length=200, blank=True, null=True)
    # A string that uniquely identifies this campaign.
    campaign_id = models.CharField(
        max_length=50, null=False, blank=False, default=131313131313, unique=True)
    # There are four types of campaigns you can create in MailChimp. A/B Split campaigns have been deprecated and variate campaigns should be used instead.
    type = models.CharField(max_length=50, null=True, blank=True)
    # The date and time the campaign was created.
    date_created = models.DateTimeField(default=timezone.now, null=True)
    # The link to the campaigns archive version.
    archive_url = models.TextField(null=True, blank=True)
    # The original link to the campaigns archive version.
    long_archive_url = models.TextField(null=True, blank=True)
    # The current status of the campaign.
    status = models.CharField(max_length=50, null=True, blank=True)
    # The total number of emails sent for this campaign.
    emails_sent = models.IntegerField(null=True, blank=True)
    # The date and time a campaign was sent.
    send_time = models.TextField(default=timezone.now)
    # How the campaigns content is put together ('template, 'drag_and_drop, 'html, 'url).
    content_type = models.CharField(max_length=50, null=True, blank=True)
    # List settings for the campaign.
    recipients = models.TextField(null=True, blank=True)
    # The settings for your campaign, including subject, from name, reply-to address, and more.
    settings = models.TextField(null=True, blank=True)
    # The tracking options for a campaign.
    tracking = models.TextField(null=True, blank=True)
    # For sent campaigns, a summary of opens, clicks, and e-commerce data.
    report_summary = models.TextField(null=True, blank=True)

    # API specific columns
    title = models.TextField(null=True, blank=True)
    preview_text = models.TextField(null=True, blank=True)
    # Updates on campaigns in the process of sending.
    delivery_status = models.TextField(null=True, blank=True)
    # Last DB-API sync datetime
    last_sync_time = models.DateTimeField(default=timezone.now, null=True)


##############################################################
# Campaign reports
##############################################################
class Integrations_MailChimp_CampaignReports(models.Model):
    # objects = Integrations_MailChimp_CampaignReportsManager()
    objects = models.Manager()
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    user_iden = models.CharField(max_length=50, null=True, blank=True)
    campaign_id = models.CharField(max_length=50, null=False, blank=False)
    campaign_ref = models.ForeignKey(Integrations_MailChimp_Campaigns, on_delete=models.CASCADE,
                                     null=True, blank=False, related_name='campaign_reports')
    create_time = models.DateTimeField(default=timezone.now, null=True)
    open_rate = models.FloatField(null=True, blank=True)
    click_rate = models.FloatField(null=True, blank=True)
    subscriber_clicks = models.IntegerField(null=True, blank=True)
    total_spent = models.FloatField(null=True, blank=True)
    total_revenue = models.FloatField(null=True, blank=True)
    total_orders = models.IntegerField(null=True, blank=True)
    clicks = models.IntegerField(null=True, blank=True)
    opens = models.IntegerField(null=True, blank=True)
    unique_opens = models.IntegerField(max_length=50, null=True, blank=True)
    last_sync_time = models.DateTimeField(default=timezone.now, null=True)


##############################################################
# Campaign BL Insights
##############################################################
class Integrations_MailChimp_Campaigns_Bl_Insights(models.Model):
    # objects = Integrations_MailChimp_CampaignReportsManager()
    objects = models.Manager()
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    user_iden = models.CharField(max_length=50, null=True, blank=True)
    campaign_id = models.CharField(max_length=50, null=False, blank=False)
    type = models.CharField(max_length=50, null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now, null=True)
    from_name = models.CharField(max_length=50, blank=True, null=True)
    subject_line = models.CharField(max_length=200, blank=True, null=True)
    archive_url = models.TextField(null=True, blank=True)
    long_archive_url = models.TextField(null=True, blank=True)
    create_time = models.DateTimeField(default=timezone.now, null=True)
    emails_sent = models.IntegerField(null=True, blank=True)
    send_time = models.TextField(default=timezone.now)
    status = models.CharField(max_length=50, null=True, blank=True)
    title = models.TextField(null=True, blank=True)
    preview_text = models.TextField(null=True, blank=True)
    #reports data#
    open_rate = models.FloatField(null=True, blank=True)
    click_rate = models.FloatField(null=True, blank=True)
    subscriber_clicks = models.IntegerField(null=True, blank=True)
    total_spent = models.FloatField(null=True, blank=True)
    total_revenue = models.FloatField(null=True, blank=True)
    total_orders = models.IntegerField(null=True, blank=True)
    clicks = models.IntegerField(null=True, blank=True)
    opens = models.IntegerField(null=True, blank=True)
    unique_opens = models.IntegerField(null=True, blank=True)
    last_sync_time = models.DateTimeField(default=timezone.now, null=True)
    campaign_aov = models.CharField(max_length=50, null=True, blank=True)
    campaign_creation_time = models.CharField(
        max_length=50, null=True, blank=True)


##############################################################
# Mailing lists
# https://developer.mailchimp.com/documentation/mailchimp/reference/lists/
# GET /lists/
##############################################################
class Integrations_MailChimp_Lists(models.Model):
    objects = models.Manager()
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    user_iden = models.CharField(max_length=50, null=True, blank=True)
    # A string that uniquely identifies this list.
    list_id = models.CharField(
        max_length=50, null=False, blank=False, default=131313131313, unique=True)
    # The ID used in the MailChimp web application. View this list in your MailChimp account at https://{dc}.admin.mailchimp.com/lists/members/?id={web_id}.
    web_id = models.CharField(
        max_length=50, null=False, blank=False, default=131313131313, unique=True)
    # The name of the list.
    name = models.TextField(null=False, blank=False)
    # Contact information displayed in campaign footers to comply with international spam laws.
    contact = models.TextField(null=True, blank=True)
    # The date and time that this list was created.
    date_created = models.DateTimeField(default=timezone.now, null=True)
    # An auto-generated activity score for the list (0-5).
    list_rating = models.CharField(
        max_length=50, null=False, blank=False, default=0)
    # Stats for the list. Many of these are cached for at least five minutes.
    stats = models.TextField(null=True, blank=True)
    # Last DB-API sync datetime
    last_sync_time = models.DateTimeField(default=timezone.now, null=True)


##############################################################
# List members
# Get information about a specific list member, including a currently subscribed, unsubscribed, or bounced member.
# GET /lists/{list_id}/members
##############################################################
class Integrations_MailChimp_ListMembers(models.Model):
    objects = models.Manager()
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    user_iden = models.CharField(max_length=50, null=True, blank=True)
    # The MD5 hash of the lowercase version of the list members email address.
    member_id = models.CharField(
        max_length=50, null=False, blank=False, default=131313131313, unique=False)
    # FK for lists
    member_ref = models.ForeignKey(
        Integrations_MailChimp_Lists, on_delete=models.CASCADE, null=True, blank=False)
    # Email address for a subscriber.
    email_address = models.EmailField(max_length=100, default='hi@example.com')
    # An identifier for the address across all of MailChimp.
    unique_email_id = models.CharField(max_length=50, null=True, blank=True)
    # Type of email this member asked to get ('html or 'text).
    email_type = models.CharField(max_length=50, null=True, blank=True)
    # Subscribers current status. Possible Values: subscribedunsubscribedcleanedpendingtransactiona
    status = models.CharField(max_length=50, null=True, blank=True)
    # Open and click rates for this subscriber.
    stats = models.TextField(null=True, blank=True)
    # IP address the subscriber signed up from.
    ip_signup = models.GenericIPAddressField(null=True)
    # The date and time the subscriber signed up for the list. "string" response
    timestamp_signup = models.TextField(null=True, blank=True)
    # Star rating for this member, between 1 and 5.
    member_rating = models.CharField(max_length=10, null=True, blank=True)
    # VIP status for subscriber.
    vip = models.BooleanField(default=False)
    # The list members email client.
    email_client = models.CharField(max_length=100, null=True, blank=True)
    # Subscriber location information.
    location = models.TextField(null=True, blank=True)
    # The list id
    list_id = models.CharField(max_length=50, null=True, blank=True)
    # Last DB-API sync datetime
    last_sync_time = models.DateTimeField(default=timezone.now, null=True)


##############################################################
# List stats
##############################################################
class Integrations_MailChimp_ListStats(models.Model):
    objects = models.Manager()
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    user_iden = models.CharField(max_length=50, null=True, blank=True)
    list_name = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.TextField(max_length=50, null=True, blank=True)
    stats_id = models.CharField(max_length=50, null=False, blank=False)
    stats_ref = models.ForeignKey(
        Integrations_MailChimp_Lists, on_delete=models.CASCADE, null=True, blank=False)
    avg_sub_rate = models.FloatField(null=True, blank=True)
    open_rate = models.FloatField(null=True, blank=True)
    member_count = models.FloatField(null=True, blank=True)
    click_rate = models.FloatField(null=True, blank=True)
    cleaned_count_since_send = models.IntegerField(null=True, blank=True)
    member_count_since_send = models.IntegerField(null=True, blank=True)
    target_sub_rate = models.FloatField(null=True, blank=True)
    last_sub_date = models.TextField(max_length=50, null=True, blank=True)
    merge_field_count = models.IntegerField(null=True, blank=True)
    avg_unsub_rate = models.FloatField(null=True, blank=True)
    unsubscribe_count = models.IntegerField(null=True, blank=True)
    cleaned_count = models.IntegerField(null=True, blank=True)
    unsubscribe_count_since_send = models.IntegerField(null=True, blank=True)
    campaign_count = models.IntegerField(null=True, blank=True)
    campaign_last_sent = models.TextField(max_length=50, null=True, blank=True)
    unsubscribe_count_since_send = models.IntegerField(null=True, blank=True)
    campaign_count = models.IntegerField(null=True, blank=True)
    last_unsub_date = models.TextField(max_length=50, null=True, blank=True)
    last_sync_time = models.DateTimeField(default=timezone.now, null=True)


#####################Instagram Models#################################
class Integrations_Instagram_Media_Objects(models.Model):
    objects = models.Manager()
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    integration_name = models.CharField(max_length=20, null=True, blank=True)
    last_sync_time = models.DateTimeField(default=timezone.now, null=True)
    user_iden = models.CharField(max_length=50, null=True, blank=True)
    media_id = models.TextField(null=True)
    media_type = models.TextField(null=True)
    media_url = models.TextField(null=True)
    owner_id = models.TextField(null=True)
    username = models.TextField(null=True)
    caption = models.TextField(null=True)
    comments_count = models.TextField(null=True)
    permalink = models.TextField(null=True)
    timestamp = models.DateTimeField(default=timezone.now, null=True)
    is_story = models.BooleanField(default=False)


class Integrations_Instagram_Media_Insights_Engagements(models.Model):
    objects = models.Manager()
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    media_object_ref = models.ForeignKey(
        Integrations_Instagram_Media_Objects, null=True, on_delete=models.CASCADE)
    integration_name = models.CharField(max_length=20, null=True, blank=True)
    last_sync_time = models.DateTimeField(default=timezone.now, null=True)
    user_iden = models.CharField(max_length=50, null=True, blank=True)
    record_id = models.CharField(max_length=500, null=True, blank=True)
    period = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    end_time = models.DateTimeField(default=timezone.now, null=True)
    value = models.CharField(max_length=200, null=True, blank=True)
    lookup = models.CharField(max_length=200, null=True, blank=True)
    all_data = models.TextField(max_length=200, null=True, blank=True)
    account_name = models.TextField(max_length=200, null=True, blank=True)


class Integrations_Instagram_Media_Insights_Impressions(models.Model):
    objects = models.Manager()
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    media_object_ref = models.ForeignKey(
        Integrations_Instagram_Media_Objects, null=True, on_delete=models.CASCADE)
    integration_name = models.CharField(max_length=20, null=True, blank=True)
    last_sync_time = models.DateTimeField(default=timezone.now, null=True)
    user_iden = models.CharField(max_length=50, null=True, blank=True)
    record_id = models.CharField(max_length=500, null=True, blank=True)
    period = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    end_time = models.DateTimeField(default=timezone.now, null=True)
    value = models.CharField(max_length=200, null=True, blank=True)
    lookup = models.CharField(max_length=200, null=True, blank=True)
    all_data = models.TextField(max_length=200, null=True, blank=True)
    account_name = models.TextField(max_length=200, null=True, blank=True)


class Integrations_Instagram_Media_Insights_Reach(models.Model):
    objects = models.Manager()
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    media_object_ref = models.ForeignKey(
        Integrations_Instagram_Media_Objects, null=True, on_delete=models.CASCADE)
    integration_name = models.CharField(max_length=20, null=True, blank=True)
    last_sync_time = models.DateTimeField(default=timezone.now, null=True)
    user_iden = models.CharField(max_length=50, null=True, blank=True)
    record_id = models.CharField(max_length=500, null=True, blank=True)
    period = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    end_time = models.DateTimeField(default=timezone.now, null=True)
    value = models.CharField(max_length=200, null=True, blank=True)
    lookup = models.CharField(max_length=200, null=True, blank=True)
    all_data = models.TextField(max_length=200, null=True, blank=True)
    account_name = models.TextField(max_length=200, null=True, blank=True)


class Integrations_Instagram_Media_Insights_Saved(models.Model):
    objects = models.Manager()
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    media_object_ref = models.ForeignKey(
        Integrations_Instagram_Media_Objects, null=True, on_delete=models.CASCADE)
    integration_name = models.CharField(max_length=20, null=True, blank=True)
    last_sync_time = models.DateTimeField(default=timezone.now, null=True)
    user_iden = models.CharField(max_length=50, null=True, blank=True)
    record_id = models.CharField(max_length=500, null=True, blank=True)
    period = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    end_time = models.DateTimeField(default=timezone.now, null=True)
    value = models.CharField(max_length=200, null=True, blank=True)
    lookup = models.CharField(max_length=200, null=True, blank=True)
    all_data = models.TextField(max_length=200, null=True, blank=True)
    account_name = models.TextField(max_length=200, null=True, blank=True)


class Integrations_Instagram_Media_Insights_Video_Views(models.Model):
    objects = models.Manager()
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    media_object_ref = models.ForeignKey(
        Integrations_Instagram_Media_Objects, null=True, on_delete=models.CASCADE)
    integration_name = models.CharField(max_length=20, null=True, blank=True)
    last_sync_time = models.DateTimeField(default=timezone.now, null=True)
    user_iden = models.CharField(max_length=50, null=True, blank=True)
    record_id = models.CharField(max_length=500, null=True, blank=True)
    period = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    end_time = models.DateTimeField(default=timezone.now, null=True)
    value = models.CharField(max_length=200, null=True, blank=True)
    lookup = models.CharField(max_length=200, null=True, blank=True)
    all_data = models.TextField(max_length=200, null=True, blank=True)
    account_name = models.TextField(max_length=200, null=True, blank=True)


class Integrations_Instagram_Media_Insights_Story_Exits(models.Model):
    objects = models.Manager()
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    media_object_ref = models.ForeignKey(
        Integrations_Instagram_Media_Objects, null=True, on_delete=models.CASCADE)
    integration_name = models.CharField(max_length=20, null=True, blank=True)
    last_sync_time = models.DateTimeField(default=timezone.now, null=True)
    user_iden = models.CharField(max_length=50, null=True, blank=True)
    record_id = models.CharField(max_length=500, null=True, blank=True)
    period = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    end_time = models.DateTimeField(default=timezone.now, null=True)
    value = models.CharField(max_length=200, null=True, blank=True)
    lookup = models.CharField(max_length=200, null=True, blank=True)
    all_data = models.TextField(max_length=200, null=True, blank=True)
    account_name = models.TextField(max_length=200, null=True, blank=True)


class Integrations_Instagram_Media_Insights_Story_Replies(models.Model):
    objects = models.Manager()
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    media_object_ref = models.ForeignKey(
        Integrations_Instagram_Media_Objects, null=True, on_delete=models.CASCADE)
    integration_name = models.CharField(max_length=20, null=True, blank=True)
    last_sync_time = models.DateTimeField(default=timezone.now, null=True)
    user_iden = models.CharField(max_length=50, null=True, blank=True)
    record_id = models.CharField(max_length=500, null=True, blank=True)
    period = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    end_time = models.DateTimeField(default=timezone.now, null=True)
    value = models.CharField(max_length=200, null=True, blank=True)
    lookup = models.CharField(max_length=200, null=True, blank=True)
    all_data = models.TextField(max_length=200, null=True, blank=True)
    account_name = models.TextField(max_length=200, null=True, blank=True)


class Integrations_Instagram_Media_Insights_Story_Taps_Fwd(models.Model):
    objects = models.Manager()
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    media_object_ref = models.ForeignKey(
        Integrations_Instagram_Media_Objects, null=True, on_delete=models.CASCADE)
    integration_name = models.CharField(max_length=20, null=True, blank=True)
    last_sync_time = models.DateTimeField(default=timezone.now, null=True)
    user_iden = models.CharField(max_length=50, null=True, blank=True)
    record_id = models.CharField(max_length=500, null=True, blank=True)
    period = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    end_time = models.DateTimeField(default=timezone.now, null=True)
    value = models.CharField(max_length=200, null=True, blank=True)
    lookup = models.CharField(max_length=200, null=True, blank=True)
    all_data = models.TextField(max_length=200, null=True, blank=True)
    account_name = models.TextField(max_length=200, null=True, blank=True)


class Integrations_Instagram_Media_Insights_Story_Taps_Back(models.Model):
    objects = models.Manager()
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    media_object_ref = models.ForeignKey(
        Integrations_Instagram_Media_Objects, null=True, on_delete=models.CASCADE)
    integration_name = models.CharField(max_length=20, null=True, blank=True)
    last_sync_time = models.DateTimeField(default=timezone.now, null=True)
    user_iden = models.CharField(max_length=50, null=True, blank=True)
    record_id = models.CharField(max_length=500, null=True, blank=True)
    period = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    end_time = models.DateTimeField(default=timezone.now, null=True)
    value = models.CharField(max_length=200, null=True, blank=True)
    lookup = models.CharField(max_length=200, null=True, blank=True)
    all_data = models.TextField(max_length=200, null=True, blank=True)
    account_name = models.TextField(max_length=200, null=True, blank=True)


class Integrations_InstagramInsights_Impressions(models.Model):
    objects = models.Manager()
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    integration_name = models.CharField(max_length=20, null=True, blank=True)
    last_sync_time = models.DateTimeField(default=timezone.now, null=True)
    user_iden = models.CharField(max_length=50, null=True, blank=True)
    record_id = models.CharField(max_length=500, null=True, blank=True)
    period = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    end_time = models.DateTimeField(default=timezone.now, null=True)
    value = models.CharField(max_length=200, null=True, blank=True)
    lookup = models.CharField(max_length=200, null=True, blank=True)
    all_data = models.TextField(max_length=200, null=True, blank=True)
    account_name = models.TextField(max_length=200, null=True, blank=True)


class Integrations_InstagramInsights_Reach(models.Model):
    objects = models.Manager()
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    integration_name = models.CharField(max_length=20, null=True, blank=True)
    last_sync_time = models.DateTimeField(default=timezone.now, null=True)
    user_iden = models.CharField(max_length=50, null=True, blank=True)
    record_id = models.CharField(max_length=500, null=True, blank=True)
    period = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    end_time = models.DateTimeField(default=timezone.now, null=True)
    value = models.CharField(max_length=200, null=True, blank=True)
    lookup = models.CharField(max_length=200, null=True, blank=True)
    all_data = models.TextField(max_length=200, null=True, blank=True)
    account_name = models.TextField(max_length=200, null=True, blank=True)


class Integrations_InstagramInsights_Followers(models.Model):
    objects = models.Manager()
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    integration_name = models.CharField(max_length=20, null=True, blank=True)
    last_sync_time = models.DateTimeField(default=timezone.now, null=True)
    user_iden = models.CharField(max_length=50, null=True, blank=True)
    record_id = models.CharField(max_length=500, null=True, blank=True)
    period = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    end_time = models.DateTimeField(default=timezone.now, null=True)
    value = models.CharField(max_length=200, null=True, blank=True)
    lookup = models.CharField(max_length=200, null=True, blank=True)
    all_data = models.TextField(max_length=200, null=True, blank=True)
    account_name = models.TextField(max_length=200, null=True, blank=True)


# class Integrations_InstagramInsights_Views(models.Model):
#     objects = models.Manager()
#     integration = models.ForeignKey(SocialAccount, on_delete=models.CASCADE, null=True)
#     integration_name = models.CharField(max_length=20, null=True, blank=True)
#     last_sync_time = models.DateTimeField(default=timezone.now, null=True)
#     user_iden = models.CharField(max_length=50, null=True, blank=True)
#     record_id = models.CharField(max_length=500, null=True, blank=True)
#     period = models.CharField(max_length=50, null=True, blank=True)
#     description = models.TextField(max_length=200, null=True, blank=True)
#     title = models.CharField(max_length=200, null=True, blank=True)
#     name = models.CharField(max_length=200, null=True, blank=True)
#     end_time = models.DateTimeField(default=timezone.now, null=True)
#     value = models.CharField(max_length=200, null=True, blank=True)
#     lookup = models.CharField(max_length=200, null=True, blank=True)
#     all_data = models.TextField(max_length=200, null=True, blank=True)
#     account_name = models.TextField(max_length=200, null=True, blank=True)


#####################Facebook Models#################################
class Integrations_Facebook_Page_Posts(models.Model):
    objects = models.Manager()
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    integration_name = models.CharField(max_length=20, null=True, blank=True)
    last_sync_time = models.DateTimeField(default=timezone.now, null=True)
    user_iden = models.CharField(max_length=50, null=True, blank=True)
    post_id = models.TextField(null=True)
    admin_creator = models.TextField(null=True)
    created_time = models.DateTimeField(default=timezone.now, null=True)
    _from = models.TextField(null=True)
    full_picture = models.TextField(null=True)
    icon = models.TextField(null=True)
    is_expired = models.BooleanField(null=True)
    is_instagram_eligible = models.BooleanField(null=True)
    is_popular = models.BooleanField(null=True)
    is_published = models.BooleanField(null=True)
    message = models.TextField(null=True)
    parent_id = models.TextField(null=True)
    permalink = models.TextField(null=True)
    promotion_status = models.TextField(null=True)
    scheduled_publish_time = models.DateTimeField(null=True)
    shares = models.TextField(null=True)
    status_type = models.TextField(null=True)
    timeline_visibility = models.TextField(null=True)
    updated_time = models.DateTimeField(null=True)


class Integrations_Facebook_Page_Post_Impressions(models.Model):
    objects = models.Manager()
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    post_ref = models.ForeignKey(
        Integrations_Facebook_Page_Posts, null=True, on_delete=models.CASCADE)
    integration_name = models.CharField(max_length=20, null=True, blank=True)
    last_sync_time = models.DateTimeField(default=timezone.now, null=True)
    user_iden = models.CharField(max_length=50, null=True, blank=True)
    record_id = models.CharField(max_length=500, null=True, blank=True)
    period = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    end_time = models.DateTimeField(default=timezone.now, null=True)
    value = models.CharField(max_length=200, null=True, blank=True)
    lookup = models.CharField(max_length=200, null=True, blank=True)
    all_data = models.TextField(max_length=200, null=True, blank=True)
    account_name = models.TextField(max_length=200, null=True, blank=True)


class Integrations_Facebook_Page_Post_Engagements(models.Model):
    objects = models.Manager()
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    post_ref = models.ForeignKey(
        Integrations_Facebook_Page_Posts, null=True, on_delete=models.CASCADE)
    integration_name = models.CharField(max_length=20, null=True, blank=True)
    last_sync_time = models.DateTimeField(default=timezone.now, null=True)
    user_iden = models.CharField(max_length=50, null=True, blank=True)
    record_id = models.CharField(max_length=500, null=True, blank=True)
    period = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    end_time = models.DateTimeField(default=timezone.now, null=True)
    value = models.CharField(max_length=200, null=True, blank=True)
    lookup = models.CharField(max_length=200, null=True, blank=True)
    all_data = models.TextField(max_length=200, null=True, blank=True)
    account_name = models.TextField(max_length=200, null=True, blank=True)


class Integrations_Facebook_Page_Post_Reactions(models.Model):
    objects = models.Manager()
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    post_ref = models.ForeignKey(
        Integrations_Facebook_Page_Posts, null=True, on_delete=models.CASCADE)
    integration_name = models.CharField(max_length=20, null=True, blank=True)
    last_sync_time = models.DateTimeField(default=timezone.now, null=True)
    user_iden = models.CharField(max_length=50, null=True, blank=True)
    record_id = models.CharField(max_length=500, null=True, blank=True)
    period = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    end_time = models.DateTimeField(default=timezone.now, null=True)
    value = models.CharField(max_length=200, null=True, blank=True)
    lookup = models.CharField(max_length=200, null=True, blank=True)
    all_data = models.TextField(max_length=200, null=True, blank=True)
    account_name = models.TextField(max_length=200, null=True, blank=True)


class Integrations_FacebookInsights_Impressions(models.Model):
    objects = models.Manager()
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    integration_name = models.CharField(max_length=20, null=True, blank=True)
    last_sync_time = models.DateTimeField(default=timezone.now, null=True)
    user_iden = models.CharField(max_length=50, null=True, blank=True)
    record_id = models.CharField(max_length=1000, null=True, blank=True)
    period = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    end_time = models.DateTimeField(default=timezone.now, null=True)
    value = models.CharField(max_length=200, null=True, blank=True)
    lookup = models.CharField(max_length=200, null=True, blank=True)
    all_data = models.TextField(max_length=200, null=True, blank=True)
    account_name = models.TextField(max_length=200, null=True, blank=True)


class Integrations_FacebookInsights_Views(models.Model):
    objects = models.Manager()
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    integration_name = models.CharField(max_length=20, null=True, blank=True)
    last_sync_time = models.DateTimeField(default=timezone.now, null=True)
    user_iden = models.CharField(max_length=50, null=True, blank=True)
    record_id = models.CharField(max_length=1000, null=True, blank=True)
    period = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    end_time = models.DateTimeField(default=timezone.now, null=True)
    value = models.CharField(max_length=200, null=True, blank=True)
    lookup = models.CharField(max_length=200, null=True, blank=True)
    all_data = models.TextField(max_length=200, null=True, blank=True)
    account_name = models.TextField(max_length=200, null=True, blank=True)


class Integrations_FacebookInsights_Engagements(models.Model):
    objects = models.Manager()
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    integration_name = models.CharField(max_length=20, null=True, blank=True)
    last_sync_time = models.DateTimeField(default=timezone.now, null=True)
    user_iden = models.CharField(max_length=50, null=True, blank=True)
    record_id = models.CharField(max_length=1000, null=True, blank=True)
    period = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    end_time = models.DateTimeField(default=timezone.now, null=True)
    value = models.CharField(max_length=200, null=True, blank=True)
    lookup = models.CharField(max_length=200, null=True, blank=True)
    all_data = models.TextField(max_length=200, null=True, blank=True)
    account_name = models.TextField(max_length=200, null=True, blank=True)


class Integrations_FacebookInsights_Reactions(models.Model):
    objects = models.Manager()
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    integration_name = models.CharField(max_length=20, null=True, blank=True)
    last_sync_time = models.DateTimeField(default=timezone.now, null=True)
    user_iden = models.CharField(max_length=50, null=True, blank=True)
    record_id = models.CharField(max_length=1000, null=True, blank=True)
    period = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    end_time = models.DateTimeField(default=timezone.now, null=True)
    value = models.CharField(max_length=200, null=True, blank=True)
    lookup = models.CharField(max_length=200, null=True, blank=True)
    all_data = models.TextField(max_length=200, null=True, blank=True)
    account_name = models.TextField(max_length=200, null=True, blank=True)


class Integrations_FacebookInsights_Posts(models.Model):
    objects = models.Manager()
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    integration_name = models.CharField(max_length=20, null=True, blank=True)
    last_sync_time = models.DateTimeField(default=timezone.now, null=True)
    user_iden = models.CharField(max_length=50, null=True, blank=True)
    record_id = models.CharField(max_length=1000, null=True, blank=True)
    period = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    end_time = models.DateTimeField(default=timezone.now, null=True)
    value = models.CharField(max_length=200, null=True, blank=True)
    lookup = models.CharField(max_length=200, null=True, blank=True)
    all_data = models.TextField(max_length=200, null=True, blank=True)
    account_name = models.TextField(max_length=200, null=True, blank=True)


class Integrations_FacebookInsights_Demographics(models.Model):
    objects = models.Manager()
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    integration_name = models.CharField(max_length=20, null=True, blank=True)
    last_sync_time = models.DateTimeField(default=timezone.now, null=True)
    user_iden = models.CharField(max_length=50, null=True, blank=True)
    record_id = models.CharField(max_length=1000, null=True, blank=True)
    period = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    end_time = models.DateTimeField(default=timezone.now, null=True)
    value = models.CharField(max_length=200, null=True, blank=True)
    lookup = models.CharField(max_length=200, null=True, blank=True)
    account_name = models.TextField(max_length=200, null=True, blank=True)
    all_data = models.TextField(max_length=200, null=True, blank=True)

    ##### ETSY MODELS ###################################################


class Integrations_Etsy_User(models.Model):
    objects = models.Manager()
    integration = models.ForeignKey(SocialAccount, on_delete=models.CASCADE, null=True)
    user_iden = models.TextField(null=True)
    avatar_id = models.IntegerField(null=True)
    avatar_src_url = models.TextField(null=True)
    user_profile_id = models.IntegerField(null=True)
    login_name = models.TextField(null=True)
    bio = models.TextField(null=True)
    gender = models.TextField(null=True)
    birth_month = models.IntegerField(null=True)
    birth_day = models.IntegerField(null=True)
    birth_year = models.IntegerField(null=True)
    join_tsz = models.DateTimeField(null=True)
    country_id = models.IntegerField(null=True)
    region = models.TextField(null=True)
    city = models.TextField(null=True)
    location = models.TextField(null=True)
    lat = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    lon = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    transaction_buy_count = models.IntegerField(null=True)
    transaction_sold_count = models.IntegerField(null=True)
    is_seller = models.NullBooleanField(null=True)
    image_url_75x75 = models.TextField(null=True)
    first_name = models.TextField(null=True)
    last_name = models.TextField(null=True)


class Integrations_Etsy_UserAddress(models.Model):
    objects = models.Manager()
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    user_iden = models.IntegerField(null=True)
    user_ref = models.ForeignKey(Integrations_Etsy_User, on_delete=models.CASCADE, null=True)
    user_id = models.TextField(null=True)
    user_address_id = models.TextField(null=True)
    last_sync_time = models.DateTimeField(default=timezone.now, null=True)
    address_name = models.TextField(null=True)
    first_line = models.TextField(null=True)
    second_line = models.TextField(null=True)
    city = models.TextField(null=True)
    state = models.TextField(null=True)
    zip = models.TextField(null=True)
    country_id = models.IntegerField(null=True)
    country_name = models.TextField(null=True)
    is_default_shipping = models.NullBooleanField(null=True)


class Integrations_Etsy_Shop(models.Model):
    objects = models.Manager()
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    user_iden = models.IntegerField(null=True)
    user_ref = models.ForeignKey(Integrations_Etsy_User, on_delete=models.CASCADE, null=True)
    user_id = models.TextField(null=True)
    last_sync_time = models.DateTimeField(default=timezone.now, null=True)
    shop_id = models.IntegerField(max_length=50, null=True, blank=True)
    shop_name = models.TextField(null=True)
    first_line = models.TextField(null=True)
    second_line = models.TextField(null=True)
    city = models.TextField(null=True)
    state = models.TextField(null=True)
    zip = models.TextField(null=True)
    country_id = models.IntegerField(null=True)
    creation_tsz = models.DateTimeField(null=True)
    title = models.TextField(null=True)
    announcement = models.TextField(null=True)
    currency_code = models.TextField(null=True)
    is_vacation = models.NullBooleanField(null=True)
    vacation_message = models.TextField(null=True)
    sale_message = models.TextField(null=True)
    digital_sale_message = models.TextField(null=True)
    last_updated_tsz = models.DateTimeField(null=True)
    listing_active_count = models.IntegerField(null=True)
    digital_listing_count = models.IntegerField(null=True)
    login_name = models.TextField(null=True)
    lat = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    lon = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    accepts_custom_requests = models.NullBooleanField(null=True)
    policy_welcome = models.TextField(null=True)
    policy_payment = models.TextField(null=True)
    policy_shipping = models.TextField(null=True)
    policy_refunds = models.TextField(null=True)
    policy_additional = models.TextField(null=True)
    policy_seller_info = models.TextField(null=True)
    policy_updated_tsz = models.DateTimeField(null=True)
    policy_has_private_receipt_info = models.NullBooleanField(null=True)
    vacation_autoreply = models.TextField(null=True)
    ga_code = models.TextField(null=True)
    name = models.TextField(null=True)
    url = models.TextField(null=True)
    image_url_760x100 = models.TextField(null=True)
    num_favorers = models.IntegerField(null=True)
    upcoming_local_event_id = models.IntegerField(null=True)
    icon_url_fullxfull = models.TextField(null=True)
    is_using_structured_policies = models.NullBooleanField(null=True)
    has_onboarded_structured_policies = models.NullBooleanField(null=True)
    has_unstructured_policies = models.NullBooleanField(null=True)
    policy_privacy = models.TextField(null=True)
    use_new_inventory_endpoints = models.NullBooleanField(null=True)
    include_dispute_form_link = models.NullBooleanField(null=True)


class Integrations_Etsy_Shop_Language(models.Model):
    objects = models.Manager()
    shop_ref = models.ForeignKey(
        Integrations_Etsy_Shop, on_delete=models.CASCADE, null=False)
    language = TruncatingCharField(max_length=255, null=False)


class Integrations_Etsy_Listing(models.Model):
    objects = models.Manager()
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    shop_ref = models.ForeignKey(Integrations_Etsy_Shop, on_delete=models.CASCADE, null=True)
    shop_id = models.TextField(null=True)
    last_sync_time = models.DateTimeField(default=timezone.now, null=True)
    user_iden = models.TextField(null=True)
    listing_id = models.TextField(null=True)
    state = models.TextField(null=True)
    user_id = models.TextField(null=True)
    category_id = models.TextField(null=True)
    title = models.TextField(null=True)
    description = models.TextField(null=True)
    creation_tsz = models.DateTimeField(null = True)
    ending_tsz = models.DateTimeField(null = True)
    original_creation_tsz = models.DateTimeField(null = True)
    last_modified_tsz = models.DateTimeField(null = True)
    price = models.TextField(null=True)
    currency_code = models.TextField(null=True)
    quantity = models.TextField(null=True)
    taxonomy_path = models.TextField(null=True)
    taxonomy_id = models.TextField(null=True)
    suggested_taxonomy_id = models.TextField(null=True)
    shop_section_id = models.TextField(null=True)
    featured_rank = models.TextField(null=True)
    state_tsz = models.TextField(null=True)
    views = models.TextField(null=True)
    num_favorers = models.TextField(null=True)
    shipping_template_id = models.TextField(null=True)
    processing_min = models.TextField(null=True)
    processing_max = models.TextField(null=True)
    who_made = models.TextField(null=True)
    is_supply = models.NullBooleanField(null=True)
    when_made = models.TextField(null=True)
    item_weight = models.TextField(null=True)
    item_weight_unit = models.TextField(null=True)
    item_length = models.TextField(null=True)
    item_width = models.TextField(null=True)
    item_height = models.TextField(null=True)
    item_dimensions_unit = models.TextField(null=True)
    is_private = models.NullBooleanField(null=True)
    recipient = models.TextField(null=True)
    occasion = models.TextField(null=True)
    style = models.TextField(null=True)
    non_taxable = models.NullBooleanField(null=True)
    is_customizable = models.NullBooleanField(null=True)
    is_digital = models.NullBooleanField(null=True)
    file_data = models.TextField(null=True)
    can_write_inventory = models.NullBooleanField(null=True)
    has_variations = models.NullBooleanField(null=True)
    should_auto_renew = models.NullBooleanField(null=True)
    language = models.TextField(null=True)


class Integrations_Etsy_Listing_Sku(models.Model):
    objects = models.Manager()
    listing_ref = models.ForeignKey(
        Integrations_Etsy_Listing, on_delete=models.CASCADE, null=False)
    sku = TruncatingCharField(max_length=255, null=False)


class Integrations_Etsy_Listing_Tag(models.Model):
    objects = models.Manager()
    listing_ref = models.ForeignKey(
        Integrations_Etsy_Listing, on_delete=models.CASCADE, null=False)
    tag = TruncatingCharField(max_length=255, null=False)


class Integrations_Etsy_Listing_Material(models.Model):
    objects = models.Manager()
    listing_ref = models.ForeignKey(
        Integrations_Etsy_Listing, on_delete=models.CASCADE, null=False)
    material = TruncatingCharField(max_length=255, null=False)


class Integrations_Etsy_Listing_Image(models.Model):
    objects = models.Manager()
    listing_ref = models.ForeignKey(
        Integrations_Etsy_Listing, on_delete=models.CASCADE, null=False)
    listing_image_id = models.TextField(null=True)
    listing_id = models.TextField(null=True)
    hex_code = models.TextField(null=True)
    red = models.TextField(null=True)
    green = models.TextField(null=True)
    blue = models.TextField(null=True)
    hue = models.TextField(null=True)
    saturation = models.TextField(null=True)
    brightness = models.TextField(null=True)
    is_black_and_white = models.TextField(null=True)
    creation_tsz = models.TextField(null=True)
    rank = models.TextField(null=True)
    url_75x75 = models.TextField(null=True)
    url_170x135 = models.TextField(null=True)
    url_570xN = models.TextField(null=True)
    url_fullxfull = models.TextField(null=True)
    full_height = models.TextField(null=True)
    full_width = models.TextField(null=True)


class Integrations_Etsy_Listing_Product(models.Model):
    objects = models.Manager()
    listing_ref = models.ForeignKey(
        Integrations_Etsy_Listing, on_delete=models.CASCADE, null=False)
    product_id = models.TextField(null=True)
    listing_id = models.CharField(max_length=50, null=True, blank=True)
    is_deleted = models.NullBooleanField(null=True)
    sku = models.TextField(null=True)


class Integrations_Etsy_Listing_Product_Offering(models.Model):
    objects = models.Manager()
    product_ref = models.ForeignKey(
        Integrations_Etsy_Listing_Product, on_delete=models.CASCADE, null=False)
    offering_id = models.TextField(null=True)
    product_id = models.TextField(null=True)
    price = models.TextField(null=True)
    quantity = models.TextField(null=True)
    is_enabled = models.NullBooleanField(null=True)
    is_deleted = models.NullBooleanField(null=True)


class Integrations_Etsy_Listing_Product_Property(models.Model):
    objects = models.Manager()
    product_ref = models.ForeignKey(
        Integrations_Etsy_Listing_Product, on_delete=models.CASCADE, null=False)
    property_id = models.TextField(null=True)
    product_id = models.TextField(null=True)
    property_name = models.TextField(null=True)
    scale_id = models.TextField(null=True)
    scale_name = models.TextField(null=True)


class Integrations_Etsy_Listing_Product_Property_Value(models.Model):
    objects = models.Manager()
    property_ref = models.ForeignKey(
        Integrations_Etsy_Listing_Product_Property, on_delete=models.CASCADE, null=True)
    property_id = models.TextField(null=True)
    product_id = models.TextField(null=True)
    value_id = models.TextField(null=True)
    value_name = models.TextField(null=True)


class Integrations_Etsy_Listing_Image_Variation(models.Model):
    objects = models.Manager()
    listing_ref = models.ForeignKey(
        Integrations_Etsy_Listing, on_delete=models.CASCADE, null=True)
    image_ref = models.ForeignKey(
        Integrations_Etsy_Listing_Image, on_delete=models.CASCADE, null=True)
    listing_id = models.CharField(max_length=50, null=True, blank=True)
    property_id = models.CharField(max_length=50, null=True, blank=True)
    image_id = models.CharField(max_length=50, null=True, blank=True)
    value_id = models.CharField(max_length=50, null=True, blank=True)


class Integrations_Etsy_Receipt(models.Model):
    objects = models.Manager()
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    shop_ref = models.ForeignKey(
        Integrations_Etsy_Shop, on_delete=models.CASCADE, null=True)
    shop_id = models.TextField(null=True)
    last_sync_time = models.DateTimeField(default=timezone.now, null=True)
    user_iden = models.TextField(null=True)
    receipt_id = models.TextField(null=True)
    receipt_type = models.IntegerField(null=True)
    order_id = models.TextField(null=True)
    seller_user_id = models.TextField(null=True)
    buyer_user_id = models.TextField(null=True)
    creation_tsz = models.DateTimeField(null=True)
    can_refund = models.NullBooleanField(null=True)
    last_modified_tsz = models.DateTimeField(null=True)
    name = models.TextField(null=True)
    first_line = models.TextField(null=True)
    second_line = models.TextField(null=True)
    city = models.TextField(null=True)
    state = models.TextField(null=True)
    zip = models.TextField(null=True)
    formatted_address = models.TextField(null=True)
    country_id = models.TextField(null=True)
    payment_method = models.TextField(null=True)
    payment_email = models.TextField(null=True)
    message_from_seller = models.TextField(null=True)
    message_from_buyer = models.TextField(null=True)
    was_paid = models.NullBooleanField(null=True)
    total_tax_cost = models.TextField(null=True)
    total_vat_cost = models.TextField(null=True)
    total_price = models.TextField(null=True)
    total_shipping_cost = models.TextField(null=True)
    currency_code = models.TextField(null=True)
    message_from_payment = models.TextField(null=True)
    was_shipped = models.NullBooleanField(null=True)
    buyer_email = models.TextField(null=True)
    seller_email = models.TextField(null=True)
    is_gift = models.NullBooleanField(null=True)
    needs_gift_wrap = models.NullBooleanField(null=True)
    gift_message = models.TextField(null=True)
    gift_wrap_price = models.TextField(null=True)
    discount_amt = models.TextField(null=True)
    subtotal = models.TextField(null=True)
    grandtotal = models.TextField(null=True)
    adjusted_grandtotal = models.TextField(null=True)
    buyer_adjusted_grandtotal = models.TextField(null=True)


class Integrations_Etsy_Receipt_Shipment(models.Model):
    objects = models.Manager()
    receipt_ref = models.ForeignKey(
        Integrations_Etsy_Receipt, on_delete=models.CASCADE, null=False)
    carrier_name = models.TextField(null=True)
    receipt_shipping_id = models.TextField(null=True)
    tracking_code = models.TextField(null=True)
    tracking_url = models.TextField(null=True)
    buyer_note = models.TextField(null=True)
    notification_date = models.TextField(null=True)
    receipt_id = models.TextField(null=True)


class Integrations_Etsy_Receipt_Payment(models.Model):
    objects = models.Manager()
    receipt_ref = models.ForeignKey(
        Integrations_Etsy_Receipt, on_delete=models.CASCADE, null=True)
    shop_ref = models.ForeignKey(
        Integrations_Etsy_Shop, on_delete=models.CASCADE, null=True)
    receipt_id = models.TextField(null=True)
    user_iden = models.CharField(max_length=50, null=True, blank=True)
    payment_id = models.TextField(null=True)
    buyer_user_id = models.TextField(null=True)
    shop_id = models.TextField(null=True)
    amount_gross = models.TextField(null=True)
    amount_fees = models.TextField(null=True)
    amount_net = models.TextField(null=True)
    posted_gross = models.TextField(null=True)
    posted_fees = models.TextField(null=True)
    posted_net = models.TextField(null=True)
    adjusted_gross = models.TextField(null=True)
    adjusted_fees = models.TextField(null=True)
    adjusted_net = models.TextField(null=True)
    currency = models.TextField(null=True)
    shop_currency = models.TextField(null=True)
    buyer_currency = models.TextField(null=True)
    shipping_user_id = models.TextField(null=True)
    shipping_address_id = models.TextField(null=True)
    billing_address_id = models.TextField(null=True)
    status = models.TextField(null=True)
    shipped_date = models.DateTimeField(null=True)
    create_date = models.DateTimeField(null=True)
    update_date = models.DateTimeField(null=True)


class Integrations_Etsy_Receipt_Payment_Adjustment(models.Model):
    objects = models.Manager()
    payment_ref = models.ForeignKey(
        Integrations_Etsy_Receipt_Payment, on_delete=models.CASCADE, null=True)
    payment_id = models.TextField(null=True)
    user_iden = models.CharField(max_length=50, null=True, blank=True)
    payment_adjustment_id = models.TextField(null=True)
    status = models.TextField(null=True)
    is_success = models.NullBooleanField(null=True)
    user_id = models.TextField(null=True)
    reason_code = models.TextField(null=True)
    total_adjustment_amount = models.TextField(null=True)
    shop_total_adjustment_amount = models.TextField(null=True)
    buyer_total_adjustment_amount = models.TextField(null=True)
    total_fee_adjustment_amount = models.TextField(null=True)
    create_date = models.DateTimeField(null=True)
    update_date = models.DateTimeField(null=True)


class Integrations_Etsy_Receipt_Payment_Adjustment_Item(models.Model):
    objects = models.Manager()
    adjustment_ref = models.ForeignKey(
        Integrations_Etsy_Receipt_Payment_Adjustment, on_delete=models.CASCADE, null=True)
    payment_adjustment_id = models.TextField(null=True)
    user_iden = models.CharField(max_length=50, null=True, blank=True)
    payment_adjustment_item_id = models.TextField(null=True)
    adjustment_type = models.TextField(null=True)
    amount = models.TextField(null=True)
    transaction_id = models.TextField(null=True)
    create_date = models.DateTimeField(null=True)


class Integrations_Etsy_Transaction(models.Model):
    objects = models.Manager()
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    shop_ref = models.ForeignKey(
        Integrations_Etsy_Shop, on_delete=models.CASCADE, null=True)
    shop_id = models.TextField(null=True)
    last_sync_time = models.DateTimeField(default=timezone.now, null=True)
    user_iden = models.CharField(max_length=50, null=True, blank=True)
    transaction_id = models.TextField(null=True)
    title = models.TextField(null=True)
    description = models.TextField(null=True)
    seller_user_id = models.TextField(null=True)
    buyer_user_id = models.TextField(null=True)
    creation_tsz = models.DateTimeField(null=True)
    paid_tsz = models.DateTimeField(null=True)
    shipped_tsz = models.DateTimeField(null=True)
    price = models.TextField(null=True)
    currency_code = models.TextField(null=True)
    quantity = models.TextField(null=True)
    image_listing_id = models.TextField(null=True)
    receipt_id = models.TextField(null=True)
    shipping_cost = models.TextField(null=True)
    is_digital = models.NullBooleanField(null=True)
    file_data = models.TextField(null=True)
    listing_id = models.TextField(null=True)
    is_quick_sale = models.NullBooleanField(null=True)
    seller_feedback_id = models.TextField(null=True)
    buyer_feedback_id = models.TextField(null=True)
    transaction_type = models.TextField(null=True)
    url = models.TextField(null=True)


class Integrations_Etsy_Transaction_BuyerFeedback(models.Model):
    objects = models.Manager()
    transaction_ref = models.ForeignKey(
        Integrations_Etsy_Transaction, on_delete=models.CASCADE, null=True)
    transaction_id = models.TextField(null=True)
    user_iden = models.CharField(max_length=50, null=True, blank=True)
    feedback_id = models.TextField(null=True)
    creator_user_id = models.TextField(null=True)
    target_user_id = models.TextField(null=True)
    seller_user_id = models.TextField(null=True)
    buyer_user_id = models.TextField(null=True)
    creation_tsz = models.DateTimeField(null=True)
    message = models.TextField(null=True)
    value = models.TextField(null=True)
    image_feedback_id = models.TextField(null=True)
    image_url_25x25 = models.TextField(null=True)
    image_url_155x125 = models.TextField(null=True)
    image_url_fullxfull = models.TextField(null=True)


class Integrations_Etsy_Ledger(models.Model):
    objects = models.Manager()
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    shop_ref = models.ForeignKey(
        Integrations_Etsy_Shop, on_delete=models.CASCADE, null=True)
    shop_id = models.TextField(null=True)
    last_sync_time = models.DateTimeField(default=timezone.now, null=True)
    user_iden = models.CharField(max_length=50, null=True, blank=True)
    ledger_id = models.TextField(null=True)
    currency = models.TextField(null=True)
    create_date = models.DateTimeField(null=True)
    update_date = models.DateTimeField(null=True)


class Integrations_Etsy_Ledger_Entry(models.Model):
    objects = models.Manager()
    ledger_ref = models.ForeignKey(
        Integrations_Etsy_Ledger, on_delete=models.CASCADE, null=True)
    ledger_id = models.TextField(null=True)
    user_iden = models.CharField(max_length=50, null=True, blank=True)
    ledger_entry_id = models.TextField(null=True)
    sequence = models.TextField(null=True)
    credit_amount = models.TextField(null=True)
    debit_amount = models.TextField(null=True)
    entry_type = models.TextField(null=True)
    reference_id = models.TextField(null=True)
    running_balance = models.TextField(null=True)
    create_date = models.DateTimeField(null=True)


class Integrations_Etsy_Transaction_Tag(models.Model):
    objects = models.Manager()
    transaction_ref = models.ForeignKey(
        Integrations_Etsy_Transaction, on_delete=models.CASCADE, null=False)
    tag = TruncatingCharField(max_length=255, null=False)


class Integrations_Etsy_Transaction_Material(models.Model):
    objects = models.Manager()
    transaction_ref = models.ForeignKey(
        Integrations_Etsy_Transaction, on_delete=models.CASCADE, null=False)
    material = TruncatingCharField(max_length=255, null=False)


# TWITTER
class Integrations_Twitter_Mentions(models.Model):
    objects = models.Manager()
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    integration_name = models.CharField(max_length=20, null=True, blank=True)
    user_iden = models.CharField(max_length=50, null=True, blank=True)
    mention_id = models.CharField(max_length=50, null=True, blank=True)
    text = models.CharField(max_length=240, null=True, blank=True)
    other_user_id = models.CharField(max_length=50, null=True, blank=True)
    other_user_name = models.CharField(max_length=50, null=True, blank=True)
    other_user_screen_name = models.CharField(
        max_length=50, null=True, blank=True)
    timestamp = models.DateTimeField(null=True)


#####################QUICKBOOKS MODELS#################################
class Integrations_Quickbooks_Company_Info(models.Model):
    objects = models.Manager()
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    integration_name = models.CharField(max_length=20, null=True, blank=True)
    user_iden = models.CharField(max_length=50, null=True, blank=True)
    company_name = models.CharField(max_length=200, null=True, blank=True)
    company_address = models.TextField(null=True, blank=True)
    create_time = models.DateTimeField(null=True, blank=True)


class Integrations_Quickbooks_Account_Info(models.Model):
    objects = models.Manager()
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    integration_name = models.CharField(max_length=20, null=True, blank=True)
    user_iden = models.CharField(max_length=50, null=True, blank=True)
    account_id = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    current_balance = models.CharField(max_length=50, null=True, blank=True)
    active = models.CharField(max_length=5, null=True, blank=True)
    create_time = models.DateTimeField(null=True, blank=True)
    last_update_time = models.DateTimeField(null=True, blank=True)


class Integrations_Quickbooks_Bills(models.Model):
    objects = models.Manager()
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    integration_name = models.CharField(max_length=20, null=True, blank=True)
    user_iden = models.CharField(max_length=50, null=True, blank=True)
    vendor_name = models.CharField(max_length=150, null=True, blank=True)
    account_name = models.CharField(max_length=150, null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    balance = models.CharField(max_length=20, null=True, blank=True)
    bill_id = models.CharField(max_length=20, null=True, blank=True)
    create_time = models.DateTimeField(null=True, blank=True)
    last_update_time = models.DateTimeField(null=True, blank=True)


class Integrations_Quickbooks_Bill_Line_Items(models.Model):
    objects = models.Manager()
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    integration_name = models.CharField(max_length=20, null=True, blank=True)
    user_iden = models.CharField(max_length=50, null=True, blank=True)
    item_id = models.CharField(max_length=20, null=True, blank=True)
    item_name = models.CharField(max_length=100, null=True, blank=True)
    bill_ref = models.ForeignKey(Integrations_Quickbooks_Bills,
                                 on_delete=models.CASCADE, null=True, related_name='line_items')
    description = models.CharField(max_length=220, null=True, blank=True)
    amount = models.CharField(max_length=20, null=True, blank=True)
    unit_price = models.CharField(max_length=20, null=True, blank=True)
    detail_type = models.CharField(max_length=120, null=True, blank=True)
    quantity = models.CharField(max_length=20, null=True, blank=True)


class Integrations_Quickbooks_Ledger_Reports(models.Model):
    objects = models.Manager()
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    integration_name = models.CharField(max_length=20, null=True, blank=True)
    user_iden = models.CharField(max_length=50, null=True, blank=True)
    account_id = models.CharField(max_length=150, null=True, blank=True)
    account_name = models.CharField(max_length=150, null=True, blank=True)
    beginning_balance = models.CharField(max_length=50, null=True, blank=True)
    ending_balance = models.CharField(max_length=50, null=True, blank=True)
    transaction_balance = models.CharField(
        max_length=50, null=True, blank=True)
    start_period = models.DateTimeField(null=True, blank=True)
    end_period = models.DateTimeField(null=True, blank=True)
    create_time = models.DateTimeField(null=True, blank=True)


class Integrations_Quickbooks_Ledger_Expenses(models.Model):
    objects = models.Manager()
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)
    integration_name = models.CharField(max_length=20, null=True, blank=True)
    user_iden = models.CharField(max_length=50, null=True, blank=True)
    transaction_id = models.CharField(max_length=50, null=True, blank=True)
    ledger_ref = models.ForeignKey(
        Integrations_Quickbooks_Account_Info, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(null=True, blank=True)
    category = models.CharField(max_length=150, null=True, blank=True)
    transaction_type = models.CharField(max_length=150, null=True, blank=True)
    vendor = models.CharField(max_length=150, null=True, blank=True)
    description = models.CharField(max_length=220, null=True, blank=True)
    amount = models.CharField(max_length=50, null=True, blank=True)
    current_ledger_value = models.CharField(
        max_length=50, null=True, blank=True)


class TimeLine_Entry(models.Model):
    objects = models.Manager()
    id = models.CharField(max_length=100, primary_key=True)
    integration = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=False)
    insight = models.TextField(null=False)
    data = JSONField(null=False)
    ts = models.DateTimeField(null=False)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
