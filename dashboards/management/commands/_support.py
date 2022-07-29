from dashboards.models import Integrations_Shopify_Product, Integrations_Shopify_Customer, Integrations_Shopify_Order, \
    Integrations_Shopify_Abandoned_Checkouts, Integrations_Shopify_Shop_Price_Rule, Integrations_Shopify_Refund, \
    Integrations_Shopify_Shop, Integrations_Google_Source, Integrations_Google_Medium, Integrations_Google_Page_Title, \
    Integrations_Google_Website_Total, Integrations_Google_Geolocation, Integrations_Google_Social_Network, \
    Integrations_Google_User_Type, UserProfile, Integrations_Google_Profile, Integrations_Instagram_Media_Objects, \
    Integrations_InstagramInsights_Impressions, Integrations_InstagramInsights_Reach, Integrations_InstagramInsights_Followers, \
    Integrations_Facebook_Page_Posts, Integrations_FacebookInsights_Views, Integrations_FacebookInsights_Impressions, \
    Integrations_FacebookInsights_Engagements, Integrations_FacebookInsights_Reactions, Integrations_FacebookInsights_Demographics, \
    Integrations_FacebookInsights_Posts, Integrations_Etsy_Listing, Integrations_Etsy_Receipt, Integrations_Etsy_Transaction, \
    Integrations_Etsy_Ledger, Integrations_Etsy_User, Integrations_Etsy_Shop, Integrations_Quickbooks_Company_Info, \
    Integrations_Quickbooks_Bills, Integrations_Quickbooks_Ledger_Reports, Integrations_Quickbooks_Account_Info

from django.contrib.auth.models import User
from django.db.models import Q


def print_deleted(wrapper, output, user):
    for table, count in output.items():
        if count > 0:
            wrapper.write(f"Deleted {count} row(s) in table {table} for user {user.id}")


def clear_shopify_data(integration, user, out_wrapper, verbosity):
    # first clear out entries in the db
    models = [Integrations_Shopify_Product, Integrations_Shopify_Customer, Integrations_Shopify_Order, Integrations_Shopify_Abandoned_Checkouts,
    Integrations_Shopify_Shop_Price_Rule, Integrations_Shopify_Refund, Integrations_Shopify_Shop]

    for model in models:
        output = model.objects.filter(integration=integration).delete()
        if verbosity >= 2:
            print_deleted(out_wrapper, output[1], user)


def clear_facebook_data(integration, user, out_wrapper, verbosity):
    models = [Integrations_Facebook_Page_Posts, Integrations_FacebookInsights_Views, Integrations_FacebookInsights_Impressions,
        Integrations_FacebookInsights_Engagements, Integrations_FacebookInsights_Reactions, Integrations_FacebookInsights_Demographics, Integrations_FacebookInsights_Posts]

    for model in models:
         output = model.objects.filter(integration=integration).delete()
         if verbosity >= 2:
             print_deleted(out_wrapper, output[1], user)


def clear_instagram_data(integration, user, out_wrapper, verbosity):
    models = [Integrations_Instagram_Media_Objects, Integrations_InstagramInsights_Impressions, Integrations_InstagramInsights_Reach,
    Integrations_InstagramInsights_Followers]

    for model in models:
         output = model.objects.filter(integration=integration).delete()
         if verbosity >= 2:
             print_deleted(out_wrapper, output[1], user)


def clear_etsy_data(integration, user, out_wapper, verbosity):
    models = [Integrations_Etsy_Listing, Integrations_Etsy_Receipt, Integrations_Etsy_Transaction, Integrations_Etsy_Ledger,
        Integrations_Etsy_User, Integrations_Etsy_Shop]

    for model in models:
         output = model.objects.filter(integration=integration).delete()
         if verbosity >= 2:
             print_deleted(out_wrapper, output[1], user)


def clear_quickbooks_data(integration, user, out_wapper, verbosity):
    models = [Integrations_Quickbooks_Company_Info, Integrations_Quickbooks_Bills, Integrations_Quickbooks_Ledger_Reports, Integrations_Quickbooks_Account_Info]

    for model in models:
         output = model.objects.filter(integration=integration).delete()
         if verbosity >= 2:
             print_deleted(out_wrapper, output[1], user)


def clear_google_data(integration, user, out_wrapper, verbosity):
    models = [Integrations_Google_Source, Integrations_Google_Medium, Integrations_Google_Page_Title,
              Integrations_Google_Website_Total, Integrations_Google_Geolocation,
              Integrations_Google_Social_Network, Integrations_Google_User_Type]

    user_profile = UserProfile.objects.get(user_id=user.id)
    if user_profile.google_view_id is None or user_profile.google_view_id == "":
        out_wrapper.write(f"There was no google view id selected for user {user.id}")
        return
    else:
        view_id = user_profile.google_view_id
        social_query = Q(web_property__account__social_account=integration)
        id_query = Q(view_id=view_id)
        profile = Integrations_Google_Profile.objects.get(social_query & id_query)
    for model in models:
        output = model.objects.filter(profile=profile).delete()
        if verbosity >= 2:
            print_deleted(out_wrapper, output[1], user)


def parse_options_user(options):
    if options["users"] is None:
        users = User.objects.all()
    else:
        users = User.objects.filter(id__in=options["users"])
    return users


def parse_options_integrations(options):
    if options["integrations"] is None:
        integrations = ["google", "shopify", "mailchimp", "facebook", "instagram"]
    else:
        integrations = options["integrations"]
    return integrations


integrations_functions = {
    "shopify": {
        "clear": clear_shopify_data
    },

    "google": {
        "clear": clear_google_data
    },

    "facebook":{
        "clear":clear_facebook_data
    },

    "instagram":{
        "clear":clear_instagram_data
    },

    "etsy":{
        "clear":clear_etsy_data
    },
    "quickbooks":{
        "clear":clear_quickbooks_data
    }
}
