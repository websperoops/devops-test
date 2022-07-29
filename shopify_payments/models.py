# from django.db import models
# from django.contrib.auth.models import User
#
# from user_tiers.models import Tier
#
#
# class ShopifyUserAccessToken(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
#     token = models.CharField(max_length=250, null=True)
#
#     def __str__(self):
#         return "<ShopifyAccessToken user-email: {}".format(self.user.email)
