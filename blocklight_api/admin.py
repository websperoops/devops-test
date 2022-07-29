from blocklight_api import models as blapi_models
from django.contrib import admin


admin.site.register(blapi_models.Integration)
admin.site.register(blapi_models.DataSource)
admin.site.register(blapi_models.ChartType)
admin.site.register(blapi_models.TimeRange)
admin.site.register(blapi_models.Metric)
admin.site.register(blapi_models.BLDashboard)
admin.site.register(blapi_models.DashboardLayout)
admin.site.register(blapi_models.Chart)
admin.site.register(blapi_models.PredefinedDashboard)
admin.site.register(blapi_models.PredefinedDashboardLayout)
admin.site.register(blapi_models.PredefinedIntegration)
admin.site.register(blapi_models.PredefinedMetric)
admin.site.register(blapi_models.PredefinedMetricType)
admin.site.register(blapi_models.PredefinedChartType)
admin.site.register(blapi_models.PredefinedTimeRange)
admin.site.register(blapi_models.SummaryIntegration)
admin.site.register(blapi_models.SummaryMetric)
admin.site.register(blapi_models.SummaryTimeRange)
admin.site.register(blapi_models.LoyaltyCode)

admin.site.register(blapi_models.TopSocialIntegration)
admin.site.register(blapi_models.TopSocialMetric)
admin.site.register(blapi_models.TopSocialTimeRange)
