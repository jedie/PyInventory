from django.contrib import admin
from import_export.admin import ImportExportMixin
from import_export.resources import ModelResource

from inventory.admin.base import BaseUserAdmin
from inventory.models import LocationModel


class LocationModelResource(ModelResource):

    class Meta:
        model = LocationModel


@admin.register(LocationModel)
class LocationModelAdmin(ImportExportMixin, BaseUserAdmin):
    pass
