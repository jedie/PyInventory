from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.fields import RichTextUploadingField, RichTextUploadingFormField
from django.forms import modelform_factory
from django.test import TestCase

from inventory.models import ItemModel


class ItemModelTestCase(TestCase):
    def test_item_description_ckeditor(self):
        item = ItemModel()
        opts = item._meta
        model_description_field = opts.get_field('description')
        self.assertIsInstance(model_description_field, RichTextUploadingField)

    def test_item_description_form_ckeditor(self):
        ItemForm = modelform_factory(ItemModel, fields=('description',))
        form = ItemForm()
        form_field = form.fields['description']
        self.assertIsInstance(form_field, RichTextUploadingFormField)
        widget = form_field.widget

        # Note: django-ckeditor 6.3.1-6.3.x broke the widget loading:
        self.assertIsInstance(widget, CKEditorWidget)
