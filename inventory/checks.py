from pathlib import Path

from django.core.checks import Error, register


@register()
def inventory_checks(app_configs, **kwargs):
    errors = []
    if not Path('.env').is_file():
        errors.append(
            Error(
                'No ".env" file found!',
                hint='Create a ".env" file. See README for details',
                id='pyinventory.E001',
            )
        )
    return errors
