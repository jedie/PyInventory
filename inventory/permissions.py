from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from inventory.models import ItemLinkModel, ItemModel, LocationModel


NORMAL_USER_GROUP_NAME = 'normal user'


def get_permissions(*models):
    content_types = []
    for model in models:
        content_types.append(ContentType.objects.get_for_model(model))

    return Permission.objects.filter(content_type__in=content_types)


def get_or_create_normal_user_group():
    return Group.objects.get_or_create(name=NORMAL_USER_GROUP_NAME)


def setup_normal_user_permissions(normal_user_group):
    """
    Setup PyInventory "normal user" permissions
    """
    assert normal_user_group.name == NORMAL_USER_GROUP_NAME
    permissions = get_permissions(ItemModel, ItemLinkModel, LocationModel)
    existing_permissions = normal_user_group.permissions.all()

    if set(permissions) != set(existing_permissions):
        normal_user_group.permissions.set(permissions)
        return True

    return False
