from django.conf import settings

import google.auth.transport.requests
import google.oauth2.credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import logging
from oauth2client import GOOGLE_TOKEN_URI, client
from rest_framework.exceptions import APIException


logger = logging.getLogger(__name__)


CLIENT_SECRET_FILE = "dev-web-google-client.json"
DISCOVERY_URI = ('https://analyticsreporting.googleapis.com/$discovery/rest')


def get_google_api_instance(google_access_token, google_refresh_token):
    return GoogleApiUtils(google_access_token, google_refresh_token)


def get_refresh_token(auth_code):
    # Exchange auth code for access token, refresh token, and ID token
    credentials = client.credentials_from_clientsecrets_and_code(
        CLIENT_SECRET_FILE,
        settings.GOOGLE_SCOPES,
        auth_code)
    return credentials


class GoogleApiUtils():

    def __init__(self, google_access_token, google_refresh_token):
        self.google_access_token = google_access_token
        self.google_refresh_token = google_refresh_token
        self.credentials = None
        self.analytics = None
        self.initialize_google_client()

    def initialize_google_client(self):

        # Initialize user's graph
        try:
            self.credentials = google.oauth2.credentials.Credentials(
                self.google_access_token,
                refresh_token=self.google_refresh_token,
                token_uri=GOOGLE_TOKEN_URI,
                client_id=settings.GOOGLE_CLIENT_ID,
                client_secret=settings.GOOGLE_CLIENT_SECRET)

            # request = google.auth.transport.requests.Request()
            # self.credentials = self.credentials.refresh(request)

            # Build the service object.
            self.analytics = build('analyticsreporting', 'v4', credentials=self.credentials)
            # self.analyticsv3 = build('analytics', 'v3', credentials=self.credentials)

        except Exception as e:
            print(e)
            # logger.error("Failed to initialize google graph", extra={
            #     'extra': {'access_token': self.google_refresh_token}},
            #              exc_info=True)
            raise APIException()


    def get_all_analytics_accounts(self):

        try:
            accounts = self.analyticsv3.management().accounts().list().execute()
            return True, accounts
        except TypeError as error:
            # Handle errors in constructing a query.
            # logger.error("error while fetching analytics accounts", extra={
            #     'extra': {'access_token': self.google_refresh_token}},
            #              exc_info=True)
            return False, 'There was an error in constructing your query'

        except HttpError as error:
            # Handle API errors.
            # logger.error("Https error while fetching analytics accounts", extra={
            #     'extra': {'access_token': self.google_refresh_token}},
            #              exc_info=True)
            return False, 'There was an API error'




