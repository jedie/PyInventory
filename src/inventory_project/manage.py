import os
import sys

from django import __version__ as django_version

from inventory import __version__


def main(argv):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_project.settings.local')

    if '--version' not in argv:
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
        execute_from_command_line(argv)
    except Exception as err:
        from bx_py_utils.error_handling import print_exc_plus
        print_exc_plus(err)
        raise


def start_test_server():
    """
    Entrypoint for "[tool.poetry.scripts]" script started by devshell command.
    """
    main(argv=[__file__, "run_testserver"] + sys.argv[1:])


if __name__ == '__main__':
    main(argv=sys.argv)
