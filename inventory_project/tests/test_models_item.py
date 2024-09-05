from django.forms import CharField, modelform_factory
from django.test import TestCase
from tinymce.models import HTMLField
from tinymce.widgets import TinyMCE

from inventory.models import ItemModel


class ItemModelTestCase(TestCase):
    def test_item_description_model_field(self):
        item = ItemModel()
        opts = item._meta
        model_description_field = opts.get_field('description')
        self.assertIsInstance(model_description_field, HTMLField)

    def test_item_description_form_fieldr(self):
        ItemForm = modelform_factory(ItemModel, fields=('description',))
        form = ItemForm()
        form_field = form.fields['description']
        self.assertIsInstance(form_field, CharField)
        widget = form_field.widget

        self.assertIsInstance(widget, TinyMCE)
