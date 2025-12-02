import logging

import tagulous
from adminsortable2.admin import SortableAdminBase, SortableAdminMixin, SortableInlineAdminMixin
from django import forms
from django.conf import settings
from django.contrib import admin, messages
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django.shortcuts import render
from django.template.loader import render_to_string
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
    NoneEmptyRelatedFieldListFilter,
    UserInlineMixin,
)
from inventory.models import ItemLinkModel, ItemModel
from inventory.models.item import ItemFileModel, ItemImageModel, ItemMainCategory
from inventory.persistent_filters import PersistentRelatedFieldListFilter
from inventory.string_utils import ltruncatechars


logger = logging.getLogger(__name__)


@admin.register(ItemMainCategory)
class ItemMainCategoryAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('order', 'name')


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


class ChangeCategoryForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=ItemMainCategory.objects.all(),
        label=_('New category'),
        required=True,
    )


@admin.action(description=_('Change category for selected items'))
def mass_change_category_action(modeladmin, request, queryset):
    item_count = queryset.count()
    assert item_count > 0, 'No items selected for mass category change.'
    if 'category' in request.POST:
        form = ChangeCategoryForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data['category']
            updated = queryset.update(category=category)
            messages.info(
                request,
                _('%(count)d items have been assigned to the category "%(category)s".')
                % {'count': updated, 'category': str(category)},
            )
            return None
    else:
        form = ChangeCategoryForm()

    # Collect currently used categories from selected items:
    used_categories = queryset.order_by('category__name').values_list('category__name', flat=True).distinct()

    return render(
        request,
        'admin/item/mass_change_category_action.html',
        context={
            'title': _('Change category for selected items'),
            'opts': modeladmin.model._meta,
            'item_count': item_count,
            'items': queryset,
            'used_categories': used_categories,
            'form': form,
            'action_checkbox_name': ACTION_CHECKBOX_NAME,
            **modeladmin.admin_site.each_context(request),
        },
    )


@admin.register(ItemModel)
class ItemModelAdmin(ImportExportMixin, SortableAdminBase, BaseUserAdmin):
    @admin.display(description=_('Related items'))
    def related_items(self, obj):
        if obj.pk is None:
            # Add a new item -> there are no related items ;)
            return '-'

        related_qs = ItemModel.tree_objects.related_objects(instance=obj)
        context = {
            'items': related_qs,
            'opts': self.opts,
        }
        return render_to_string('admin/item/related_items.html', context)

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
            format_string='<a href="{url}">{prefixes}<strong>{item}</strong></a>',
            url=url,
            prefixes=prefixes,
            item=item,
        )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.prefetch_related(
            'location',
            'kind',
            'producer',
        )
        return qs

    def get_max_order(self, request, obj=None):
        # Work-a-round for: https://github.com/jrief/django-admin-sortable2/issues/341
        return 0

    date_hierarchy = 'create_dt'
    list_display = ('producer', 'item', 'kind', 'location', 'received_date', 'update_dt')
    ordering = ('path_str',)
    list_display_links = ()
    list_filter = (
        ('category', PersistentRelatedFieldListFilter),
        LimitTreeDepthListFilter,
        ('kind', NoneEmptyRelatedFieldListFilter),
        ('location', NoneEmptyRelatedFieldListFilter),
        ('producer', NoneEmptyRelatedFieldListFilter),
        ('tags', NoneEmptyRelatedFieldListFilter),
    )
    search_fields = ('name', 'description', 'kind__name', 'tags__name')
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
                    ('category', 'kind'),
                    ('producer', 'name'),
                    'description',
                    'tags',
                    'fcc_id',
                    'parent',
                    'location',
                )
            },
        ),
        (_('Related items'), {'classes': ('collapse',), 'fields': ('related_items',)}),
        (
            _('Lent'),
            {
                'classes': ('collapse',),
                'fields': (
                    'lent_to',
                    (
                        'lent_from_date',
                        'lent_until_date',
                    ),
                ),
            },
        ),
        (
            _('Received'),
            {
                'classes': ('collapse',),
                'fields': (('received_from', 'received_date', 'received_price'),),
            },
        ),
        (
            _('Handed over'),
            {
                'classes': ('collapse',),
                'fields': (('handed_over_to', 'handed_over_date', 'handed_over_price'),),
            },
        ),
    )
    autocomplete_fields = ('parent', 'location')
    readonly_fields = ('id', 'create_dt', 'update_dt', 'user', 'related_items')
    inlines = (ItemImageModelInline, ItemFileModelInline, ItemLinkModelInline)
    actions = (mass_change_category_action,)


tagulous.admin.enhance(ItemModel, ItemModelAdmin)
