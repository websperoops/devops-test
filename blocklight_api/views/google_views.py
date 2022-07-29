from .base_views import BaseDatasourceViewSet
from blocklight_api.serializers import google_serializers
from blocklight_api.serializers.core_serializers import ChartDataSerializer

from dashboards.models import (
    Integrations_Google_Analytics_Account, Integrations_Google_Geolocation,
    Integrations_Google_Medium, Integrations_Google_Page_Title,
    Integrations_Google_Profile, Integrations_Google_Social_Network,
    Integrations_Google_Source, Integrations_Google_User_Type,
    Integrations_Google_Web_Property, Integrations_Google_Website_Total,
)


class GoogleAnalyticsAccountsViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Google_Analytics_Account.objects.all()
    serializer_class = google_serializers.GoogleAnalyticsAccountsSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'social_account__user_id'
    since_until_field = 'datehour'


class GoogleWebPropertiesViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Google_Web_Property.objects.all()
    serializer_class = google_serializers.GoogleWebPropertiesSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'account__social_account__user_id'
    since_until_field = 'datehour'


class GoogleProfilesViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Google_Profile.objects.all()
    serializer_class = google_serializers.GoogleProfilesSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'web_property__account__social_account__user_id'
    since_until_field = 'datehour'


class GoogleGeolocationsViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Google_Geolocation.objects.all()
    serializer_class = google_serializers.GoogleGeolocationsSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'datehour'


class GoogleMediumsViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Google_Medium.objects.all()
    serializer_class = google_serializers.GoogleMediumsSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'datehour'


class GooglePageTitlesViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Google_Page_Title.objects.all()
    serializer_class = google_serializers.GooglePageTitlesSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'datehour'


class GoogleSocialNetworksViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Google_Social_Network.objects.all()
    serializer_class = google_serializers.GoogleSocialNetworksSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'datehour'


class GoogleSourcesViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Google_Source.objects.all()
    serializer_class = google_serializers.GoogleSourcesSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'datehour'


class GoogleUserTypesViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Google_User_Type.objects.all()
    serializer_class = google_serializers.GoogleUserTypesSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'datehour'


class GoogleWebsiteTotalsViewSet(BaseDatasourceViewSet):
    queryset = Integrations_Google_Website_Total.objects.all()
    serializer_class = google_serializers.GoogleWebsiteTotalsSerializer
    chart_data_serializer = ChartDataSerializer
    owner_field_reference = 'user_iden'
    since_until_field = 'datehour'
