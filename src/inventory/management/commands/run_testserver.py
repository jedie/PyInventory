import os

from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    help = "Run Django dev. Server"

    def verbose_call(self, command, **kwargs):
        self.stdout.write("\n")
        self.stdout.write("_" * 79)
        self.stdout.write(self.style.NOTICE(f" *** call '{command}' command:"))
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

        self.verbose_call("runserver", use_threading=True, use_reloader=True, verbosity=2)
