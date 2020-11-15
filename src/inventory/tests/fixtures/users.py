from django.contrib.auth.models import User
from model_bakery import baker

from inventory.permissions import get_or_create_normal_user_group


def get_normal_pyinventory_user(**baker_kwargs):
    pyinventory_user_group = get_or_create_normal_user_group()[0]
    pyinventory_user = baker.make(
        User,
        is_staff=True, is_active=True, is_superuser=False,
        **baker_kwargs
    )
    pyinventory_user.groups.set([pyinventory_user_group])
    return pyinventory_user
