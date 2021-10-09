from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin
from django.utils.html import format_html
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
    fields = (
        'position', 'preview', 'image', 'name', 'tags'
    )
    readonly_fields = ('preview',)


class BaseFileModelInline(UserInlineMixin, SortableInlineAdminMixin, admin.TabularInline):
    extra = 0
    fields = (
        'position', 'file', 'name', 'tags'
    )
