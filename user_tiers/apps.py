from django.apps import AppConfig


class UserTiersConfig(AppConfig):
    name = 'user_tiers'

    def ready(self):
        import user_tiers.signals  # noqa