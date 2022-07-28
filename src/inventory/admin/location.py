from django.conf import settings
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportMixin
from import_export.resources import ModelResource

from inventory.admin.base import BaseUserAdmin, LimitTreeDepthListFilter
from inventory.models import LocationModel
from inventory.string_utils import ltruncatechars


class LocationModelResource(ModelResource):

    class Meta:
        model = LocationModel


@admin.register(LocationModel)
class LocationModelAdmin(ImportExportMixin, BaseUserAdmin):
    @admin.display(ordering='path_str', description=_('LocationModel.verbose_name'))
    def location(self, obj):
        text = ' › '.join(obj.path)
        text = ltruncatechars(text, max_length=settings.TREE_PATH_STR_MAX_LENGTH)
        return text

    list_display = ('location', 'create_dt', 'update_dt')
    list_display_links = ('location',)
    list_filter = (LimitTreeDepthListFilter,)
    ordering = ('path_str',)
