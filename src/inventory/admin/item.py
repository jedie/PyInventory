import logging

import tagulous
from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin
from django.template.loader import render_to_string
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from import_export.admin import ImportExportMixin
from import_export.resources import ModelResource

from inventory.admin.base import BaseUserAdmin
from inventory.forms import ItemModelModelForm
from inventory.models import ItemLinkModel, ItemModel
from inventory.models.item import ItemFileModel, ItemImageModel


logger = logging.getLogger(__name__)


class UserInlineMixin:
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if not request.user.is_superuser:
            # Display only own created entries
            qs = qs.filter(user=request.user)

        return qs


class ItemLinkModelInline(UserInlineMixin, SortableInlineAdminMixin, admin.TabularInline):
    model = ItemLinkModel
    extra = 0


class ItemImageModelInline(UserInlineMixin, SortableInlineAdminMixin, admin.TabularInline):
    def preview(self, instance):
        return format_html(
            (
                '<a href="{url}" title="{name}"'
                ' target="_blank" class="image_file_input_preview">'
                '<img style="width:9em;" src="{url}"></a>'
            ),
            url=instance.image.url,
            name=instance.name,
        )
    model = ItemImageModel
    extra = 0
    fields = (
        'position', 'preview', 'image', 'name', 'tags'
    )
    readonly_fields = ('preview',)


class ItemFileModelInline(UserInlineMixin, SortableInlineAdminMixin, admin.TabularInline):
    model = ItemFileModel
    extra = 0
    fields = (
        'position', 'file', 'name', 'tags'
    )


class ItemModelResource(ModelResource):
    class Meta:
        model = ItemModel


class GroupItemsListFilter(admin.SimpleListFilter):
    title = _('Group Items')
    parameter_name = 'grouping'

    GET_KEY_AUTO = 'auto'
    GET_KEY_NO = 'no'

    def lookups(self, request, model_admin):
        return (
            (self.GET_KEY_AUTO, _('Automatic')),
            (self.GET_KEY_NO, _('No')),
        )

    def value(self):
        return super().value() or self.GET_KEY_AUTO

    def queryset(self, request, queryset):
        auto_mode = self.value() == self.GET_KEY_AUTO
        if auto_mode:
            request.group_items = not request.GET.keys()
        else:
            request.group_items = self.value() != self.GET_KEY_NO

        logger.info('Group items: %r (auto mode: %r)', request.group_items, auto_mode)

        if request.group_items:
            queryset = queryset.filter(parent__isnull=True)

        return queryset

    def choices(self, changelist):
        for lookup, title in self.lookup_choices:
            if lookup == self.GET_KEY_AUTO:
                query_string = changelist.get_query_string(remove=[self.parameter_name])
            else:
                query_string = changelist.get_query_string({self.parameter_name: lookup})

            yield {
                'selected': self.value() == lookup,
                'query_string': query_string,
                'display': title,
            }


@admin.register(ItemModel)
class ItemModelAdmin(ImportExportMixin, BaseUserAdmin):
    form = ItemModelModelForm

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related(
            'user',
        )
        qs = qs.prefetch_related(
            'kind',
            'producer',
        )
        return qs

    def column_item(self, obj):
        context = {
            'base_item': obj,
        }

        if self.request.group_items:  # Attribute added in GroupItemsListFilter.queryset()
            logger.debug('Display sub items inline')
            # TODO: annotate "sub_items" !
            qs = ItemModel.objects.filter(
                user=self.user  # user added in BaseUserAdmin.get_changelist()
            )
            qs = qs.filter(parent=obj).sort()
            context['sub_items'] = qs

        return render_to_string(
            template_name='admin/inventory/item/column_item.html',
            context=context,
        )

    column_item.short_description = _('ItemModel.verbose_name_plural')

    date_hierarchy = 'create_dt'
    list_display = (
        'kind', 'producer',
        'column_item',
        'location',
        'received_date', 'update_dt'
    )
    ordering = ('kind', 'producer', 'name')
    list_display_links = None
    list_filter = (GroupItemsListFilter, 'kind', 'location', 'producer', 'tags')
    search_fields = ('name', 'description', 'kind__name', 'tags__name')
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
    inlines = (ItemImageModelInline, ItemFileModelInline, ItemLinkModelInline)


tagulous.admin.enhance(ItemModel, ItemModelAdmin)
