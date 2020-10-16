from django.contrib import admin
from reversion_compare.admin import CompareVersionAdmin

from inventory.models import ItemModel


@admin.register(ItemModel)
class ItemModelAdmin(CompareVersionAdmin):
    pass
