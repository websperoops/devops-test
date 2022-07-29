from allauth.socialaccount.models import SocialAccount
from dashboards.models import Integrations_Shopify_Product

from django.contrib.auth.models import User
from django.test import TransactionTestCase


class TruncatingCharFieldTestCase(TransactionTestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="test12345")
        self.socialaccount = SocialAccount.objects.create(user=self.user, provider='shopify', uid='123')

    def test_1(self):
        product = Integrations_Shopify_Product.objects.create(integration=self.socialaccount, product_id="12243")
        too_long_string = "QkV3rbHo3Rie1iacOQEpNFIZqlbmZZMo8oA7WQKf8MLqUNywgq" + \
                          "NudqDXAHAJ8L9XdwMDiBWW4baxnGP0ngD1HbLDd3hYVt6yUNgk" + \
                          "b2XgAqL6ph6lhR6KiIi4JnDdNTYgN0qzYAWQEtbpCk6JSylSBC" + \
                          "SrlXXqduYOeh7tNsCdPLsLNyYNuAZ2XAi4undH3vFC24LCmi1P" + \
                          "jUnCN9ifrNoCflCjNYw3GPRI7GzqIj7OW7olwIe8qMtJbFLnJ1" + \
                          "GTiTHFPOc11bKGn36pjkEO8kelM6vSc6FjwtgAMCNIkLKA8jQQ" + \
                          "c10AhhLtOMTX9IYke0caNEUAd6KPEG3E89FucmBc4tSTvjbZQf"

        product.title = too_long_string
        product.save()
        product.refresh_from_db()
        self.assertEqual(len(product.title), 255)

    def test_2(self):
        product = Integrations_Shopify_Product.objects.create(integration=self.socialaccount, product_id="12243")
        small_string = "i"

        product.title = small_string
        product.save()
        product.refresh_from_db()
        self.assertEqual(len(product.title), len(small_string))
