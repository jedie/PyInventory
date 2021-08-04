import os

from django.core.management import call_command
from django.core.management.commands.runserver import Command as RunServerCommand


class Command(RunServerCommand):
    help = "Run Django dev. Server"

    def verbose_call(self, command, **kwargs):
        self.stdout.write("\n")
        self.stdout.write("_" * 79)
        self.stdout.write(self.style.NOTICE(f" *** call '{command}' command with {kwargs}:"))
        self.stdout.write("\n")
        call_command(command, **kwargs)

    def handle(self, *args, **options):
        """
        INFO: The django reloader will call this multiple times!
        We check RUN_MAIN, that will be set in django.utils.autoreload
        So we can skip the first migrate run.
        """
        if os.environ.get("RUN_MAIN"):
            self.verbose_call("migrate", run_syncdb=True, interactive=False, verbosity=1)
            self.verbose_call("showmigrations", verbosity=1)

        self.verbose_call("runserver", **options)
