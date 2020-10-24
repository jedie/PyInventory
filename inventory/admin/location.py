from django.contrib import admin
from import_export.admin import ImportExportMixin
from import_export.resources import ModelResource

from inventory.admin.base import BaseUserAdmin
from inventory.forms import LocationModelModelForm
from inventory.models import LocationModel


class LocationModelResource(ModelResource):

    class Meta:
        model = LocationModel


@admin.register(LocationModel)
class LocationModelAdmin(ImportExportMixin, BaseUserAdmin):
    form = LocationModelModelForm

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if not request.user.is_superuser:
            # Display only own created entries
            qs = qs.filter(user=request.user)

        return qs
