import time
from argparse import OPTIONAL

from django.apps import apps
from django.core.management.base import BaseCommand


class PrintDuration:
    def __init__(self, stdout):
        self.stdout = stdout

    def __enter__(self):
        self.start_time = time.monotonic()

    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = (time.monotonic() - self.start_time) * 1000
        self.stdout.write(f'(Done in: {duration:.1f}ms)')


class Command(BaseCommand):
    help = 'Repair tree information'

    def add_arguments(self, parser):
        parser.add_argument(
            'model_name',
            metavar='model_name',
            nargs=OPTIONAL,
            default='itemmodel',
            choices=['itemmodel', 'locationmodel'],
            help='Model Name (default: "%(default)s")',
        )

    def handle(self, *args, **options):
        self.stdout.write()
        self.stdout.write('=' * 100)
        self.stdout.write(self.help)
        self.stdout.write('-' * 100)

        model_name = options['model_name']
        ModelClass = apps.get_model(app_label='inventory', model_name=model_name)

        self.print_info(ModelClass, text='Old information about model:')

        self.stdout.write('_' * 100)
        self.stdout.write(f'Clean tree information on model: {ModelClass._meta.verbose_name!r}')
        with PrintDuration(self.stdout):
            ModelClass.objects.update(path=None, path_str=None, level=None)

        self.stdout.write('_' * 100)
        self.stdout.write(f'Repair tree model: {ModelClass._meta.verbose_name!r}')
        with PrintDuration(self.stdout):
            ModelClass.tree_objects.update_tree_info()

        self.print_info(ModelClass, text='New information about model:')

    def print_info(self, ModelClass, text):
        self.stdout.write('_' * 100)
        self.stdout.write(f'{text} {ModelClass._meta.verbose_name!r}')
        with PrintDuration(self.stdout):
            data = ModelClass.objects.values('level', 'path_str', 'path', 'name')
            for entry in data:
                self.stdout.write(repr(entry))
