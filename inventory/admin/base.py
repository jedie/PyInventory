from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from reversion_compare.admin import CompareVersionAdmin

from inventory.forms import OnlyUserRelationsModelForm


class UserInlineMixin:
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if not request.user.is_superuser:
            # Display only own created entries
            qs = qs.filter(user=request.user)

        return qs


class BaseUserAdmin(CompareVersionAdmin):
    form = OnlyUserRelationsModelForm

    def get_changelist(self, request, **kwargs):
        self.request = request
        self.user = request.user
        return super().get_changelist(request, **kwargs)

    def save_model(self, request, obj, form, change):
        if obj.user_id is None:
            obj.user = request.user

        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.select_related(
            'user',
        )
        if not request.user.is_superuser:
            # Display only own created entries
            qs = qs.filter(user=request.user)

        return qs

    def get_list_filter(self, request):
        list_filter = self.list_filter

        if request.user.is_superuser:
            # Superuser sees entries from all users -> Add "By user" filter
            list_filter = list(list_filter)
            list_filter.insert(0, 'user')

        return list_filter

    def get_list_display(self, request):
        list_display = self.list_display

        if request.user.is_superuser:
            # Superuser sees entries from all users -> Display the user in change list
            list_display = list(list_display)
            list_display.insert(0, 'user')

        return list_display


class BaseImageModelInline(UserInlineMixin, SortableInlineAdminMixin, admin.TabularInline):
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

    extra = 0
    fields = ('position', 'preview', 'image', 'name', 'tags')
    readonly_fields = ('preview',)


class BaseFileModelInline(UserInlineMixin, SortableInlineAdminMixin, admin.TabularInline):
    extra = 0
    fields = ('position', 'file', 'name', 'tags')


class LimitTreeDepthListFilter(admin.SimpleListFilter):
    title = _('Limit tree depth')
    parameter_name = 'level'

    def lookups(self, request, model_admin):
        return (
            ('1', _('Only root')),
            ('2', _('Root + first sub')),
            ('3', _('Root + first + second sub')),
        )

    def queryset(self, request, queryset):
        level = self.value()
        if level:
            level = int(level)
            return queryset.filter(level__lte=level)
