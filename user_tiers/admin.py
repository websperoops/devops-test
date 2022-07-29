from django.contrib import admin
from user_tiers.models import Tier, UserTier


admin.site.register(Tier)
admin.site.register(UserTier)