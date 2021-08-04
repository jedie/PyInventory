import subprocess
import sys
from pathlib import Path
from unittest import TestCase

from dev_shell.utils.assertion import assert_is_file

import inventory


BASE_PATH = Path(inventory.__file__).parent.parent.parent


def call_run_testserver(*args):
    dev_shell_py = BASE_PATH / 'devshell.py'
    assert_is_file(dev_shell_py)
    output = subprocess.check_output(
        [sys.executable, str(dev_shell_py), 'run_testserver'] + list(args),
        stderr=subprocess.STDOUT,
        text=True
    )
    return output


class RunTestServerTestCase(TestCase):
    def test_run_testserver(self):
        output = call_run_testserver('--help')
        assert 'usage: manage.py run_testserver' in output
        assert 'Run Django dev. Server' in output
        assert 'Optional port number, or ipaddr:port' in output

    def test_pass_wrong_addrport(self):
        output = call_run_testserver('not-ip:no-port')
        assert "call 'runserver' command with" in output
        assert (
            'CommandError: "not-ip:no-port" is not a valid port number or address:port pair.'
        ) in output
