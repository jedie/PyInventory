#!/usr/bin/env python3
import os
import sys
from pathlib import Path

from django import __version__ as django_version

import inventory
from inventory import __version__


BASE_PATH = Path(inventory.__file__).parent


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_project.settings.local')

    if '--version' not in sys.argv:
        print(f'PyInventory v{__version__} (Django v{django_version})', file=sys.stderr)
        print(f'DJANGO_SETTINGS_MODULE={os.environ["DJANGO_SETTINGS_MODULE"]!r}', file=sys.stderr)

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            'Couldn\'t import Django. Are you sure it\'s installed and '
            'available on your PYTHONPATH environment variable? Did you '
            'forget to activate a virtual environment?'
        ) from exc
    try:
        execute_from_command_line(sys.argv)
    except Exception as err:
        from bx_py_utils.error_handling import print_exc_plus
        print_exc_plus(err)
        raise


def start_test_server():
    """
    Entrypoint for "[tool.poetry.scripts]" script started by devshell command.
    """
    sys.argv = [__file__, "run_testserver"]
    main()


if __name__ == '__main__':
    main()
