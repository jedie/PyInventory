import io

from django.core import management
from django.test import TestCase
from model_bakery import baker

from inventory.management.commands import tree
from inventory.models import ItemModel


class ManagementCommandTestCase(TestCase):
    def test_tree_command(self):
        baker.make(ItemModel, name='Foo Bar')
        ItemModel.objects.update(path_str='OLD', path=['OLD'])

        output = io.StringIO()

        management.call_command(tree.Command(), stdout=output)

        output = output.getvalue()
        self.assertIn('Repair tree information', output)

        self.assertIn("Old information about model: 'Item'", output)
        self.assertIn("{'level': 1, 'path_str': 'OLD', 'path': ['OLD'], 'name': 'Foo Bar'}", output)

        self.assertIn("New information about model: 'Item'", output)
        self.assertIn("{'level': 1, 'path_str': 'foobar', 'path': ['Foo Bar'], 'name': 'Foo Bar'}", output)
