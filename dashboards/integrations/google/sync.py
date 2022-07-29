from __future__ import print_function

from . import google_api
from . import metricsHandler

from allauth.socialaccount.models import SocialAccount
from celery import shared_task
from dashboards.models import Integrations_Google_Profile, UserProfile
from django.contrib.auth.models import User as DjangoUser
from google.auth.exceptions import RefreshError
import logging
from ...enums.CoreEnums import Master_Blocklight_User



def save_google(integration=None, user=None):
    logger = logging.getLogger(__name__)

    if not integration or not user:
        integration, user = GoogleIntegration(), DjangoUser.objects.get(id=Master_Blocklight_User.User_Id)
    print("done")
    print("SYNC - GOOGLE_SYNCWORKER - {}".format(user))
    params = integration.get_params()
    user_iden = user.id
    # Get view ID
    try:
        user_profile = UserProfile.objects.get(user_id=user_iden)
        logger.debug("UserProfile: " + str(user_profile))
    except UserProfile.DoesNotExist as e:
        logger.warn("The userprofile for the user: " + str(user) + " does not exist.")
        raise e
    view_id = user_profile.google_view_id

    if view_id == None or view_id == "":
        raise Exception("user profile id has no view id")

    try:
        profile = Integrations_Google_Profile.objects.get(view_id=view_id)
    except Integrations_Google_Profile.DoesNotExist as e:
        logger.warn("The google profile for the user: " + str(user) + " does not exist.")
        raise e
    # set up credentials and analytics reporting object
    try:
        token = SocialAccount.objects.get(user_id=user_iden, provider="google").socialtoken_set.first()
    except SocialAccount.DoesNotExist as e:
        logger.warn("The Social Account for the user: " + str(user) + " does not exist.")
        raise e
    try:
        credentials = google_api.set_up_google_cred(token)
    except RefreshError as e:
        logger.warn("Google token invalid/expired for user: " + str(user))
        raise e

    analytics = google_api.initialize_analyticsreporting(credentials)
    requests = google_api.build_report_requests(params["models"], profile)
    groups = google_api.group_reports(requests)

    gAcc = SocialAccount.objects.get(provider="google", user_id=user_iden)
    integration_id = gAcc.id
    for start_date, group in groups.items():
        reports = google_api.get_batch_reports(analytics, group)
        for report, model in reports:
            google_mass_sync.apply_async(args=[profile, report, model, integration_id, user_iden])


@shared_task(time_limit=36000, name="google_mass_sync")
def google_mass_sync(profile, report, model,integration_id,user_iden):
    print("SYNC - GOOGLE_MASS - {}".format(profile))
    data = report.get("data", {}).get("rows",[])
    handler = metricsHandler.MetricsHandler(report, integration_id, user_iden,model, profile)
    handler.save_all_objects()
    
    return "success"
