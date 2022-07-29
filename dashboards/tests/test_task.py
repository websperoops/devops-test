from allauth.socialaccount.models import SocialToken

from dashboards.models import Integrations_Google_Medium, Integrations_Google_Source, \
    Integrations_Google_Social_Network, Integrations_Google_User_Type, Integrations_Google_Page_Title, \
    Integrations_Google_Website_Total, Integrations_Google_Profile, Integrations_Google_Web_Property, \
    Integrations_Google_Analytics_Account, UserProfile

from dashboards.tasks import initialize_google_syncworker_task
from dashboards.tests.test_google import set_up_mock_refresh_grant

from django.contrib.auth.models import User
from django.test import TransactionTestCase, tag

import json
import logging
from unittest.mock import patch, Mock, MagicMock


logger = logging.getLogger(__name__)


def mock_batch_get(body):
    reports = []
    for request in body["reportRequests"]:
        dims = request["dimensions"]
        page_token_used = request.get("pageToken", False)
        if dims == Integrations_Google_Medium.get_dimensions_used():
            json_file = "dashboards/tests/resources/google/medium"
        elif dims == Integrations_Google_Source.get_dimensions_used():
            json_file = "dashboards/tests/resources/google/source"
        elif dims == Integrations_Google_Social_Network.get_dimensions_used():
            json_file = "dashboards/tests/resources/google/social_network"
        elif dims == Integrations_Google_User_Type.get_dimensions_used():
            json_file = "dashboards/tests/resources/google/usertype"
        elif dims == Integrations_Google_Page_Title.get_dimensions_used():
            json_file = "dashboards/tests/resources/google/page_title"
        elif dims == Integrations_Google_Website_Total.get_dimensions_used():
            json_file = "dashboards/tests/resources/google/website_total"
        else:
            assert True, "Invalid dimensions ussed"

        if page_token_used:
            json_file = json_file + "2"
        with open(json_file + ".json") as fp:
            d = json.load(fp)
            reports.append(d["reports"][0])

    mock = Mock()
    mock.execute.return_value = {"reports": reports}
    return mock

def set_up_mock_batch_get(analyitcs_mock):
    mock_get = MagicMock(side_effect =mock_batch_get)
    mock_reports = Mock()
    mock_reports.return_value.batchGet = mock_get
    analyitcs_mock.return_value = Mock()
    analyitcs_mock.return_value.reports = mock_reports


def set_up_mock_initialize_acc_sum(mock_obj):
    def side_eff():
        logger.debug("Initialize_acc mock called")

    mock_obj.return_value = side_eff


class GoogleTestCase(TransactionTestCase):
    fixtures = ["initial_google_token.json"]

    def setUp(self):
        self.user = User.objects.first()
        self.token = SocialToken.objects.all().first()
        self.account = self.token.account
        self.analytics_accont = Integrations_Google_Analytics_Account.objects.create(social_account=self.account,
                                                                                     name="Blocklight",
                                                                                     account_id="120810601")
        self.webProperty = Integrations_Google_Web_Property.objects.create(account=self.analytics_accont,
                                                                           property_id="UA-120810601-1",
                                                                           internal_id="178618680", name="Blocklight",
                                                                           website_url="https://www.blocklight.io/")
        self.profile = Integrations_Google_Profile.objects.create(web_property=self.webProperty, view_id="177083815",
                                                                  name="All Web Site Data")
        self.userprofile = UserProfile.objects.create(user_id=self.user.id, google_view_id=self.profile.view_id)

    @tag("Google", "Sync", "Task")
    @patch("google.oauth2._client.refresh_grant")
    @patch("dashboards.tasks.initialize_analyticsreporting")
    def test_intialize_google_task(self, mock_reporting, mock_refresh_grant):
        set_up_mock_refresh_grant(mock_refresh_grant)
        set_up_mock_batch_get(mock_reporting)
        request = {'user': {'id': self.user.id}}
        initialize_google_syncworker_task(request, self.user, "I don't think the url matters")

        self.assertEqual(Integrations_Google_Medium.objects.count(), 20)
        self.assertEqual(Integrations_Google_User_Type.objects.count(), 20)
        self.assertEqual(Integrations_Google_Source.objects.count(), 20)
        self.assertEqual(Integrations_Google_Social_Network.objects.count(), 20)
        self.assertEqual(Integrations_Google_Website_Total.objects.count(), 20)
        self.assertEqual(Integrations_Google_Page_Title.objects.count(), 20)


