import logging

import tagulous
from adminsortable2.admin import SortableInlineAdminMixin
from django.conf import settings
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportMixin
from import_export.resources import ModelResource

from inventory.admin.base import (
    BaseFileModelInline,
    BaseImageModelInline,
    BaseUserAdmin,
    LimitTreeDepthListFilter,
    UserInlineMixin,
)
from inventory.models import ItemLinkModel, ItemModel
from inventory.models.item import ItemFileModel, ItemImageModel
from inventory.string_utils import ltruncatechars


logger = logging.getLogger(__name__)


class ItemLinkModelInline(UserInlineMixin, SortableInlineAdminMixin, admin.TabularInline):
    model = ItemLinkModel
    extra = 0


class ItemImageModelInline(BaseImageModelInline):
    model = ItemImageModel


class ItemFileModelInline(BaseFileModelInline):
    model = ItemFileModel


class ItemModelResource(ModelResource):
    class Meta:
        model = ItemModel


@admin.register(ItemModel)
class ItemModelAdmin(ImportExportMixin, BaseUserAdmin):
    @admin.display(ordering='path_str', description=_('ItemModel.verbose_name'))
    def item(self, obj):
        path = obj.path
        if len(path) > 1:
            prefixes = ' › '.join(path[:-1] + [''])
            prefixes = ltruncatechars(prefixes, max_length=settings.TREE_PATH_STR_MAX_LENGTH)
        else:
            prefixes = ''
        item = path[-1]
        url = reverse('admin:inventory_itemmodel_change', args=[obj.pk])
        return format_html(
            '<a href="{}">{}<strong>{}</strong></a>',
            url,
            prefixes,
            item,
        )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.prefetch_related(
            'location',
            'kind',
            'producer',
        )
        return qs

    date_hierarchy = 'create_dt'
    list_display = ('item', 'kind', 'producer', 'location', 'received_date', 'update_dt')
    ordering = ('path_str',)
    list_display_links = None
    list_filter = (LimitTreeDepthListFilter, 'kind', 'location', 'producer', 'tags')
    search_fields = ('name', 'description', 'kind__name', 'tags__name')
    fieldsets = (
        (_('Internals'), {
            'classes': ('collapse',),
            'fields': (
                ('id', 'version'),
                'user',
            )
        }),
        (_('Meta'), {
            'classes': ('collapse',),
            'fields': (
                'create_dt', 'update_dt'
            )
        }),
        (_('Basic'), {'fields': (
            'kind',
            ('producer', 'name'),
            'description',
            'tags',
            'fcc_id',
            'parent',
            'location',
        )}),
        (_('Lent'), {
            'classes': ('collapse',),
            'fields': (
                'lent_to',
                ('lent_from_date', 'lent_until_date',)
            )}),
        (_('Received'), {
            'classes': ('collapse',),
            'fields': (
                ('received_from', 'received_date', 'received_price'),
            )}),
        (_('Handed over'), {
            'classes': ('collapse',),
            'fields': (
                ('handed_over_to', 'handed_over_date', 'handed_over_price'),
            )}),
    )
    readonly_fields = ('id', 'create_dt', 'update_dt', 'user')
    inlines = (ItemImageModelInline, ItemFileModelInline, ItemLinkModelInline)


tagulous.admin.enhance(ItemModel, ItemModelAdmin)
