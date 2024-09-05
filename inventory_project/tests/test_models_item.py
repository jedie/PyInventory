from django.forms import modelform_factory
from django.test import TestCase
from django_prose_editor.fields import ProseEditorFormField
from django_prose_editor.sanitized import SanitizedProseEditorField
from django_prose_editor.widgets import ProseEditorWidget

from inventory.models import ItemModel


class ItemModelTestCase(TestCase):
    def test_item_description_prose_editor(self):
        item = ItemModel()
        opts = item._meta
        model_description_field = opts.get_field('description')
        self.assertIsInstance(model_description_field, SanitizedProseEditorField)

    def test_item_description_form_prose_editor(self):
        ItemForm = modelform_factory(ItemModel, fields=('description',))
        form = ItemForm()
        form_field = form.fields['description']
        self.assertIsInstance(form_field, ProseEditorFormField)
        widget = form_field.widget

        self.assertIsInstance(widget, ProseEditorWidget)
