import tagulous
from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from django.template.loader import render_to_string
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from import_export.admin import ImportExportMixin
from import_export.resources import ModelResource

from inventory.admin.base import BaseUserAdmin
from inventory.forms import ItemModelModelForm
from inventory.models import ItemLinkModel, ItemModel
from inventory.models.item import ItemFileModel, ItemImageModel


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


class ItemModelChangeList(ChangeList):
    def get_queryset(self, request):
        """
        List always the base instances
        """
        qs = super().get_queryset(request)
        qs = qs.filter(parent__isnull=True)
        return qs


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
        # TODO: annotate "sub_items" !
        qs = ItemModel.objects.filter(user=self.user)
        qs = qs.filter(parent=obj).sort()
        context = {
            'base_item': obj,
            'sub_items': qs
        }
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
    list_filter = ('kind', 'location', 'producer', 'tags')
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

    def get_changelist(self, request, **kwargs):
        self.user = request.user
        return ItemModelChangeList


tagulous.admin.enhance(ItemModel, ItemModelAdmin)
