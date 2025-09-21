import logging

import tagulous
from adminsortable2.admin import SortableAdminBase, SortableAdminMixin, SortableInlineAdminMixin
from django.conf import settings
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.db import models
from django.db.models import Count
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
    UserInlineMixin,
)
from inventory.admin.tagulous_fix import TagulousModelAdminFix
from inventory.current_category import get_current_category_slug, set_current_category_slug
from inventory.models import ItemLinkModel, ItemModel
from inventory.models.item import ItemFileModel, ItemImageModel, ItemMainCategory
from inventory.string_utils import ltruncatechars


logger = logging.getLogger(__name__)


@admin.register(ItemMainCategory)
class ItemMainCategoryAdmin(SortableAdminMixin, admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('order', 'name')


class MainCategoryListFilter(admin.SimpleListFilter):
    title = _('ItemMainCategory.verbose_name')
    parameter_name = 'category'
    value_uncategorized = '__uncategorized__'

    def __init__(self, request, params, model, model_admin: ModelAdmin):
        self.request = request
        self.model: models.Model = model_admin.model
        super().__init__(request, params, model, model_admin)

    def has_output(self):
        return ItemMainCategory.objects.exists()

    def lookups(self, request, model_admin):
        pass  # Only a placeholder, real lookups are generated in choices()!

    def get_lookups(self, add_facets):
        base_qs = self.model.objects.all()
        if not self.request.user.is_superuser:
            # Display only own created entries
            base_qs = base_qs.select_related('user')
            base_qs = base_qs.filter(user=self.request.user)

        if add_facets:
            # Collect the counts for all used categories:
            used_category_counts = dict(
                base_qs.order_by()
                .values('category_id')
                .annotate(count=Count('category_id'))
                .values_list('category_id', 'count')
                .distinct()
            )

        # Get all categories:
        all_categories_qs = ItemMainCategory.objects.order_by('order').values_list('id', 'name', 'slug')

        lookups_data = [(None, _('All'))]

        # add with "Uncategorized" (without a category) if there are any:
        uncategorized_count = base_qs.filter(category__isnull=True).count()
        if uncategorized_count:
            if add_facets:
                uncategorized_title = _('Uncategorized (%(count)s)') % {'count': uncategorized_count}
            else:
                uncategorized_title = _('Uncategorized')
            lookups_data.append((self.value_uncategorized, uncategorized_title))

        # Add all categories with their used counts:
        for id, name, slug in all_categories_qs:
            if add_facets:
                count = used_category_counts.get(id, 0)
                lookups_data.append((slug, f'{name} ({count})'))
            else:
                lookups_data.append((slug, name))

        return lookups_data

    def choices(self, changelist):
        lookup_choices = self.get_lookups(add_facets=changelist.add_facets)
        for lookup, title in lookup_choices:
            yield {
                'selected': self.value() == lookup,
                'query_string': changelist.get_query_string({self.parameter_name: lookup}),
                'display': title,
            }

    def value(self):
        if self.parameter_name not in self.request.GET:
            # Use last selected category if available:
            slug = get_current_category_slug(user=self.request.user)
        else:
            # Get from GET parameters:
            slug = super().value()
        return slug

    def queryset(self, request, queryset):
        if slug := self.value():
            if slug == self.value_uncategorized:
                # "Uncategorized" items (items without a category)
                queryset = queryset.filter(category__isnull=True)
            else:
                # items from the selected category:
                queryset = queryset.filter(category__slug=slug)

        set_current_category_slug(user=request.user, slug=slug)

        return queryset


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
class ItemModelAdmin(TagulousModelAdminFix, ImportExportMixin, SortableAdminBase, BaseUserAdmin):
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
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related(
            'location',
            'kind',
            'producer',
        )
        return queryset

    def get_max_order(self, request, obj=None):
        # Work-a-round for: https://github.com/jrief/django-admin-sortable2/issues/341
        return 0

    date_hierarchy = 'create_dt'
    list_display = ('producer', 'item', 'kind', 'location', 'received_date', 'update_dt')
    ordering = ('path_str',)
    list_display_links = ()
    list_filter = (
        MainCategoryListFilter,
        LimitTreeDepthListFilter,
        ('kind', admin.RelatedOnlyFieldListFilter),
        ('location', admin.RelatedOnlyFieldListFilter),
        ('producer', admin.RelatedOnlyFieldListFilter),
        ('tags', admin.RelatedOnlyFieldListFilter),
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


tagulous.admin.enhance(ItemModel, ItemModelAdmin)
