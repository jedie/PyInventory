import filecmp
import shutil
from pathlib import Path
from unittest import TestCase

import dev_shell
from dev_shell.utils.assertion import assert_is_file

from inventory_project.dev_shell import PACKAGE_ROOT


class BootstrapTestCase(TestCase):
    def test_our_bootstrap_is_up2date(self):
        source_file_path = Path(dev_shell.__file__).parent / 'bootstrap-source.py'
        assert_is_file(source_file_path)

        own_bootstrap_file = PACKAGE_ROOT / 'devshell.py'
        assert_is_file(own_bootstrap_file)

        are_the_same = filecmp.cmp(source_file_path, own_bootstrap_file, shallow=False)
        if not are_the_same:
            shutil.copyfile(
                src=source_file_path,
                dst=own_bootstrap_file,
                follow_symlinks=False
            )
            raise AssertionError(f'Bootstrap "{own_bootstrap_file}" updated!')
