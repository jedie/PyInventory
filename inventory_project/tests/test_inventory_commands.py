from cmd2 import CommandResult
from cmd2_ext_test import ExternalTestMixin
from dev_shell.tests.fixtures import CmdAppBaseTestCase
from django import __version__

from inventory_project.dev_shell import DevShellApp, get_devshell_app_kwargs


class DevShellAppTester(ExternalTestMixin, DevShellApp):
    pass


class DevShellAppBaseTestCase(CmdAppBaseTestCase):
    """
    Base class for dev-shell tests
    """

    def get_app_instance(self):
        # Init the test app with the same kwargs as the real app
        # see: dev_shell.cmd2app.devshell_cmdloop()
        app = DevShellAppTester(**get_devshell_app_kwargs())
        return app


class PyInventoryDevShellTestCase(DevShellAppBaseTestCase):
    def test_help_raw(self):
        out = self.app.app_cmd('help')

        assert isinstance(out, CommandResult)
        assert 'Documented commands' in out.stdout

        assert 'Documented commands' in out.stdout

    def test_help_via_execute(self):
        stdout, stderr = self.execute('help')
        assert stderr == ''
        assert 'Documented commands' in stdout

    def test_manage(self):
        stdout, stderr = self.execute('manage --version')
        assert stderr == ''
        assert 'manage.py --version' in stdout
        assert __version__ in stdout
