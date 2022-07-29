from .models import Dashboard, Widget, BasicAuthRecords, Integrations_User_LastSync, Report, Element,Tab, BlocklightBilling_Recurring_Shopify
from django.contrib import admin


class DashboardAdmin(admin.ModelAdmin):
    pass
admin.site.register(Dashboard, DashboardAdmin)

class TabAdmin(admin.ModelAdmin):
    pass
admin.site.register(Tab, TabAdmin)


class WidgetAdmin(admin.ModelAdmin):
    pass
admin.site.register(Widget, WidgetAdmin)

class ElementAdmin(admin.ModelAdmin):
    pass
admin.site.register(Element, ElementAdmin)


class ReportAdmin(admin.ModelAdmin):
    pass
admin.site.register(Report, ReportAdmin)

class SyncAdmin(admin.ModelAdmin):
    pass
admin.site.register(Integrations_User_LastSync, SyncAdmin)


class BillingAdmin(admin.ModelAdmin):
    pass
admin.site.register(BlocklightBilling_Recurring_Shopify, BillingAdmin)

class BasicAuthRecordsAdmin(admin.ModelAdmin):
    pass
admin.site.register(BasicAuthRecords, BasicAuthRecordsAdmin)

