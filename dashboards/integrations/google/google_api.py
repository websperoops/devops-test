from datetime import timedelta
from django.utils import timezone

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from dashboards.models import Integrations_Google_Analytics_Account, Integrations_Google_Web_Property, Integrations_Google_Profile
import logging
import pprint


logger = logging.getLogger(__name__)


def initialize_analytics(credentials):
    """
    Initialize a resource for Google Analytics API v3

    Args:
        credentials: An instance of oogle.oauth2.credentials.Credentials or something similar. Just to authorize the resource

    Returns:
        A Resource for interacting with Google analytics API v3.
    """
    analytics = build('analytics', 'v3', credentials=credentials)
    return analytics


def initialize_analyticsreporting(credentials):
    """
    Initializes an Analytics Reporting API V4 Resource object.

    Args:
        credentials: An instance of google.oauth2.credentials.Credentials or something similar. Just to authorize the resource

    Returns:
        An authorized Analytics Reporting API V4 service object.
    """
    analytics_reporting = build(
        'analyticsreporting', 'v4', credentials=credentials, cache_discovery=False)
    return analytics_reporting


def build_report_requests(models, profile):
    """
    Given a list of models, generates a list of report request corresponding to each model for syncing purposes
    Args:
        models: A list of Integrations_Google_Metric models
        profile: An instance of Integration_Google_Profile

    Returns:
        A list of (report request dict, model)
    """

    requests = []
    for model in models:
        # figure out the start data
        # first time a metric is getting data
        if model.objects.filter(profile=profile).count() == 0:
            start_date = "2005-01-01"  # earliest time possible in google analytics
        else:
            # Converting time to reflect PST as Google Analytics is on PST timezone
            start_date = model.objects.latest(
                'datehour').datehour - timedelta(hours=8)
            start_date = start_date.strftime("%Y-%m-%d")
        metrics = model.get_metrics_used()
        dimensions = model.get_dimensions_used()
        # Google only supports up to 10 metrics per report, so we loop by 10
        for i in range(0, len(metrics), 10):
            report_request = {
                'viewId': profile.view_id,
                "dateRanges": [{
                    "startDate": start_date,
                    "endDate": "today"
                }],
                "metrics": metrics[i:i + 10],
                "dimensions": dimensions,
                "samplingLevel": "LARGE",
                "pageSize": 10000,
                "orderBys": [
                    {
                        "fieldName": "ga:dateHour",
                        "sortOrder": "ASCENDING"
                    }
                ],
                "hideTotals": True
            }
            requests.append((report_request, model))
    return requests


def group_reports(requests):
    """
    Groups reports with similar data ranges, allowing them to be used together in batchGet
    Args:
        requests: a list of (report request dict, model) tuples

    Returns:
        A dict with key in form of "<startDate>to<endDate>" and value of a list of report requests
    """
    # seperate reports by date ranges
    date_range_reports = {}
    for request in requests:
        key = request[0]["dateRanges"][0]["startDate"] + \
            "to" + request[0]["dateRanges"][0]["endDate"]
        if key in date_range_reports:
            date_range_reports[key].append(request)
        else:
            date_range_reports[key] = [request]
    return date_range_reports


def set_up_google_cred(token):
    """
    Sets up the credentials to use Google APIs. Also will refresh the token if needed. If the token is refreshed, the database will be updated too

    Args:
        token: an instance of the model SocialToken from allauth.socialaccount.models. Token should correspond to the Google social app

    Returns:
        An instance of oauth2client.client.GoogleCredentials
    """
    # need to convert to a naive datetime object
    expire = token.expires_at.replace(tzinfo=None)
    credentials = Credentials(token=token.token, refresh_token=token.token_secret, client_id=token.app.client_id,
                              client_secret=token.app.secret, token_uri="https://oauth2.googleapis.com/token")
    credentials.expiry = expire

    # check if the token needs to be refreshed
    if credentials.expired:
        request = Request()
        credentials.refresh(request)
        logger.info("Refreshed Google access token")
        # update the db
        token.token = credentials.token
        token.expires_at = credentials.expiry.replace(tzinfo=timezone.utc)
        token.save()

    return credentials


def get_batch_reports(analytics, report_requests):
    """
        Gets multiple reports using reports.batchGet (google analytics reporting v4)
    Args:
        analytics: An analytics report v4 resource object
        report_requests: a list of (report request dict, model) tuple, all with the same dateRanges

    Returns:
        A list of (reports, model) tuples
    """
    reports = []
    requests = report_requests.copy()
    while requests:
        i = 0
        batch = []
        while requests and i < 5:
            batch.append(requests.pop(0))
            i = i + 1
        body = {
            "reportRequests": [request for request, model in batch]
        }
        try:
            response = analytics.reports().batchGet(body=body).execute()
            for j, report in enumerate(response["reports"]):
                if "nextPageToken" in report:  # need to request again to get remaining information
                    newRequest, model = batch[j]
                    newRequest["pageToken"] = report["nextPageToken"]
                    requests.append((newRequest, model))

                reports.append((report, batch[j][1]))
        except Exception as e:
            logger.error(
                f"Google analytics batch get failed.\nRequest: {pprint.pformat(body)},\nexception: {e}")
            raise e
    return reports


def query_google_profile_info(view_id, web_property_id, account_id, analytics):
    """
        Retrives more information about a profile using Google API
    Args:
        view_id:
        web_property_id:
        account_id:
        analytics: A Google Analytics API v3 resource object
    Returns:
    """
    profile_info = analytics.management().profiles().get(accountId=account_id, webPropertyId=web_property_id,
                                                         profileId=view_id).execute()
    analytics_account = Integrations_Google_Analytics_Account.objects.get(
        account_id=account_id)
    web_property = analytics_account.integrations_google_web_property_set.get(
        property_id=web_property_id)
    profile = web_property.integrations_google_profile_set.get(view_id=view_id)
    profile.time_zone = profile_info["timezone"]
    profile.save()
    pass


def query_google_account_summaries(social_account):
    """
        Given a Google social account (with a valid token), retrieves a summary of all accounts, properties and profiles
        and stores them in the database
    Args:
        social_account: A allauth.socialaccount.models.SocialAccount instance with provider as "google"
    Returns:
    """
    token = social_account.socialtoken_set.all().first()
    creds = set_up_google_cred(token)
    analytics = initialize_analytics(creds)
    # get account summaries list using Google Analytics Management API
    account_summaries = analytics.management().accountSummaries().list().execute()
    for account in account_summaries["items"]:
        analytics_account, created = Integrations_Google_Analytics_Account.objects.get_or_create(
            social_account=social_account,
            account_id=account["id"])
        analytics_account.name = account["name"]
        analytics_account.save()
        for wprop in account["webProperties"]:
            web_property, created = Integrations_Google_Web_Property.objects.get_or_create(account=analytics_account,
                                                                                           internal_id=wprop[
                                                                                               "internalWebPropertyId"],
                                                                                           property_id=wprop["id"])
            web_property.name = wprop["name"]
            web_property.website_url = wprop["websiteUrl"]
            web_property.save()
            for view in wprop["profiles"]:
                profile, created = Integrations_Google_Profile.objects.get_or_create(web_property=web_property,
                                                                                     view_id=view["id"])
                profile.name = view["name"]
                profile.save()
                query_google_profile_info(profile.view_id, web_property.property_id, analytics_account.account_id,
                                          analytics)


def get_google_account_summaries(social_account):
    """
    Get the account summaries associated with a particular social account
    Args:
        social_account: A allauth.socialaccount.models.SocialAccount instance with provider as "google"
    Returns:
        A list of dictionaries. The account dictionary has keys of "name" and "id", "web_properties". The web property dict
        has the keys "id", "name" and "profiles". The profile dict has the keys "view_id", "id" and "name"
    """
    summaries = []
    accounts = Integrations_Google_Analytics_Account.objects.filter(
        social_account=social_account)
    for account in accounts:
        acc = {"name": account.name, "web_properties": [], "id": account.id}
        properties = Integrations_Google_Web_Property.objects.filter(
            account=account)
        for web_property in properties:
            prop = {"name": web_property.name,
                    "profiles": [], "id": web_property.id}
            profiles = Integrations_Google_Profile.objects.filter(
                web_property=web_property)
            for profile in profiles:
                prof = {"name": profile.name,
                        "view_id": profile.view_id, "id": profile.id}
                prop["profiles"].append(prof)
            acc["web_properties"].append(prop)
        summaries.append(acc)
    return summaries
