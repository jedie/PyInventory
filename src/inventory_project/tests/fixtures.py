from django.contrib.auth.models import User
from model_bakery import baker

from inventory.permissions import get_or_create_normal_user_group


def get_normal_user():
    user = baker.make(
        User,
        id=1,
        username='NormalUser',
        is_staff=True,
        is_active=True,
        is_superuser=False,
    )
    assert user.user_permissions.count() == 0
    group = get_or_create_normal_user_group()[0]
    user.groups.set([group])
    user.full_clean()
    return user
