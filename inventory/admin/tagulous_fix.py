"""
    Work-a-round for:
        https://github.com/radiac/django-tagulous/issues/164
"""
from django import forms
from django.contrib.admin.widgets import AutocompleteMixin
from tagulous import settings as tagulous_settings
from tagulous.forms import AdminTagWidget, BaseTagField
from tagulous.models import SingleTagField, TagField


class AdminTagWidget2(AdminTagWidget):
    @property
    def media(self):
        # Get the media from the AutocompleteMixin - this will give us Django's
        # vendor jQuery and select2
        class GetMedia(AutocompleteMixin, forms.Select):
            pass

        dependency_media = GetMedia(None, None).media
        tagulous_media = forms.Media(
            js=tagulous_settings.ADMIN_AUTOCOMPLETE_JS,
            css=tagulous_settings.ADMIN_AUTOCOMPLETE_CSS,
        )
        all_media = dependency_media + tagulous_media

        return all_media


class BaseTagField2(BaseTagField):
    widget = AdminTagWidget2


class TagulousModelAdminFix:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.formfield_overrides[SingleTagField] = {
            'form_class': BaseTagField2,
            'widget': AdminTagWidget2,
        }
        self.formfield_overrides[TagField] = {
            'form_class': BaseTagField2,
            'widget': AdminTagWidget2,
        }
