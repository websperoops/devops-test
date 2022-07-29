from ...integrations.integration import Integration
from . import sync

from allauth.socialaccount.models import SocialAccount
from celery import shared_task

from ...enums.CoreEnums import Master_Blocklight_User


from dashboards.integrations.utils.dashboard_sync_complete import dashboard_sync_complete
from dashboards.models import Integrations_Google_Social_Network, Integrations_Google_Page_Title, \
    Integrations_Google_User_Type, Integrations_Google_Website_Total, Integrations_Google_Geolocation, \
    Integrations_Google_Medium, Integrations_Google_Source

from django.contrib.auth.models import User as DjangoUser


class GoogleIntegration(Integration):

    # TODO: correct logging and move it up
    def get_task(self, user):
        task = initialize_google_syncworker_task
        tcount = SocialAccount.objects.filter(provider='google', user_id=user.id).count()
        return task, tcount

    def get_params(self):
        """
        Returns: A dictionary with a list of models, start times and end time

        """
        standard_times = ['yesterday', '7daysAgo', '30daysAgo', '90daysAgo', '180daysAgo', '365daysAgo']
        end_date = "today"
        models = [Integrations_Google_Medium, Integrations_Google_Source, Integrations_Google_Social_Network,
                  Integrations_Google_Page_Title, Integrations_Google_User_Type, Integrations_Google_Website_Total,
                  Integrations_Google_Geolocation]
        return {"models": models, "start_times": standard_times, "end_date": end_date}

    def set_sync_state(self, user_id, integration_name, celery_id):
        return super().set_sync_state(user_id, integration_name, celery_id)

    def build_auth_params(self, integration_name, user):
        return super().build_auth_params(integration_name, user)


@shared_task(time_limit=36000, name="initialize_google_syncworker_task")
def initialize_google_syncworker_task(integration=None, user=None):
    if not integration or not user:
        integration, user = GoogleIntegration(), DjangoUser.objects.get(id=Master_Blocklight_User.User_Id)
    task_id = initialize_google_syncworker_task.request.id
    integration.set_sync_state(user.id, 'google', task_id)
    dashboard_sync_complete('google', user.id)

    return sync.save_google(integration, user)
