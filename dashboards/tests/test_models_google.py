from allauth.socialaccount.models import SocialAccount

from dashboards.google import parse_report
from dashboards.models import Integrations_Google_Web_Property, \
    Integrations_Google_Analytics_Account, Integrations_Google_Medium, Integrations_Google_Profile, \
    Integrations_Google_Source, Integrations_Google_Social_Network, Integrations_Google_Page_Title, \
    Integrations_Google_Website_Total, Integrations_Google_User_Type, Integrations_Google_Geolocation

from django.contrib.auth.models import User
from django.test import TransactionTestCase, tag
from django.utils import timezone

import json
import pytz


class GoogleMetricsTestCase(TransactionTestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="test12345")
        self.socialaccount = SocialAccount.objects.create(user=self.user, provider='openid', uid='123')
        self.analytics_accont = Integrations_Google_Analytics_Account.objects.create(social_account=self.socialaccount,
                                                                                     name="Blocklight",
                                                                                     account_id="120810601")
        self.webProperty = Integrations_Google_Web_Property.objects.create(account=self.analytics_accont,
                                                                           property_id="UA-120810601-1",
                                                                           internal_id="178618680", name="Blocklight",
                                                                           website_url="https://www.blocklight.io/")
        self.profile = Integrations_Google_Profile.objects.create(web_property=self.webProperty, view_id="177083815",
                                                                  name="All Web Site Data", time_zone="America/Chicago")

    @tag("Google", "Sync", "Models")
    def test_medium_sync(self):
        model = Integrations_Google_Medium
        with open("dashboards/tests/resources/google/medium.json") as fp:
            reports = json.load(fp)

        rows = parse_report(reports["reports"][0])
        before_sync_time = timezone.now()
        model.sync(self.profile, data=rows[0])
        after_sync_time = timezone.now()

        self.assertEqual(Integrations_Google_Medium.objects.count(), 1)

        entry = Integrations_Google_Medium.objects.first()

        self.assertEqual(entry.medium, "(none)")
        self.assertEqual(entry.users, 1179)
        self.assertEqual(entry.profile, self.profile)
        self.assertTrue(entry.last_sync_time > before_sync_time)
        self.assertTrue(entry.last_sync_time < after_sync_time)
        datehour = entry.datehour.astimezone(pytz.timezone(self.profile.time_zone))
        self.assertEqual(datehour.year, 2018)
        self.assertEqual(datehour.month, 6)
        self.assertEqual(datehour.day, 16)
        self.assertEqual(datehour.hour, 14)

    @tag("Google", "Sync", "Models")
    def test_medium_sync_mulitple(self):
        model = Integrations_Google_Medium
        with open("dashboards/tests/resources/google/medium.json") as fp:
            reports = json.load(fp)

        rows = parse_report(reports["reports"][0])
        start_date = ["30daysago", "60daysago"]
        before_sync_time = timezone.now()
        model.sync(self.profile, data=rows[0])
        model.sync(self.profile, data=rows[1])
        after_sync_time = timezone.now()

        self.assertEqual(Integrations_Google_Medium.objects.count(), 2)

        entry1 = Integrations_Google_Medium.objects.earliest('datehour')
        entry2 = Integrations_Google_Medium.objects.latest('datehour')

        self.assertEqual(entry1.medium, "(none)")
        self.assertEqual(entry1.users, 1179)
        self.assertEqual(entry1.profile, self.profile)
        self.assertTrue(entry1.last_sync_time > before_sync_time)
        self.assertTrue(entry1.last_sync_time < after_sync_time)
        datehour = entry1.datehour.astimezone(pytz.timezone(self.profile.time_zone))
        self.assertEqual(datehour.year, 2018)
        self.assertEqual(datehour.month, 6)
        self.assertEqual(datehour.day, 16)
        self.assertEqual(datehour.hour, 14)

        self.assertEqual(entry2.medium, "organic")
        self.assertEqual(entry2.users, 199)
        self.assertEqual(entry2.profile, self.profile)
        self.assertTrue(entry2.last_sync_time > before_sync_time)
        self.assertTrue(entry2.last_sync_time < after_sync_time)
        datehour = entry2.datehour.astimezone(pytz.timezone(self.profile.time_zone))
        self.assertEqual(datehour.year, 2018)
        self.assertEqual(datehour.month, 6)
        self.assertEqual(datehour.day, 17)
        self.assertEqual(datehour.hour, 22)

        self.assertTrue(entry2.last_sync_time > entry1.last_sync_time)

    @tag("Google", "Sync", "Models")
    def test_medium_sync_duplicate(self):
        model = Integrations_Google_Medium
        with open("dashboards/tests/resources/google/medium.json") as fp:
            reports = json.load(fp)

        rows = parse_report(reports["reports"][0])
        start_date = "60daysago"
        model.sync(self.profile, data=rows[0])

        last_sync_time = Integrations_Google_Medium.objects.first().last_sync_time

        rows[0]["ga:users"] = 3000
        model.sync(self.profile, data=rows[0])
        entry = Integrations_Google_Medium.objects.first()

        self.assertEqual(entry.medium, "(none)")
        self.assertEqual(entry.users, 3000)
        self.assertEqual(entry.profile, self.profile)
        self.assertTrue(entry.last_sync_time > last_sync_time)
        datehour = entry.datehour.astimezone(pytz.timezone(self.profile.time_zone))
        self.assertEqual(datehour.year, 2018)
        self.assertEqual(datehour.month, 6)
        self.assertEqual(datehour.day, 16)
        self.assertEqual(datehour.hour, 14)

    @tag("Google", "Sync", "Models")
    def test_source_sync(self):
        model = Integrations_Google_Source
        with open("dashboards/tests/resources/google/source.json") as fp:
            reports = json.load(fp)

        rows = parse_report(reports["reports"][0])
        before_sync_time = timezone.now()
        model.sync(self.profile, data=rows[0])
        after_sync_time = timezone.now()

        self.assertEqual(Integrations_Google_Source.objects.count(), 1)

        entry = Integrations_Google_Source.objects.first()

        self.assertEqual(entry.source, "(direct)")
        self.assertEqual(entry.users, 1179)
        self.assertEqual(entry.has_social_referral, False)
        self.assertEqual(entry.profile, self.profile)
        self.assertTrue(entry.last_sync_time > before_sync_time)
        self.assertTrue(entry.last_sync_time < after_sync_time)
        datehour = entry.datehour.astimezone(pytz.timezone(self.profile.time_zone))
        self.assertEqual(datehour.year, 2018)
        self.assertEqual(datehour.month, 6)
        self.assertEqual(datehour.day, 16)
        self.assertEqual(datehour.hour, 14)

    @tag("Google", "Sync", "Models")
    def test_source_sync_multiple(self):
        model = Integrations_Google_Source
        with open("dashboards/tests/resources/google/source.json") as fp:
            reports = json.load(fp)

        rows = parse_report(reports["reports"][0])
        before_sync_time = timezone.now()
        model.sync(self.profile, data=rows[0])
        model.sync(self.profile, data=rows[1])
        after_sync_time = timezone.now()

        self.assertEqual(Integrations_Google_Source.objects.count(), 2)

        entry1 = Integrations_Google_Source.objects.earliest('datehour')
        entry2 = Integrations_Google_Source.objects.latest('datehour')

        self.assertEqual(entry1.source, "(direct)")
        self.assertEqual(entry1.has_social_referral, False)
        self.assertEqual(entry1.users, 1179)
        self.assertEqual(entry1.profile, self.profile)
        self.assertTrue(entry1.last_sync_time > before_sync_time)
        self.assertTrue(entry1.last_sync_time < after_sync_time)
        datehour = entry1.datehour.astimezone(pytz.timezone(self.profile.time_zone))
        self.assertEqual(datehour.year, 2018)
        self.assertEqual(datehour.month, 6)
        self.assertEqual(datehour.day, 16)
        self.assertEqual(datehour.hour, 14)

        self.assertEqual(entry2.source, "accounts.google.com")
        self.assertEqual(entry2.has_social_referral, True)
        self.assertEqual(entry2.users, 4)
        self.assertEqual(entry2.profile, self.profile)
        self.assertTrue(entry2.last_sync_time > before_sync_time)
        self.assertTrue(entry2.last_sync_time < after_sync_time)
        datehour = entry2.datehour.astimezone(pytz.timezone(self.profile.time_zone))
        self.assertEqual(datehour.year, 2018)
        self.assertEqual(datehour.month, 6)
        self.assertEqual(datehour.day, 17)
        self.assertEqual(datehour.hour, 22)

        self.assertTrue(entry2.last_sync_time > entry1.last_sync_time)

    @tag("Google", "Sync", "Models")
    def test_source_sync_duplicate(self):
        model = Integrations_Google_Source
        with open("dashboards/tests/resources/google/source.json") as fp:
            reports = json.load(fp)

        rows = parse_report(reports["reports"][0])
        model.sync(self.profile,  data=rows[0])

        last_sync_time = Integrations_Google_Source.objects.first().last_sync_time

        rows[0]["ga:users"] = 3000
        model.sync(self.profile,  data=rows[0])
        self.assertEqual(Integrations_Google_Source.objects.count(), 1)

        entry = Integrations_Google_Source.objects.first()

        self.assertEqual(entry.source, "(direct)")
        self.assertEqual(entry.users, 3000)
        self.assertEqual(entry.has_social_referral, False)
        self.assertEqual(entry.profile, self.profile)
        self.assertTrue(entry.last_sync_time > last_sync_time)
        datehour = entry.datehour.astimezone(pytz.timezone(self.profile.time_zone))
        self.assertEqual(datehour.year, 2018)
        self.assertEqual(datehour.month, 6)
        self.assertEqual(datehour.day, 16)
        self.assertEqual(datehour.hour, 14)

    @tag("Google", "Sync", "Models")
    def test_social_network_sync(self):
        model = Integrations_Google_Social_Network
        with open("dashboards/tests/resources/google/social_network.json") as fp:
            reports = json.load(fp)

        rows = parse_report(reports["reports"][0])
        before_sync_time = timezone.now()
        model.sync(self.profile, data=rows[0])
        after_sync_time = timezone.now()

        self.assertEqual(Integrations_Google_Social_Network.objects.count(), 1)

        entry = Integrations_Google_Social_Network.objects.first()

        self.assertEqual(entry.social_network, "(not set)")
        self.assertEqual(entry.users, 1373)
        self.assertEqual(entry.profile, self.profile)
        self.assertTrue(entry.last_sync_time > before_sync_time)
        self.assertTrue(entry.last_sync_time < after_sync_time)
        datehour = entry.datehour.astimezone(pytz.timezone(self.profile.time_zone))
        self.assertEqual(datehour.year, 2018)
        self.assertEqual(datehour.month, 6)
        self.assertEqual(datehour.day, 16)
        self.assertEqual(datehour.hour, 14)

    @tag("Google", "Sync", "Models")
    def test_social_network_sync_multiple(self):
        model = Integrations_Google_Social_Network
        with open("dashboards/tests/resources/google/social_network.json") as fp:
            reports = json.load(fp)

        rows = parse_report(reports["reports"][0])
        before_sync_time = timezone.now()
        model.sync(self.profile, data=rows[0])
        model.sync(self.profile, data=rows[1])
        after_sync_time = timezone.now()

        self.assertEqual(Integrations_Google_Social_Network.objects.count(), 2)

        entry1 = Integrations_Google_Social_Network.objects.earliest('datehour')
        entry2 = Integrations_Google_Social_Network.objects.latest('datehour')

        self.assertEqual(entry1.social_network, "(not set)")
        self.assertEqual(entry1.users, 1373)
        self.assertEqual(entry1.profile, self.profile)
        self.assertTrue(entry1.last_sync_time > before_sync_time)
        self.assertTrue(entry1.last_sync_time < after_sync_time)
        datehour = entry1.datehour.astimezone(pytz.timezone(self.profile.time_zone))
        self.assertEqual(datehour.year, 2018)
        self.assertEqual(datehour.month, 6)
        self.assertEqual(datehour.day, 16)
        self.assertEqual(datehour.hour, 14)

        self.assertEqual(entry2.social_network, "Facebook")
        self.assertEqual(entry2.users, 127)
        self.assertEqual(entry2.profile, self.profile)
        self.assertTrue(entry2.last_sync_time > before_sync_time)
        self.assertTrue(entry2.last_sync_time < after_sync_time)
        datehour = entry2.datehour.astimezone(pytz.timezone(self.profile.time_zone))
        self.assertEqual(datehour.year, 2018)
        self.assertEqual(datehour.month, 6)
        self.assertEqual(datehour.day, 17)
        self.assertEqual(datehour.hour, 22)

        self.assertTrue(entry2.last_sync_time > entry1.last_sync_time)

    @tag("Google", "Sync", "Models")
    def test_social_network_sync_duplicate(self):
        model = Integrations_Google_Social_Network
        with open("dashboards/tests/resources/google/social_network.json") as fp:
            reports = json.load(fp)

        rows = parse_report(reports["reports"][0])
        model.sync(self.profile, data=rows[0])

        last_sync_time = Integrations_Google_Social_Network.objects.first().last_sync_time

        rows[0]["ga:users"] = 3000
        model.sync(self.profile, data=rows[0])
        self.assertEqual(Integrations_Google_Social_Network.objects.count(), 1)

        entry = Integrations_Google_Social_Network.objects.first()

        self.assertEqual(entry.social_network, "(not set)")
        self.assertEqual(entry.users, 3000)
        self.assertEqual(entry.profile, self.profile)
        self.assertTrue(entry.last_sync_time > last_sync_time)
        datehour = entry.datehour.astimezone(pytz.timezone(self.profile.time_zone))
        self.assertEqual(datehour.year, 2018)
        self.assertEqual(datehour.month, 6)
        self.assertEqual(datehour.day, 16)
        self.assertEqual(datehour.hour, 14)

    @tag("Google", "Sync", "Models")
    def test_page_title_sync(self):
        model = Integrations_Google_Page_Title
        with open("dashboards/tests/resources/google/page_title.json") as fp:
            reports = json.load(fp)

        rows = parse_report(reports["reports"][0])
        before_sync_time = timezone.now()
        model.sync(self.profile, data=rows[0])
        after_sync_time = timezone.now()

        self.assertEqual(Integrations_Google_Page_Title.objects.count(), 1)

        entry = Integrations_Google_Page_Title.objects.first()

        self.assertEqual(entry.profile, self.profile)
        self.assertEqual(entry.page_title, "(not set)")
        self.assertEqual(entry.page_views, 2)
        self.assertEqual(entry.unique_page_views, 1)
        self.assertEqual(entry.time_on_page, 1524)
        self.assertEqual(entry.exits, 0)
        self.assertEqual(entry.sessions, 1)
        self.assertEqual(entry.screen_views, 0)
        self.assertTrue(entry.last_sync_time > before_sync_time)
        self.assertTrue(entry.last_sync_time < after_sync_time)
        datehour = entry.datehour.astimezone(pytz.timezone(self.profile.time_zone))
        self.assertEqual(datehour.year, 2018)
        self.assertEqual(datehour.month, 7)
        self.assertEqual(datehour.day, 9)
        self.assertEqual(datehour.hour, 22)

    @tag("Google", "Sync", "Models")
    def test_social_page_title_multiple(self):
        model = Integrations_Google_Page_Title
        with open("dashboards/tests/resources/google/page_title.json") as fp:
            reports = json.load(fp)

        rows = parse_report(reports["reports"][0])
        before_sync_time = timezone.now()
        model.sync(self.profile , data=rows[0])
        model.sync(self.profile , data=rows[1])
        after_sync_time = timezone.now()

        self.assertEqual(Integrations_Google_Page_Title.objects.count(), 2)

        entry1 = Integrations_Google_Page_Title.objects.earliest('datehour')
        entry2 = Integrations_Google_Page_Title.objects.latest('datehour')

        self.assertEqual(entry1.profile, self.profile)
        self.assertEqual(entry1.page_title, "(not set)")
        self.assertEqual(entry1.page_views, 2)
        self.assertEqual(entry1.unique_page_views, 1)
        self.assertEqual(entry1.time_on_page, 1524)
        self.assertEqual(entry1.exits, 0)
        self.assertEqual(entry1.sessions, 1)
        self.assertEqual(entry1.screen_views, 0)
        self.assertTrue(entry1.last_sync_time > before_sync_time)
        self.assertTrue(entry1.last_sync_time < after_sync_time)
        datehour = entry1.datehour.astimezone(pytz.timezone(self.profile.time_zone))
        self.assertEqual(datehour.year, 2018)
        self.assertEqual(datehour.month, 7)
        self.assertEqual(datehour.day, 9)
        self.assertEqual(datehour.hour, 22)

        self.assertEqual(entry2.profile, self.profile)
        self.assertEqual(entry2.page_title, "Blocklight - Home")
        self.assertEqual(entry2.page_views, 11)
        self.assertEqual(entry2.unique_page_views, 3)
        self.assertEqual(entry2.time_on_page, 1206)
        self.assertEqual(entry2.exits, 0)
        self.assertEqual(entry2.sessions, 1)
        self.assertEqual(entry2.screen_views, 0)
        self.assertTrue(entry2.last_sync_time > before_sync_time)
        self.assertTrue(entry2.last_sync_time < after_sync_time)
        datehour = entry2.datehour.astimezone(pytz.timezone(self.profile.time_zone))
        self.assertEqual(datehour.year, 2018)
        self.assertEqual(datehour.month, 7)
        self.assertEqual(datehour.day, 17)
        self.assertEqual(datehour.hour, 10)

        self.assertTrue(entry2.last_sync_time > entry1.last_sync_time)

    @tag("Google", "Sync", "Models")
    def test_social_page_title_duplicate(self):
        model = Integrations_Google_Page_Title
        with open("dashboards/tests/resources/google/page_title.json") as fp:
            reports = json.load(fp)

        rows = parse_report(reports["reports"][0])
        model.sync(self.profile, data=rows[0])

        last_sync_time = Integrations_Google_Page_Title.objects.first().last_sync_time

        rows[0]["ga:pageviews"] = 3000
        model.sync(self.profile, data=rows[0])
        self.assertEqual(Integrations_Google_Page_Title.objects.count(), 1)

        entry = Integrations_Google_Page_Title.objects.first()

        self.assertEqual(entry.profile, self.profile)
        self.assertEqual(entry.page_title, "(not set)")
        self.assertEqual(entry.page_views, 3000)
        self.assertEqual(entry.unique_page_views, 1)
        self.assertEqual(entry.time_on_page, 1524)
        self.assertEqual(entry.exits, 0)
        self.assertEqual(entry.sessions, 1)
        self.assertEqual(entry.screen_views, 0)
        self.assertTrue(entry.last_sync_time > last_sync_time)
        datehour = entry.datehour.astimezone(pytz.timezone(self.profile.time_zone))
        self.assertEqual(datehour.year, 2018)
        self.assertEqual(datehour.month, 7)
        self.assertEqual(datehour.day, 9)
        self.assertEqual(datehour.hour, 22)

    @tag("Google", "Sync", "Models")
    def test_website_total_sync(self):
        model = Integrations_Google_Website_Total
        with open("dashboards/tests/resources/google/google_website_total.json") as fp1:
            reports1 = json.load(fp1)

        rows1 = parse_report(reports1["reports"][0])

        before_sync_time = timezone.now()
        model.sync(self.profile, data=rows1[0])
        after_sync_time = timezone.now()

        self.assertEqual(Integrations_Google_Website_Total.objects.count(), 1)

        entry = Integrations_Google_Website_Total.objects.first()

        self.assertEqual(entry.profile, self.profile)
        self.assertEqual(entry.page_views, 8)
        self.assertEqual(entry.unique_page_views, 1)
        self.assertEqual(entry.time_on_page, 1227)
        self.assertEqual(entry.exits, 1)
        self.assertEqual(entry.sessions, 3)
        self.assertEqual(entry.bounces, 5)
        self.assertEqual(entry.hits, 8)
        self.assertEqual(entry.screen_views, 7)
        self.assertEqual(entry.session_duration, 1)
        self.assertTrue(entry.last_sync_time > before_sync_time)
        self.assertTrue(entry.last_sync_time < after_sync_time)

    @tag("Google", "Sync", "Models")
    def test_user_type_sync(self):
        model = Integrations_Google_User_Type
        with open("dashboards/tests/resources/google/usertype.json") as fp:
            reports = json.load(fp)

        rows = parse_report(reports["reports"][0])
        before_sync_time = timezone.now()
        model.sync(self.profile, data=rows[0])
        after_sync_time = timezone.now()

        self.assertEqual(Integrations_Google_User_Type.objects.count(), 1)

        entry = Integrations_Google_User_Type.objects.first()

        self.assertEqual(entry.user_type, "New Visitor")
        self.assertEqual(entry.users, 1526)
        self.assertEqual(entry.profile, self.profile)
        self.assertTrue(entry.last_sync_time > before_sync_time)
        self.assertTrue(entry.last_sync_time < after_sync_time)
        datehour = entry.datehour.astimezone(pytz.timezone(self.profile.time_zone))
        self.assertEqual(datehour.year, 2018)
        self.assertEqual(datehour.month, 6)
        self.assertEqual(datehour.day, 16)
        self.assertEqual(datehour.hour, 14)

    @tag("Google", "Sync", "Models")
    def test_user_type_multiple(self):
        model = Integrations_Google_User_Type
        with open("dashboards/tests/resources/google/usertype.json") as fp:
            reports = json.load(fp)

        rows = parse_report(reports["reports"][0])
        before_sync_time = timezone.now()
        model.sync(self.profile, data=rows[0])
        model.sync(self.profile, data=rows[1])
        after_sync_time = timezone.now()

        self.assertEqual(Integrations_Google_User_Type.objects.count(), 2)

        entry1 = Integrations_Google_User_Type.objects.earliest('datehour')
        entry2 = Integrations_Google_User_Type.objects.latest('datehour')

        self.assertEqual(entry1.user_type, "New Visitor")
        self.assertEqual(entry1.users, 1526)
        self.assertEqual(entry1.profile, self.profile)
        self.assertTrue(entry1.last_sync_time > before_sync_time)
        self.assertTrue(entry1.last_sync_time < after_sync_time)
        datehour = entry1.datehour.astimezone(pytz.timezone(self.profile.time_zone))
        self.assertEqual(datehour.year, 2018)
        self.assertEqual(datehour.month, 6)
        self.assertEqual(datehour.day, 16)
        self.assertEqual(datehour.hour, 14)

        self.assertEqual(entry2.user_type, "Returning Visitor")
        self.assertEqual(entry2.users, 324)
        self.assertEqual(entry2.profile, self.profile)
        self.assertTrue(entry2.last_sync_time > before_sync_time)
        self.assertTrue(entry2.last_sync_time < after_sync_time)
        datehour = entry2.datehour.astimezone(pytz.timezone(self.profile.time_zone))
        self.assertEqual(datehour.year, 2018)
        self.assertEqual(datehour.month, 6)
        self.assertEqual(datehour.day, 20)
        self.assertEqual(datehour.hour, 12)

        self.assertTrue(entry2.last_sync_time > entry1.last_sync_time)

    @tag("Google", "Sync", "Models")
    def test_user_type_sync_duplicate(self):
        model = Integrations_Google_User_Type
        with open("dashboards/tests/resources/google/usertype.json") as fp:
            reports = json.load(fp)

        rows = parse_report(reports["reports"][0])
        model.sync(self.profile, data=rows[0])

        last_sync_time = Integrations_Google_User_Type.objects.first().last_sync_time

        rows[0]["ga:users"] = 3000
        model.sync(self.profile, data=rows[0])
        entry = Integrations_Google_User_Type.objects.first()

        self.assertEqual(entry.user_type, "New Visitor")
        self.assertEqual(entry.users, 3000)
        self.assertEqual(entry.profile, self.profile)
        self.assertTrue(entry.last_sync_time > last_sync_time)
        datehour = entry.datehour.astimezone(pytz.timezone(self.profile.time_zone))
        self.assertEqual(datehour.year, 2018)
        self.assertEqual(datehour.month, 6)
        self.assertEqual(datehour.day, 16)
        self.assertEqual(datehour.hour, 14)

    @tag("Google", "Sync", "Models")
    def test_geolocstion(self):
        model = Integrations_Google_Geolocation
        with open("dashboards/tests/resources/google/geolocation.json") as fp1:
            reports1 = json.load(fp1)

        rows1 = parse_report(reports1["reports"][0])

        before_sync_time = timezone.now()
        model.sync(self.profile, data=rows1[0])
        after_sync_time = timezone.now()

        self.assertEqual(Integrations_Google_Geolocation.objects.count(), 1)

        entry = Integrations_Google_Geolocation.objects.first()

        self.assertEqual(entry.profile, self.profile)
        datehour = entry.datehour.astimezone(pytz.timezone(self.profile.time_zone))
        self.assertEqual(datehour.year, 2019)
        self.assertEqual(datehour.month, 7)
        self.assertEqual(datehour.day, 4)
        self.assertEqual(datehour.hour, 5)

        self.assertEqual(entry.users, 1)
        self.assertEqual(entry.continent, "Oceania")
        self.assertEqual(entry.sub_continent, "Australasia")
        self.assertEqual(entry.country, "Australia")
        self.assertEqual(entry.region, "New South Wales")
        self.assertEqual(entry.city, "Sydney")

        self.assertTrue(entry.last_sync_time > before_sync_time)
        self.assertTrue(entry.last_sync_time < after_sync_time)

    @tag("Google", "Sync", "Models")
    def test_geolocstion_duplicate(self):
        model = Integrations_Google_Geolocation
        with open("dashboards/tests/resources/google/geolocation.json") as fp1:
            reports = json.load(fp1)

        rows = parse_report(reports["reports"][0])
        model.sync(self.profile, data=rows[0])

        last_sync_time = Integrations_Google_Geolocation.objects.first().last_sync_time

        rows[0]["ga:users"] = 3000
        model.sync(self.profile, data=rows[0])
        self.assertEqual(Integrations_Google_Geolocation.objects.count(), 1)

        entry = Integrations_Google_Geolocation.objects.first()

        self.assertEqual(entry.profile, self.profile)
        datehour = entry.datehour.astimezone(pytz.timezone(self.profile.time_zone))
        self.assertEqual(datehour.year, 2019)
        self.assertEqual(datehour.month, 7)
        self.assertEqual(datehour.day, 4)
        self.assertEqual(datehour.hour, 5)

        self.assertEqual(entry.users, 3000)
        self.assertEqual(entry.continent, "Oceania")
        self.assertEqual(entry.sub_continent, "Australasia")
        self.assertEqual(entry.country, "Australia")
        self.assertEqual(entry.region, "New South Wales")
        self.assertEqual(entry.city, "Sydney")
        self.assertTrue(entry.last_sync_time > last_sync_time)



