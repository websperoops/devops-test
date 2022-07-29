from django.apps import AppConfig


class DjangoUserAccounts(AppConfig):
    name = 'account'


class DashboardsConfig(AppConfig):
    name = 'dashboards'

    def ready(self):
        import dashboards.signals  # noqa
