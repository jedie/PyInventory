from pathlib import Path

from bx_py_utils.path import assert_is_dir

import inventory


PACKAGE_ROOT = Path(inventory.__file__).parent.parent
assert_is_dir(PACKAGE_ROOT / 'inventory')


__version__ = inventory.__version__
