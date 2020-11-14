"""
    https://docs.djangoproject.com/en/2.0/ref/applications/#configuring-applications-ref

    created 14.20.2020 by Jens Diemer <opensource@jensdiemer.de>
    :copyleft: 2020 by the PyInventory team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""


from django.apps import AppConfig


class InventoryConfig(AppConfig):
    name = "inventory"
    verbose_name = "Inventory"

    def ready(self):
        import inventory.signals  # noqa
