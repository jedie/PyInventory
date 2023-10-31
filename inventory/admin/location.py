from django.conf import settings
from django.contrib import admin
from django.db.models import Count
from django.db.models.options import Options
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportMixin
from import_export.resources import ModelResource

from inventory.admin.base import BaseUserAdmin, LimitTreeDepthListFilter
from inventory.models import ItemModel, LocationModel
from inventory.string_utils import ltruncatechars


class LocationModelResource(ModelResource):
    class Meta:
        model = LocationModel


@admin.register(LocationModel)
class LocationModelAdmin(ImportExportMixin, BaseUserAdmin):
    @admin.display(ordering='item_count', description=_('ItemModel.verbose_name_plural'))
    def item_count(self, obj):
        return obj.item_count

    @admin.display(description=_('ItemModel.verbose_name_plural'))
    def items(self, obj):
        item_qs = ItemModel.objects.filter(location=obj)
        opts: Options = ItemModel._meta
        context = {
            'items': item_qs,
            'opts': opts,
        }
        return render_to_string('admin/location/items.html', context)

    @admin.display(ordering='path_str', description=_('LocationModel.verbose_name'))
    def location(self, obj):
        text = ' › '.join(obj.path)
        text = ltruncatechars(text, max_length=settings.TREE_PATH_STR_MAX_LENGTH)
        return text

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(item_count=Count('items'))
        return qs

    list_display = ('location', 'create_dt', 'update_dt', 'item_count')
    fieldsets = (
        (
            _('Internals'),
            {
                'classes': ('collapse',),
                'fields': (
                    ('id', 'version'),
                    'user',
                ),
            },
        ),
        (_('Meta'), {'classes': ('collapse',), 'fields': ('create_dt', 'update_dt')}),
        (
            _('Basic'),
            {
                'fields': (
                    'name',
                    'description',
                    'tags',
                    'parent',
                )
            },
        ),
        (_('Items in this Location'), {'fields': ('items',)}),
    )
    readonly_fields = ('id', 'create_dt', 'update_dt', 'user', 'item_count', 'items')
    list_display_links = ('location',)
    list_filter = (LimitTreeDepthListFilter,)
    search_fields = ('name', 'description', 'tags__name')
    ordering = ('path_str',)
