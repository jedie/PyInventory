from pathlib import Path

from django.core.checks import Error, Warning, register

from inventory.permissions import get_or_create_normal_user_group, setup_normal_user_permissions


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


@register()
def inventory_user_groups(app_configs, **kwargs):
    """
    Setup PyInventory user groups
    """
    warnings = []

    normal_user_group, created = get_or_create_normal_user_group()
    if created:
        warnings.append(
            Warning(f'User group {normal_user_group} created')
        )

    updated = setup_normal_user_permissions(normal_user_group)
    if updated:
        warnings.append(
            Warning(f'Update permissions for {normal_user_group}')
        )

    return warnings
