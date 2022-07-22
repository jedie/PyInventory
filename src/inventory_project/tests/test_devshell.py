import subprocess
import sys
from pathlib import Path
from unittest import TestCase

from dev_shell.utils.assertion import assert_is_file

import inventory


BASE_PATH = Path(inventory.__file__).parent.parent.parent


def call_devshell_commands(*args):
    dev_shell_py = BASE_PATH / 'devshell.py'
    assert_is_file(dev_shell_py)
    output = subprocess.check_output(
        [sys.executable, str(dev_shell_py)] + list(args), stderr=subprocess.STDOUT, text=True
    )
    return output


class DevShellTestCase(TestCase):
    def test_run_testserver(self):
        output = call_devshell_commands('run_testserver', '--help')
        assert 'usage: manage.py run_testserver' in output
        assert 'Run Django dev. Server' in output
        assert 'Optional port number, or ipaddr:port' in output

    def test_pass_wrong_addrport(self):
        output = call_devshell_commands('run_testserver', 'not-ip:no-port')
        assert "call 'runserver' command with" in output
        assert (
            'CommandError: "not-ip:no-port" is not a valid port number or address:port pair.'
        ) in output

    def test_manage_command(self):
        output = call_devshell_commands('manage', 'diffsettings')
        assert "DJANGO_SETTINGS_MODULE='inventory_project.settings.tests'" in output
        assert f"PROJECT_PATH:{BASE_PATH}/src" in output
        assert f"BASE_PATH:{BASE_PATH}" in output
        assert f"PROJECT_PATH = PosixPath('{BASE_PATH}/src')" in output
