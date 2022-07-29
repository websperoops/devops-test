from ._support import integrations_functions, parse_options_integrations, parse_options_user
from allauth.socialaccount.models import SocialAccount

from django.core.management.base import BaseCommand
from django.db.models import Q


class Command(BaseCommand):
    help = "Clear out all the integration data. Example usage:" + \
           "\"python manage.py clear -verbosity=2 -u 26 -i google\" will clear user 26's google data"




    def handle(self, *args, **options):

        if options["users"] is None:
            confirmation = input("Are you sure want to clear all user data? [YES/no]: ")
            if confirmation != "YES":
                return

        users = parse_options_user(options)
        integrations = parse_options_integrations(options)
        for user in users:
            user_query = Q(user_id=user.id)
            provider_query = Q(provider__in=integrations)
            accounts = SocialAccount.objects.filter(user_query & provider_query)
            for integration in accounts:
                clear_func = integrations_functions[integration.provider]["clear"]
                clear_func(integration, user, self.stdout, options["verbosity"])
                self.stdout.write(self.style.SUCCESS(f"Cleared {integration.provider} data for user {user.id}"))
        pass


    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('-u', nargs='+', type=int, help="ID(s) for user(s) to sync", dest="users")
        parser.add_argument('-i', nargs='+', type=str, help="Integrations to sync", dest="integrations")
