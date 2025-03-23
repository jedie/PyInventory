from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):
    name = 'inventory'
    verbose_name = 'Inventory'

    def ready(self):
        import inventory.checks  # noqa
        import inventory.signals  # noqa
