from django.contrib import admin

from inventory.admin.base import BaseUserAdmin
from inventory.models import LocationModel


@admin.register(LocationModel)
class LocationModelAdmin(BaseUserAdmin):
    pass
