import inspect
import io
from difflib import unified_diff

from django.contrib.auth.models import User
from django.core import management
from django.test import TestCase

from inventory.management.commands import seed_data
from inventory.models import ItemModel, LocationModel


class ManagementCommandTestCase(TestCase):
    def test_seed_data_command(self):
        output = io.StringIO()

        management.call_command(seed_data.Command(), user_count=2, location_count=2, item_count=2, stdout=output)
        assert User.objects.count() == 2
        assert LocationModel.objects.count() == 8
        assert ItemModel.objects.count() == 16

        output = output.getvalue()
        reference = inspect.cleandoc(
            """
            Fill database with example data
            ____________________________________________________________________________________________________
            Create seed data for user seed-data-user-1
            Room 1 › Cupboard 1 › Drawer 1 | Retrocomputing 001
            Room 1 › Cupboard 1 › Drawer 1 | Retrocomputing 001 › Item 001
            Room 1 › Cupboard 1 › Drawer 1 | Retrocomputing 001 › Item 001 › Part 001
            Room 1 › Cupboard 1 › Drawer 1 | Retrocomputing 001 › Item 001 › Part 002
            Room 1 › Cupboard 1 › Drawer 2 | Photo Equipment 002
            Room 1 › Cupboard 1 › Drawer 2 | Photo Equipment 002 › Item 002
            Room 1 › Cupboard 1 › Drawer 2 | Photo Equipment 002 › Item 002 › Part 003
            Room 1 › Cupboard 1 › Drawer 2 | Photo Equipment 002 › Item 002 › Part 004
            ____________________________________________________________________________________________________
            Create seed data for user seed-data-user-2
            Room 1 › Cupboard 1 › Drawer 1 | Household Goods 003
            Room 1 › Cupboard 1 › Drawer 1 | Household Goods 003 › Item 003
            Room 1 › Cupboard 1 › Drawer 1 | Household Goods 003 › Item 003 › Part 005
            Room 1 › Cupboard 1 › Drawer 1 | Household Goods 003 › Item 003 › Part 006
            Room 1 › Cupboard 1 › Drawer 2 | Retrocomputing 004
            Room 1 › Cupboard 1 › Drawer 2 | Retrocomputing 004 › Item 004
            Room 1 › Cupboard 1 › Drawer 2 | Retrocomputing 004 › Item 004 › Part 007
            Room 1 › Cupboard 1 › Drawer 2 | Retrocomputing 004 › Item 004 › Part 008

            Seed data created.
            """
        )
        if output.strip() != reference.strip():
            raise AssertionError(
                ''.join(
                    (
                        '\n',
                        '=' * 80,
                        '\n',
                        output,
                        '\n',
                        '=' * 80,
                        '\n',
                        *unified_diff(
                            a=output.splitlines(keepends=True),
                            b=reference.splitlines(keepends=True),
                            fromfile='output',
                            tofile='reference',
                        ),
                    ),
                )
            )
