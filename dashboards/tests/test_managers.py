from django.contrib.auth.models import User
from django.test import TransactionTestCase, tag

from dashboards.models import Integrations_Google_Profile, Integrations_Google_Web_Property, \
    Integrations_Google_Analytics_Account, Integrations_Google_Medium

from allauth.socialaccount.models import SocialAccount

from django.utils import timezone

from dashboards.managers import Integrations_GoogleInsights_Medium_Distribution


class GoogleMetricsTestCase(TransactionTestCase):
    fixtures = ["google_accounts.json", "google_medium.json"]

    def setUp(self):
        self.user = User.objects.first()
        self.account = SocialAccount.objects.first()
        self.analytics_accont = Integrations_Google_Analytics_Account.objects.first()
        self.webProperty = Integrations_Google_Web_Property.objects.first()
        self.profile = Integrations_Google_Profile.objects.first()

    @tag("Google", "Managers", "Charts")
    def test_medium_distribution(self):
        start_date = timezone.datetime(year=2018, month=7, day=1, tzinfo=timezone.utc)
        end_date = start_date + timezone.timedelta(days=60)
        self.assertEqual(Integrations_Google_Medium.objects.count(), 10)
        i = Integrations_GoogleInsights_Medium_Distribution()
        data = i.build_series(metric=None, user_iden=self.user.id, option_dict=None, chart_type=None,
                              start_date=start_date, end_date=end_date, interval=None)
        self.assertEqual(len(data), 3)
        self.assertTrue(("referral", 8) in data)
        self.assertTrue(("(none)", 3) in data)
        self.assertTrue(("organic", 4) in data)

    @tag("Google", "Managers", "Charts")
    def test_medium_distribution_2(self):
        start_date = timezone.datetime(year=2018, month=7, day=31, tzinfo=timezone.utc)
        end_date = timezone.datetime(year=2018, month=8, day=10, tzinfo=timezone.utc)
        self.assertEqual(Integrations_Google_Medium.objects.count(), 10)
        i = Integrations_GoogleInsights_Medium_Distribution()
        data = i.build_series(metric=None, user_iden=self.user.id, option_dict=None, chart_type=None,
                              start_date=start_date, end_date=end_date, interval=None)
        self.assertEqual(len(data), 3)
        self.assertTrue(("referral", 4) in data)
        self.assertTrue(("(none)", 2) in data)
        self.assertTrue(("organic", 4) in data)
