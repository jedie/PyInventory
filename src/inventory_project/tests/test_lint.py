import subprocess
import sys
from pathlib import Path

from dev_shell.utils.assertion import assert_is_file

import inventory


BASE_PATH = Path(inventory.__file__).parent.parent.parent


def test_lint():
    dev_shell_py = BASE_PATH / 'devshell.py'
    assert_is_file(dev_shell_py)
    subprocess.check_call([sys.executable, str(dev_shell_py), 'linting'])
