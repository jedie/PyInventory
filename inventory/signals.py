from django.db.models.signals import post_migrate
from django.dispatch import receiver

from inventory.permissions import get_or_create_normal_user_group, setup_normal_user_permissions


@receiver(post_migrate)
def post_migrate_callback(sender, **kwargs):
    normal_user_group, created = get_or_create_normal_user_group()
    if created:
        print(f'User group {normal_user_group} created')

    updated = setup_normal_user_permissions(normal_user_group)
    if updated:
        print(f'Update permissions for {normal_user_group}')
