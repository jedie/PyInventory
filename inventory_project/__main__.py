"""
    Allow your-cool-package to be executable
    through `python -m inventory`.
"""

import sys

from manage_django_project.manage import execute_django_from_command_line
from typeguard import install_import_hook


def main():
    """
    entrypoint installed via pyproject.toml and [project.scripts] section.
    Must be set in ./manage.py and PROJECT_SHELL_SCRIPT
    """

    if 'test' in sys.argv:
        # Install typeguard import hook to check for missing type annotations.
        # Sadly we can't add this into: cli_base/tests/__init__.py
        install_import_hook(packages=('inventory', 'inventory_project'))

    execute_django_from_command_line()


if __name__ == '__main__':
    main()
