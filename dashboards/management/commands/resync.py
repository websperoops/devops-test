from ._support import integrations_functions, parse_options_integrations, parse_options_user
from allauth.socialaccount.models import SocialAccount
from django.core.management.base import BaseCommand
from django.db.models import Q


class Command(BaseCommand):
    help = "Clear out all the integration data and then syncs the data. Example usage:" + \
           "\"python manage.py resync --verbosity=2 -u 26 -i google\" will resync user 26's google data"

    def resync(self, integration, user, verbosity=1):
        """
            Will delete all integration data for the user/integration and then start an celery sync task
        Args:
            integration: the name of the integration. Should correspond to a provider value in the SocialAccount table
            user: an instance of django.contrib.auth.models.User
            verbosity:

        Returns:

        """
        if verbosity >= 2:
            self.stdout.write(f"Resyncing {integration.provider} for user {user.id}")

        clear_func = integrations_functions[integration.provider]["clear"]
        clear_func(integration, user, self.stdout, verbosity)

        user_id = user.id
        req = {'user': {'id': user_id}}
        current_url_is = 'it doesn\'t matter'

        task = integrations_functions[integration.provider]["sync"]
        result = task.apply_async(args=[req, user, current_url_is])
        self.stdout.write(self.style.SUCCESS(f"Started celery task {task.__name__}[{result.id}]"))

    def handle(self, *args, **options):
        users = parse_options_user(options)
        integrations = parse_options_integrations(options)

        for user in users:
            user_query = Q(user_id=user.id)
            provider_query = Q(provider__in=integrations)
            accounts = SocialAccount.objects.filter(user_query & provider_query)
            for account in accounts:
                self.resync(account, user, options["verbosity"])

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('-u', nargs='+', type=int, help="ID(s) for user(s) to sync", dest="users")
        parser.add_argument('-i', nargs='+', type=str, help="Integrations to sync", dest="integrations")
