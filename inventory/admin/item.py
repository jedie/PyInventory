import tagulous
from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from inventory.admin.base import BaseUserAdmin
from inventory.models import ItemLinkModel, ItemModel


class ItemLinkModelInline(SortableInlineAdminMixin, admin.TabularInline):
    model = ItemLinkModel
    extra = 1


@admin.register(ItemModel)
class ItemModelAdmin(BaseUserAdmin):
    date_hierarchy = 'create_dt'
    list_display = (
        'kind', 'producer',
        'parent', 'name',
        'location', 'received_date', 'update_dt'
    )
    list_display_links = ('name',)
    list_filter = ('kind', 'location', 'producer', 'tags')
    search_fields = ('name', 'description')
    fieldsets = (
        (_('Internals'), {
            'classes': ('collapse',),
            'fields': (
                'id',
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
    inlines = (ItemLinkModelInline,)


tagulous.admin.enhance(ItemModel, ItemModelAdmin)
