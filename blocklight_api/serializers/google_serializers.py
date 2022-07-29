from dashboards.models import (
    Integrations_Google_Analytics_Account, Integrations_Google_Geolocation,
    Integrations_Google_Medium, Integrations_Google_Page_Title,
    Integrations_Google_Profile, Integrations_Google_Social_Network,
    Integrations_Google_Source, Integrations_Google_User_Type,
    Integrations_Google_Web_Property, Integrations_Google_Website_Total,
)

from rest_framework import serializers


class GoogleWebPropertiesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Google_Web_Property
        fields = [
            'account',
            'property_id',
            'internal_id',
            'name',
            'website_url'
        ]


class GoogleProfilesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Google_Profile
        fields = [
            'web_property',
            'view_id',
            'name',
            'time_zone'
        ]


class GoogleAnalyticsAccountsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Google_Analytics_Account
        fields = [
            'name',
            'account_id',


        ]


class GoogleGeolocationsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Google_Geolocation
        fields = [
            'profile',
            'user_iden',
            'continent',
            'sub_continent',
            'country',
            'region',
            'city',
            'users'
        ]


class GoogleMediumsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Google_Medium
        fields = [
            'profile',
            'user_iden',
            'medium',
            'users'
        ]


class GooglePageTitlesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Google_Page_Title
        fields = [
            'profile',
            'user_iden',
            'page_views',
            'unique_page_views',
            'time_on_page',
            'exits',
            'sessions',
            'screen_views'
        ]


class GoogleSocialNetworksSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Google_Social_Network
        fields = [
            'profile',
            'user_iden',
            'social_network',
            'users'
        ]


class GoogleSourcesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Google_Source
        fields = [
            'profile',
            'user_iden',
            'source',
            'has_social_referral',
            'users'
        ]


class GoogleUserTypesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Google_User_Type
        fields = [
            'profile',
            'user_iden',
            'user_type',
            'users'
        ]


class GoogleWebsiteTotalsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Integrations_Google_Website_Total
        fields = [
            'profile',
            'user_iden',
            'page_views',
            'unique_page_views',
            'time_on_page',
            'exits',
            'sessions',
            'bounces',
            'hits',
            'screen_views',
            'session_duration'
        ]
