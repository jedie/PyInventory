#!/usr/bin/env python3

import os
import sys


def main():
    assert 'DJANGO_SETTINGS_MODULE' in os.environ, 'No "DJANGO_SETTINGS_MODULE" in environment!'
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


if __name__ == '__main__':
    main()
