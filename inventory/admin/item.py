from django.contrib import admin

from inventory.admin.base import BaseUserAdmin
from inventory.models import ItemModel


@admin.register(ItemModel)
class ItemModelAdmin(BaseUserAdmin):
    pass
