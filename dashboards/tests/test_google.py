from allauth.socialaccount.models import SocialToken
from datetime import timedelta

from dashboards.integrations.google.google_api import set_up_google_cred, get_google_account_summaries, \
    query_google_profile_info, query_google_account_summaries, get_batch_reports, group_reports, \
    build_report_requests

from dashboards.models import Integrations_Google_Profile, Integrations_Google_Web_Property, \
    Integrations_Google_Analytics_Account, Integrations_Google_Medium, Integrations_Google_Website_Total, \
    Integrations_Google_Source, Integrations_Google_User_Type

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.test import TransactionTestCase, tag
from django.utils import timezone

import json
import logging
from unittest.mock import patch, MagicMock, Mock


logger = logging.getLogger(__name__)


# util/helper functions

# Used for mocking google.oauth2._client.refresh_grant function which is used when refreshing an access token
def set_up_mock_refresh_grant(mock_obj):
    execpted_expiration = timezone.now() + timedelta(hours=1)

    def side_effect(value):
        return value

    response_grant = Mock()
    response_grant.get = MagicMock(side_effect=side_effect)
    mock_obj.return_value = ["New access token", "Refresh token", execpted_expiration, response_grant]


# set up a mock analytics object to return account summaries (from json file)
def set_up_mock_initialize_acc_sum(mock_obj, account_summaries_file, profile_json_file):
    with open(account_summaries_file) as fp:
        accs = json.load(fp)
    with open(profile_json_file) as fp:
        profiles = json.load(fp)
    mock_obj.return_value.management.return_value.accountSummaries.return_value.list.return_value.execute.return_value = accs
    mock_obj.return_value.management.return_value.profiles.return_value.get.return_value.execute.return_value = profiles


# set up mocking nalytics.management().profiles().get(accountId=account_id, webPropertyId=web_property_id, profileId=view_id).execute()
def set_up_mock_query_profile(mock_obj, json_file):
    with open(json_file) as fp:
        obj = json.load(fp)
    mock_obj.management.return_value.profiles.return_value.get.return_value.execute.return_value = obj


class GoogleTestCase(TransactionTestCase):
    fixtures = ["initial_google_token.json"]

    def setUp(self):
        self.token = SocialToken.objects.all().first()
        self.account = self.token.account

    @tag("Google")
    def test_expired_token_creds(self):
        self.token.expires_at = timezone.now() - timedelta(days=1)
        self.token.save()
        with patch("google.oauth2._client.refresh_grant") as mock_refresh_grant:
            execpted_expiration = timezone.now() + timedelta(hours=1)

            def side_effect(value):
                return value

            response_grant = Mock()
            response_grant.get = MagicMock(side_effect=side_effect)

            mock_refresh_grant.return_value = ["New access token", "Refresh token", execpted_expiration, response_grant]

            creds = set_up_google_cred(self.token)
            self.assertEqual(creds.token, "New access token")
            self.assertEqual(creds.expiry, execpted_expiration)
            self.token.refresh_from_db()
            self.assertEqual(self.token.token, "New access token")
            self.assertEqual(self.token.expires_at, execpted_expiration)

    @tag("Google")
    def test_not_expired_cred(self):
        self.token.expires_at = timezone.now() + timedelta(days=1)
        self.token.save()
        old_token = self.token.token
        old_expire = self.token.expires_at.replace(tzinfo=None)
        with patch("google.oauth2._client.refresh_grant") as mock_refresh_grant:
            execpted_expiration = timezone.now() + timedelta(hours=1)

            def side_effect(value):
                return value

            response_grant = Mock()
            response_grant.get = MagicMock(side_effect=side_effect)

            mock_refresh_grant.return_value = ["New access token", "Refresh token", execpted_expiration, response_grant]

            creds = set_up_google_cred(self.token)
            self.assertEqual(creds.token, old_token)
            self.assertEqual(creds.expiry, old_expire)
            self.token.refresh_from_db()
            self.assertEqual(self.token.token, old_token)
            self.assertEqual(self.token.expires_at.replace(tzinfo=None), old_expire)

    @tag("Google")
    def test_query_google_account_summaries(self):
        with patch("google.oauth2._client.refresh_grant") as mock_refresh_grant, \
                patch("dashboards.google.initialize_analytics") as mock_initialize:
            set_up_mock_refresh_grant(mock_refresh_grant)
            set_up_mock_initialize_acc_sum(mock_initialize,
                                           "dashboards/tests/resources/google/account_summaries.json",
                                           "dashboards/tests/resources/google/profile.json")
            query_google_account_summaries(self.account)

            # check the database
            self.assertEqual(Integrations_Google_Analytics_Account.objects.count(), 3)
            self.assertEqual(Integrations_Google_Web_Property.objects.count(), 5)
            self.assertEqual(Integrations_Google_Profile.objects.count(), 8)
            try:
                account1 = Integrations_Google_Analytics_Account.objects.get(social_account=self.account,
                                                                             name="Another test",
                                                                             account_id="142018643")
                account2 = Integrations_Google_Analytics_Account.objects.get(social_account=self.account,
                                                                             name="Blocklight",
                                                                             account_id="120810601")
                account3 = Integrations_Google_Analytics_Account.objects.get(social_account=self.account,
                                                                             name="Test",
                                                                             account_id="141933286")
                web_property1 = Integrations_Google_Web_Property.objects.get(account=account1,
                                                                             property_id="UA-142018643-1",
                                                                             internal_id="203176700", name="127.0.0.1",
                                                                             website_url="http://127.0.0.1")
                web_property2 = Integrations_Google_Web_Property.objects.get(account=account1,
                                                                             property_id="UA-142018643-2",
                                                                             internal_id="203188923",
                                                                             name="dev blocklight",
                                                                             website_url="https://dev.blocklight.io")
                web_property3 = Integrations_Google_Web_Property.objects.get(account=account2,
                                                                             property_id="UA-120810601-1",
                                                                             internal_id="178618680", name="Blocklight",
                                                                             website_url="https://www.blocklight.io/")
                web_property4 = Integrations_Google_Web_Property.objects.get(account=account3,
                                                                             property_id="UA-141933286-1",
                                                                             internal_id="203051676",
                                                                             name="localBlocklight",
                                                                             website_url="http://127.0.0.1")
                web_property5 = Integrations_Google_Web_Property.objects.get(account=account3,
                                                                             property_id="UA-141933286-2",
                                                                             internal_id="203049413",
                                                                             name="Second property",
                                                                             website_url="http://127.0.0.1")

                self.assertEqual(Integrations_Google_Profile.objects.filter(web_property=web_property1,
                                                                            view_id="196799292",
                                                                            name="All Web Site Data").count(), 1)
                self.assertEqual(Integrations_Google_Profile.objects.filter(web_property=web_property2,
                                                                            view_id="196792021",
                                                                            name="Advertising").count(), 1)
                self.assertEqual(Integrations_Google_Profile.objects.filter(web_property=web_property2,
                                                                            view_id="196844127",
                                                                            name="All Web Site Data").count(), 1)
                self.assertEqual(Integrations_Google_Profile.objects.filter(web_property=web_property3,
                                                                            view_id="177083815",
                                                                            name="All Web Site Data").count(), 1)
                self.assertEqual(Integrations_Google_Profile.objects.filter(web_property=web_property4,
                                                                            view_id="196722831",
                                                                            name="All Web Site Data").count(), 1)
                self.assertEqual(Integrations_Google_Profile.objects.filter(web_property=web_property4,
                                                                            view_id="196720930",
                                                                            name="Second view").count(), 1)
                self.assertEqual(Integrations_Google_Profile.objects.filter(web_property=web_property4,
                                                                            view_id="196759408",
                                                                            name="Third view").count(), 1)
                self.assertEqual(Integrations_Google_Profile.objects.filter(web_property=web_property5,
                                                                            view_id="196761116",
                                                                            name="All Web Site Data").count(), 1)
                profiles = Integrations_Google_Profile.objects.all()
                for profile in profiles:
                    self.assertEqual(profile.time_zone, "America/Chicago")
            except ObjectDoesNotExist:
                self.assert_(True, "Database was not properly populated")

    @tag("Google")
    def test_get_google_account_summaries(self):
        with patch("google.oauth2._client.refresh_grant") as mock_refresh_grant, \
                patch("dashboards.google.initialize_analytics") as mock_initialize:
            set_up_mock_refresh_grant(mock_refresh_grant)
            set_up_mock_initialize_acc_sum(mock_initialize, "dashboards/tests/resources/google/account_summaries.json", "dashboards/tests/resources/google/profile.json")
            query_google_account_summaries(self.account)

        accounts = get_google_account_summaries(self.account)
        for account in accounts:
            for property in account["web_properties"]:
                for profile in property["profiles"]:
                    Integrations_Google_Profile.objects.get(id=profile["id"], name=profile["name"],
                                                            view_id=profile["view_id"]).delete()
                property_obj = Integrations_Google_Web_Property.objects.get(id=property["id"], name=property["name"])
                self.assertEqual(property_obj.integrations_google_profile_set.count(), 0)
                property_obj.delete()
            account_obj = Integrations_Google_Analytics_Account.objects.get(id=account["id"], name=account["name"])
            self.assertEqual(account_obj.integrations_google_web_property_set.count(), 0)
            account_obj.delete()
        self.assertEqual(Integrations_Google_Analytics_Account.objects.count(), 0)
        self.assertEqual(Integrations_Google_Web_Property.objects.count(), 0)
        self.assertEqual(Integrations_Google_Profile.objects.count(), 0)


        self.assertEqual(len(result), len(report["data"]["rows"]))
        rows = report["data"]["rows"]
        for i in range(len(rows)):
            dim = rows[i]["dimensions"][0]
            values = rows[i]["metrics"][0]["values"]
            self.assertEqual(dim, result[i]["ga:pageTitle"])
            self.assertEqual(values[0], result[i]["ga:pageviews"])
            self.assertEqual(values[1], result[i]["ga:uniquePageviews"])
            self.assertEqual(values[2], result[i]["ga:pageviewsPerSession"])
            self.assertEqual(values[3], result[i]["ga:timeOnPage"])
            self.assertEqual(values[4], result[i]["ga:avgTimeOnPage"])
            self.assertEqual(values[5], result[i]["ga:exits"])
            self.assertEqual(values[6], result[i]["ga:exitRate"])

    @tag("Google")
    def test_query_google_profile_info(self):
        analytics = Mock()
        set_up_mock_query_profile(analytics, "dashboards/tests/resources/google/profile.json")

        # Create google accounts first
        account = Integrations_Google_Analytics_Account.objects.create(social_account=self.account,
                                                                       name="Blocklight",
                                                                       account_id="120810601")
        property = Integrations_Google_Web_Property.objects.create(account=account,
                                                                   property_id="UA-120810601-1",
                                                                   internal_id="178618680", name="Blocklight",
                                                                   website_url="https://www.blocklight.io/")
        profile = Integrations_Google_Profile.objects.create(web_property=property,
                                                             view_id="177083815",
                                                             name="All Web Site Data")
        query_google_profile_info(profile.view_id, property.property_id, account.account_id, analytics)

        profile.refresh_from_db()
        self.assertEqual(profile.time_zone, "America/Chicago")


class ReportTestCase(TransactionTestCase):
    fixtures = ["initial_google_token.json"]

    def setUp(self):
        self.user = User.objects.all().first()
        self.token = SocialToken.objects.all().first()
        self.account = self.token.account
        self.analytics_account = Integrations_Google_Analytics_Account.objects.create(social_account=self.account,
                                                                                      name="Blocklight",
                                                                                      account_id="120810601")
        self.property = Integrations_Google_Web_Property.objects.create(account=self.analytics_account,
                                                                        property_id="UA-120810601-1",
                                                                        internal_id="178618680", name="Blocklight",
                                                                        website_url="https://www.blocklight.io/")
        self.profile = Integrations_Google_Profile.objects.create(web_property=self.property,
                                                                  view_id="177083815",
                                                                  name="All Web Site Data")

    @tag("Google")
    def test_build_report_requests_1(self):
        models = [Integrations_Google_Medium]
        requests = build_report_requests(models, self.profile)
        self.assertEqual(len(requests), 1)
        self.assertEqual(requests[0][0]["dimensions"], Integrations_Google_Medium.get_dimensions_used())
        self.assertEqual(requests[0][0]["metrics"], Integrations_Google_Medium.get_metrics_used())
        self.assertEqual(requests[0][0]["dateRanges"][0]["startDate"], "2005-01-01")

    @tag("Google")
    def test_build_report_requests_2(self):
        models = [Integrations_Google_Medium]
        t = timezone.now()
        Integrations_Google_Medium.objects.create(profile=self.profile, last_sync_time=t, datehour=t)
        requests = build_report_requests(models, self.profile)
        self.assertEqual(len(requests), 1)
        self.assertEqual(requests[0][0]["dimensions"], Integrations_Google_Medium.get_dimensions_used())
        self.assertEqual(requests[0][0]["metrics"], Integrations_Google_Medium.get_metrics_used())
        self.assertEqual(requests[0][0]["dateRanges"][0]["startDate"], t.strftime("%Y-%m-%d"))

    @tag("Google")
    def test_build_report_requests_3(self):
        models = [Integrations_Google_Medium]
        time1 = timezone.now()
        time2 = time1 + timedelta(days=365)
        Integrations_Google_Medium.objects.create(profile=self.profile, last_sync_time=time1, datehour=time1)
        Integrations_Google_Medium.objects.create(profile=self.profile, last_sync_time=time1, datehour=time2)
        requests = build_report_requests(models, self.profile)
        self.assertEqual(len(requests), 1)
        self.assertEqual(requests[0][0]["dimensions"], Integrations_Google_Medium.get_dimensions_used())
        self.assertEqual(requests[0][0]["metrics"], Integrations_Google_Medium.get_metrics_used())
        self.assertEqual(requests[0][0]["dateRanges"][0]["startDate"], time2.strftime("%Y-%m-%d"))

    @tag("Google")
    def test_build_report_requests_4(self):
        models = [Integrations_Google_Website_Total]
        time1 = timezone.now()
        Integrations_Google_Website_Total.objects.create(profile=self.profile, last_sync_time=time1, datehour=time1)
        requests = build_report_requests(models, self.profile)
        self.assertEqual(len(requests), 1)
        self.assertEqual(requests[0][0]["dimensions"], Integrations_Google_Website_Total.get_dimensions_used())
        self.assertEqual(requests[0][0]["dateRanges"][0]["startDate"], time1.strftime("%Y-%m-%d"))

    @tag("Google")
    def test_build_report_requests_5(self):
        models = [Integrations_Google_Website_Total, Integrations_Google_Medium]
        time1 = timezone.now()
        time2 = time1 + timedelta(days=365)
        Integrations_Google_Website_Total.objects.create(profile=self.profile, last_sync_time=time1, datehour=time1)
        Integrations_Google_Medium.objects.create(profile=self.profile, last_sync_time=time1, datehour=time2)
        requests = build_report_requests(models, self.profile)
        self.assertEqual(len(requests), 2)

    @tag("Google")
    def test_group_reports_1(self):
        models = [Integrations_Google_Website_Total]
        requests = build_report_requests(models, self.profile)
        grouped_requests = group_reports(requests)
        self.assertEqual(len(grouped_requests.keys()), 1)
        key = requests[0][0]["dateRanges"][0]["startDate"] + "to" + requests[0][0]["dateRanges"][0]["endDate"]
        self.assertEqual(len(grouped_requests[key]), 1)

    @tag("Google")
    def test_group_reports_2(self):
        models = [Integrations_Google_Website_Total, Integrations_Google_Medium, Integrations_Google_Source]
        requests = build_report_requests(models, self.profile)
        grouped_requests = group_reports(requests)
        self.assertEqual(len(grouped_requests.keys()), 1)
        key = requests[0][0]["dateRanges"][0]["startDate"] + "to" + requests[0][0]["dateRanges"][0]["endDate"]
        self.assertEqual(len(grouped_requests[key]), 3)

    @tag("Google")
    def test_group_reports_3(self):
        models = [Integrations_Google_Website_Total, Integrations_Google_Medium, Integrations_Google_Source]
        t = timezone.now()
        Integrations_Google_Medium.objects.create(profile=self.profile, last_sync_time=t, datehour=t)
        requests = build_report_requests(models, self.profile)
        grouped_requests = group_reports(requests)
        self.assertEqual(len(grouped_requests.keys()), 2)
        key1 = "2005-01-01totoday"
        key2 = t.strftime("%Y-%m-%d") + "totoday"
        self.assertEqual(len(grouped_requests[key1]), 2)
        self.assertEqual(len(grouped_requests[key2]), 1)


class TestBatchReports(TransactionTestCase):
    fixtures = ["initial_google_token.json"]

    def setUp(self):
        self.user = User.objects.all().first()
        self.token = SocialToken.objects.all().first()
        self.account = self.token.account
        self.analytics_account = Integrations_Google_Analytics_Account.objects.create(social_account=self.account,
                                                                                      name="Blocklight",
                                                                                      account_id="120810601")
        self.property = Integrations_Google_Web_Property.objects.create(account=self.analytics_account,
                                                                        property_id="UA-120810601-1",
                                                                        internal_id="178618680", name="Blocklight",
                                                                        website_url="https://www.blocklight.io/")
        self.profile = Integrations_Google_Profile.objects.create(web_property=self.property,
                                                                  view_id="177083815",
                                                                  name="All Web Site Data")
        self.analytics = Mock()

    def set_analytics_mock_values(self, json_files):
        def json_load(f):
            with open(f) as fp:
                return json.load(fp)

        self.analytics.reports.return_value.batchGet.return_value.execute.side_effect = map(json_load, json_files)

    @tag("Google")
    def test_get_batch_reports_1(self):
        models = [Integrations_Google_User_Type]
        requests = build_report_requests(models, self.profile)
        self.set_analytics_mock_values(
            ["dashboards/tests/resources/google/usertype.json", "dashboards/tests/resources/google/usertype2.json"])

        reports = get_batch_reports(self.analytics, requests)
        self.assertEqual(len(reports), 2)
        self.assertEqual(len(list(filter(lambda x: x[1] == Integrations_Google_User_Type, reports))), 2)

    @tag("Google")
    def test_get_batch_reports_2(self):
        models = [Integrations_Google_User_Type]
        requests = build_report_requests(models, self.profile)
        self.set_analytics_mock_values(
            ["dashboards/tests/resources/google/usertype2.json"])

        reports = get_batch_reports(self.analytics, requests)
        self.assertEqual(len(reports), 2)
        self.assertEqual(len(list(filter(lambda x: x[1] == Integrations_Google_User_Type, reports))), 2)

    @tag("Google")
    def test_get_batch_reports_3(self):
        models = [Integrations_Google_User_Type, Integrations_Google_Medium]
        requests = build_report_requests(models, self.profile)
        self.set_analytics_mock_values(["dashboards/tests/resources/google/batch_request.json"])

        reports = get_batch_reports(self.analytics, requests)
        self.assertEqual(len(reports), 2)
        self.assertEqual(len(list(filter(lambda x: x[1] == Integrations_Google_User_Type, reports))), 1)
        self.assertEqual(len(list(filter(lambda x: x[1] == Integrations_Google_Medium, reports))), 1)
        self.assertEqual(self.analytics.reports.return_value.batchGet.return_value.execute.call_count, 1)
