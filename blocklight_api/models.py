from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE, PROTECT, SET_NULL


# Create your models here.
class DataSource(models.Model):
    name = models.CharField(max_length=100)
    # api_version = models.CharField(max_length=50)
    url = models.CharField(max_length=100)

    def __str__(self):
        return "<{} - {}: {}>".format(
            self.__class__.__name__,
            self.id,
            self.name
        )


class ChartType(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return "<{} - {}: {}>".format(
            self.__class__.__name__,
            self.id,
            self.name
        )


class PredefinedIntegration(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return "<{} - {}: {}>".format(
            self.__class__.__name__,
            self.id,
            self.name
        )


class PredefinedDashboard(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return "<{} - {}: {}>".format(
            self.__class__.__name__,
            self.id,
            self.name
        )


class PredefinedMetric(models.Model):
    predefined_dashboard = models.ForeignKey(
        PredefinedDashboard, on_delete=CASCADE, null=True, blank=True
    )
    predefined_integrations = models.ManyToManyField(PredefinedIntegration)
    # Used only when creating default dashboards
    predefined_metric_for_edit = models.ForeignKey(
        "self", null=True, blank=True, on_delete=PROTECT
    )
    name = models.CharField(max_length=100)
    chart_type_icon = models.ForeignKey(ChartType, on_delete=PROTECT)

    def __str__(self):
        return "<{} - {}: {}>".format(
            self.__class__.__name__,
            self.id,
            self.name
        )


class PredefinedMetricType(models.Model):

    predefined_metric = models.ForeignKey(PredefinedMetric, on_delete=PROTECT)
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=200, null=True, blank=True)

    datasource = models.ForeignKey(DataSource, on_delete=PROTECT)

    filter_expression = models.CharField(max_length=1000)
    group_by_expression = models.CharField(max_length=1000)
    aggregate_expression = models.CharField(max_length=1000)
    time_group_by_expression = models.CharField(
        max_length=500, null=True, blank=True)

    x_field = models.CharField(max_length=50, null=True, blank=True)
    y_field = models.CharField(max_length=50)
    secondary_y_field = models.CharField(max_length=50, null=True, blank=True)
    group_field = models.CharField(max_length=50, null=True, blank=True)

    x_label = models.CharField(max_length=100, null=True, blank=True)
    y_label = models.CharField(max_length=100)
    secondary_y_label = models.CharField(max_length=100, null=True, blank=True)
    group_label = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return "<{} - {}: {}>".format(
            self.__class__.__name__,
            self.id,
            self.name
        )


class PredefinedDashboardLayout(models.Model):
    predefined_dashboard = models.ForeignKey(
        PredefinedDashboard, on_delete=CASCADE
    )
    predefined_metric = models.ForeignKey(PredefinedMetric, on_delete=CASCADE)
    x = models.IntegerField(null=False)
    y = models.IntegerField(null=False)
    w = models.IntegerField(null=False)
    h = models.IntegerField(null=False)

    def __str__(self):
        return "<{} - {}: {}>".format(
            self.__class__.__name__,
            self.id,
            "{} - x: {} y: {} w: {} h: {}".format(
                self.predefined_metric,
                self.x,
                self.y,
                self.w,
                self.h
            )
        )


class PredefinedChartType(models.Model):
    name = models.CharField(max_length=30)
    predefined_metric = models.ForeignKey(PredefinedMetric, on_delete=PROTECT)

    def __str__(self):
        return "<{} - {}: {}>".format(
            self.__class__.__name__,
            self.id,
            self.name
        )


class PredefinedTimeRange(models.Model):
    name = models.CharField(max_length=30)
    predefined_metric = models.ForeignKey(PredefinedMetric, on_delete=PROTECT)
    since = models.CharField(max_length=500, null=True)
    until = models.CharField(max_length=500, null=True)

    def __str__(self):
        return "<{} - {}: {}>".format(
            self.__class__.__name__,
            self.id,
            self.name
        )


class Integration(models.Model):
    name = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    social_account = models.ForeignKey(
        SocialAccount, on_delete=models.CASCADE, null=True)

    def __str__(self):
        # try:
        #     user = User.objects.get(id=self.user_iden)
        # except User.DoesNotExist:
        #     user = None

        return "<{} - {}: {} - {} - {}>".format(
            self.__class__.__name__,
            self.id,
            self.name,
            self.user.email if self.user else None,
            self.user.id if self.user else None,
        )


class TimeRange(models.Model):
    since = models.CharField(max_length=500, null=True, blank=True)
    until = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return "<{} - {}: {} - {}>".format(
            self.__class__.__name__,
            self.id,
            self.since,
            self.until,
        )


# TODO: Consider joining Metric and Chart to one object/table
class Metric(models.Model):
    datasource = models.ForeignKey(DataSource, on_delete=PROTECT)
    integrations = models.ManyToManyField(Integration)
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=200, null=True, blank=True)
    chart_type = models.ForeignKey(ChartType, on_delete=PROTECT)

    time_range = models.OneToOneField(
        TimeRange, null=True, blank=True, on_delete=PROTECT)

    filter = models.CharField(max_length=500, null=True, blank=True)
    group_by = models.CharField(max_length=500, null=True, blank=True)
    aggregate = models.CharField(max_length=500, null=True, blank=True)
    # TODO: make django's `choices` on this
    # week_dynamic, year_static etc.
    time_group_by = models.CharField(max_length=500, null=True, blank=True)

    x_field = models.CharField(max_length=50, null=True, blank=True)
    y_field = models.CharField(max_length=50)
    secondary_y_field = models.CharField(max_length=50, null=True, blank=True)
    group_field = models.CharField(max_length=50, null=True, blank=True)

    x_label = models.CharField(max_length=100, null=True, blank=True)
    y_label = models.CharField(max_length=100)
    secondary_y_label = models.CharField(max_length=100, null=True, blank=True)
    group_label = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return "<{} - {}: {}>".format(
            self.__class__.__name__,
            self.id,
            self.name
        )


# NOTE: Needs to have BL prefix for now because there is another model
#     dashboards.Dashboard and it and it causes:
#     (fields.E304) Reverse accessor for 'Dashboard.user' clashes with
#     reverse accessor for 'Dashboard.user'
# TODO: Rename to Dashboard after dashboards.Dashboard will be deleted
class BLDashboard(models.Model):
    name = models.CharField(max_length=1000, blank=True)
    user = models.ForeignKey(User, on_delete=CASCADE)
    is_favorite = models.BooleanField(default=False)
    account = models.ForeignKey(SocialAccount, on_delete=SET_NULL, null=True, blank=True)

    def __str__(self):
        return "<{}. {}: {} - {}>".format(
            self.__class__.__name__,
            self.id,
            self.name,
            self.user.email
        )


class Chart(models.Model):
    description = models.CharField(max_length=1000, blank=True)
    metric = models.OneToOneField(Metric, on_delete=CASCADE)
    dashboard = models.ForeignKey(
        BLDashboard,
        related_name='charts',
        related_query_name="chart",
        on_delete=CASCADE
    )
    # PredefinedMetric from which the Chart was created
    # Used for options of editing the chart.
    predefined_metric = models.ForeignKey(PredefinedMetric, on_delete=PROTECT)

    # TODO:
    # tooltip_title
    # tooltip_detail

    def __str__(self):
        return "<{} - {}: {}>".format(
            self.__class__.__name__,
            self.id,
            "{}-{}".format(self.dashboard, self.metric)
        )


class DashboardLayout(models.Model):
    dashboard = models.ForeignKey(BLDashboard, on_delete=CASCADE)
    chart = models.ForeignKey(Chart, on_delete=CASCADE)
    x = models.IntegerField(null=False)
    y = models.IntegerField(null=False)
    w = models.IntegerField(null=False)
    h = models.IntegerField(null=False)

    def __str__(self):
        return "<{} - {}: {}>".format(
            self.__class__.__name__,
            self.id,
            "{} - x: {} y: {} w: {} h: {}".format(
                self.chart,
                self.x,
                self.y,
                self.w,
                self.h
            )
        )


class SummaryIntegration(models.Model):
    name = models.CharField(max_length=100)
    priority_number = models.IntegerField(null=False)

    def __str__(self):
        return "<{} - {}: {}>".format(
            self.__class__.__name__,
            self.id,
            self.name,
            self.priority_number
        )


class SummaryMetric(models.Model):
    integration = models.ForeignKey(
        SummaryIntegration, on_delete=CASCADE, null=True, blank=True
    )
    name = models.CharField(max_length=100)
    data_source = models.ForeignKey(
        DataSource, null=True, blank=True, on_delete=PROTECT
    )
    filter = models.CharField(max_length=100)
    group_by = models.CharField(max_length=100)
    aggregate = models.CharField(max_length=100)
    metric_priority = models.IntegerField(null=False)

    def __str__(self):
        return "<{} - {}: {}>".format(
            self.__class__.__name__,
            self.id,
            self.name
        )


class SummaryTimeRange(models.Model):
    name = models.CharField(max_length=30)
    since = models.CharField(max_length=500, null=True)
    until = models.CharField(max_length=500, null=True)
    compare_since = models.CharField(max_length=500, null=True)
    compare_until = models.CharField(max_length=500, null=True)

    def __str__(self):
        return "<{} - {}: {}>".format(
            self.__class__.__name__,
            self.id,
            self.name
        )


class LoyaltyCode(models.Model):
    loyalty_code = models.CharField(max_length=50)
    trial_period = models.IntegerField(null=False)

    def __str__(self):
        return "<{} - {} - {}>".format(
            self.__class__.__name__,
            self.id,
            self.loyalty_code,
            self.trial_period,
        )


class TopSocialIntegration(models.Model):
    name = models.CharField(max_length=50)
    priority_number = models.IntegerField(null=False)
    DATA_TYPE_FIELD = [
        ('POST', 'post'),
        ('STORY', 'story')
    ]
    data_type = models.CharField(
        max_length=5,
        choices=DATA_TYPE_FIELD,
        default='POST'
    )

    def __str__(self):
        return "<{} - {}: {}>".format(
            self.__class__.__name__,
            self.id,
            self.name,
            self.priority_number
        )


class TopSocialMetric(models.Model):
    integration = models.ForeignKey(
        TopSocialIntegration, on_delete=CASCADE, null=True, blank=True
    )
    name = models.CharField(max_length=100)
    data_source = models.ForeignKey(
        DataSource, null=True, blank=True, on_delete=PROTECT
    )
    filter = models.CharField(max_length=100)
    group_by = models.CharField(max_length=100)
    aggregate = models.CharField(max_length=100)
    
    DATA_SOURCE_CHOICES = [
        ('EN', 'engagements'),
        ('RE', 'reactions'),
        ('IM', 'impressions'),
        ('PO', 'posts')
    ]
    sources = models.CharField(
        max_length=2,
        choices=DATA_SOURCE_CHOICES,
        default='PO'
    )
    
    def __str__(self):
        return "<{} - {}: {}>".format(
            self.__class__.__name__,
            self.id,
            self.name
        )


class TopSocialTimeRange(models.Model):
    name = models.CharField(max_length=30)
    since = models.CharField(max_length=500, null=True)
    until = models.CharField(max_length=500, null=True)

    def __str__(self):
        return "<{} - {}: {}>".format(
            self.__class__.__name__,
            self.id,
            self.name
        )