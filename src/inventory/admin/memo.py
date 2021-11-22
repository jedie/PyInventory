import logging

import tagulous
from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportMixin
from import_export.resources import ModelResource

from inventory.admin.base import BaseFileModelInline, BaseImageModelInline, BaseUserAdmin, UserInlineMixin
from inventory.models import MemoLinkModel, MemoModel
from inventory.models.memo import MemoFileModel, MemoImageModel


logger = logging.getLogger(__name__)


class MemoLinkModelInline(UserInlineMixin, SortableInlineAdminMixin, admin.TabularInline):
    model = MemoLinkModel
    extra = 0


class MemoImageModelInline(BaseImageModelInline):
    model = MemoImageModel


class MemoFileModelInline(BaseFileModelInline):
    model = MemoFileModel


class MemoModelResource(ModelResource):
    class Meta:
        model = MemoModel


@admin.register(MemoModel)
class MemoModelAdmin(ImportExportMixin, BaseUserAdmin):
    date_hierarchy = 'create_dt'
    list_display = (
        'name', 'update_dt'
    )
    ordering = ('-update_dt',)
    list_display_links = ('name',)
    list_filter = ('tags',)
    search_fields = ('name', 'memo', 'tags__name')
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
            'name',
            'memo',
            'tags',
        )}),
    )
    readonly_fields = ('id', 'create_dt', 'update_dt', 'user')
    inlines = (MemoImageModelInline, MemoFileModelInline, MemoLinkModelInline)


tagulous.admin.enhance(MemoModel, MemoModelAdmin)
