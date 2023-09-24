import sys

from cli_base.cli_tools.subprocess_utils import verbose_check_call
from manage_django_project.management.base import BasePassManageCommand


class Command(BasePassManageCommand):  # TODO: Move to manage_django_projects
    help = 'Call playwright CLI'

    def run_from_argv(self, argv):
        super().run_from_argv(argv)

        # Just pass every argument to the origin CLI:
        verbose_check_call(sys.executable, '-m', 'playwright', *argv[2:], exit_on_error=True)

        sys.exit(0)
