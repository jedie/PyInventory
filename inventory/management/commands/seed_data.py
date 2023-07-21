import itertools
import logging
from collections import Counter

from django.contrib.auth.hashers import UNUSABLE_PASSWORD_PREFIX
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from inventory.models import ItemModel, LocationModel


SEED_DATA_USER_PREFIX = 'seed-data-user-'


class SetupLogger:
    def __init__(self, level):
        self.level = level

    def __enter__(self):
        self.old_level = logging.root.manager.disable
        logging.disable(self.level)

    def __exit__(self, exit_type, exit_value, exit_traceback):
        logging.disable(self.old_level)


def iter_location_chain(user, location_count):
    room_no = itertools.count(start=1)
    cupboard_no = itertools.count(start=1)
    drawer_no = itertools.count(start=1)

    location_no = 0
    while True:
        room = LocationModel.objects.create(user=user, name=f'Room {next(room_no)}')
        room.full_clean()
        for _ in range(2):
            cupboard = LocationModel.objects.create(user=user, name=f'Cupboard {next(cupboard_no)}', parent=room)
            cupboard.full_clean()
            for _ in range(2):
                drawer = LocationModel.objects.create(user=user, name=f'Drawer {next(drawer_no)}', parent=cupboard)
                drawer.full_clean()
                yield drawer
                location_no += 1
                if location_no >= location_count:
                    return


class ItemCreator:
    def __init__(self):
        self.equipment_no = itertools.count(start=1)
        self.item_no = itertools.count(start=1)
        self.part_no = itertools.count(start=1)

        self.part_per_location = Counter()

    def create_items(self, user, location, item_count):
        assert user
        assert location
        while True:
            equipment = ItemModel.objects.create(
                user=user,
                location=location,
                name=f'Equipment {next(self.equipment_no):03}',
            )
            equipment.full_clean()
            yield equipment

            while True:
                item = ItemModel.objects.create(
                    user=user,
                    location=location,
                    name=f'Item {next(self.item_no):03}',
                    parent=equipment,
                )
                item.full_clean()
                yield item

                while True:
                    part = ItemModel.objects.create(
                        user=user,
                        location=location,
                        name=f'Part {next(self.part_no):03}',
                        parent=item,
                    )
                    part.full_clean()
                    yield part
                    self.part_per_location[location] += 1
                    if self.part_per_location[location] >= item_count:
                        return


class Command(BaseCommand):
    help = 'Fill database with example data'

    def add_arguments(self, parser):
        parser.add_argument('--user-count', type=int, default=3, choices=range(1, 10), help='User count')
        parser.add_argument('--location-count', type=int, default=3, choices=range(1, 20), help='Location count')
        parser.add_argument('--item-count', type=int, default=4, choices=range(1, 40), help='Item count')

    def handle(self, **options):
        self.stdout.write(self.help)

        user_count = options['user_count']
        location_count = options['location_count']
        item_count = options['item_count']

        verbosity = options['verbosity']
        if verbosity > 2:
            log_level = logging.DEBUG
        else:
            log_level = logging.WARNING

        with SetupLogger(level=log_level):
            existing_users = User.objects.filter(username__startswith=SEED_DATA_USER_PREFIX)
            for user in existing_users:
                self.stdout.write(f'Clean data from user {user}...')
                info = user.delete()
                self.stdout.write(f'done: {info}')

            item_creator = ItemCreator()

            for user_no in range(1, user_count + 1):
                self.stdout.write('_' * 100)
                user = User.objects.create_user(
                    username=f'{SEED_DATA_USER_PREFIX}{user_no}',
                    email=f'{SEED_DATA_USER_PREFIX}{user_no}@test.tld',
                    password=f'{UNUSABLE_PASSWORD_PREFIX} no password',
                )
                self.stdout.write(f'Create seed data for user {user}')

                for location in iter_location_chain(user, location_count):
                    for item in item_creator.create_items(user, location, item_count):
                        self.stdout.write(f'{location} | {item}')

            self.stdout.write('\nSeed data created.')
