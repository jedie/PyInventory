from bx_py_utils.test_utils.snapshot import assert_text_snapshot
from manage_django_project.tests.cmd2_test_utils import BaseShellTestCase


class PyInventoryDevShellTestCase(BaseShellTestCase):
    def test_help(self):
        stdout, stderr = self.execute(command='help')
        self.assertEqual(stderr, '')
        self.assertIn('Documented commands', stdout)

        # Django commands:
        self.assertIn('django.core', stdout)
        self.assertIn('makemessages', stdout)
        self.assertIn('makemigrations', stdout)

        # manage_django_project:
        self.assertIn('manage_django_project', stdout)
        self.assertIn('run_dev_server', stdout)

        # Own commands:
        self.assertIn('inventory', stdout)
        self.assertIn('seed_data', stdout)
        self.assertIn('tree', stdout)

        assert_text_snapshot(got=stdout)
