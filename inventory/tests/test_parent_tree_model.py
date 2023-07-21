from bx_django_utils.test_utils.assert_queries import AssertQueries
from django.db.models import QuerySet
from django.test import TestCase

from inventory.admin import ItemModelAdmin, LocationModelAdmin
from inventory.models import ItemModel, LocationModel
from inventory_project.tests.fixtures import get_normal_user


class TreeModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.normaluser = get_normal_user()

    def test_parent_tree_model(self):
        for main_item_no in range(1, 3):
            main_item = ItemModel.objects.create(
                user=self.normaluser,
                name=f'{main_item_no}.',
            )
            main_item.full_clean()

            for sub_item_no in range(1, 3):
                sub_item = ItemModel.objects.create(
                    parent=main_item,
                    user=self.normaluser,
                    name=f'{main_item_no}.{sub_item_no}.',
                )
                sub_item.full_clean()

                for sub_sub_item_no in range(1, 3):
                    sub_sub_item = ItemModel.objects.create(
                        parent=sub_item,
                        user=self.normaluser,
                        name=f'{main_item_no}.{sub_item_no}.{sub_sub_item_no}.',
                    )
                    sub_sub_item.full_clean()

        data = list(ItemModel.objects.values_list('level', 'path_str', 'name'))
        assert data == [
            (1, '1', '1.'),
            (2, '1 0 11', '1.1.'),
            (3, '1 0 11 0 111', '1.1.1.'),
            (3, '1 0 11 0 112', '1.1.2.'),
            (2, '1 0 12', '1.2.'),
            (3, '1 0 12 0 121', '1.2.1.'),
            (3, '1 0 12 0 122', '1.2.2.'),
            (1, '2', '2.'),
            (2, '2 0 21', '2.1.'),
            (3, '2 0 21 0 211', '2.1.1.'),
            (3, '2 0 21 0 212', '2.1.2.'),
            (2, '2 0 22', '2.2.'),
            (3, '2 0 22 0 221', '2.2.1.'),
            (3, '2 0 22 0 222', '2.2.2.'),
        ]

        item_2_1 = ItemModel.objects.get(name='2.1.')

        related_qs = ItemModel.tree_objects.related_objects(instance=item_2_1)
        data = list(related_qs.values_list('name', flat=True))
        assert data == ['2.', '2.1.', '2.1.1.', '2.1.2.', '2.2.', '2.2.1.', '2.2.2.']

        item_2_1.name = 'NEW 2.1. Name'
        with AssertQueries() as queries:
            item_2_1.save()

        data = list(ItemModel.objects.values_list('level', 'path_str', 'name'))
        assert data == [
            (1, '1', '1.'),
            (2, '1 0 11', '1.1.'),
            (3, '1 0 11 0 111', '1.1.1.'),
            (3, '1 0 11 0 112', '1.1.2.'),
            (2, '1 0 12', '1.2.'),
            (3, '1 0 12 0 121', '1.2.1.'),
            (3, '1 0 12 0 122', '1.2.2.'),
            (1, '2', '2.'),
            (2, '2 0 22', '2.2.'),
            (3, '2 0 22 0 221', '2.2.1.'),
            (3, '2 0 22 0 222', '2.2.2.'),
            (2, '2 0 new21name', 'NEW 2.1. Name'),
            (3, '2 0 new21name 0 211', '2.1.1.'),
            (3, '2 0 new21name 0 212', '2.1.2.'),
        ]

        itemmodel_count = 1  # full_clean(): Check if parent exists
        itemmodel_count += 1  # VersionProtectBaseModel: Check version
        itemmodel_count += 1  # VersionProtectBaseModel: Save new version
        itemmodel_count += 1  # Get info for tree update
        itemmodel_count += 1  # Fetch the items to update
        itemmodel_count += 1  # Bulk update save

        queries.assert_queries(
            table_counts={
                'inventory_itemmodel': itemmodel_count,
                'auth_user': 1,  # full_clean(): Check if user exists
            },
            double_tables=False,
            duplicated=True,
            similar=True,
        )

    def test_related_objects(self):
        item = ItemModel()
        qs = ItemModel.tree_objects.related_objects(instance=item)
        assert isinstance(qs, QuerySet)
        assert qs.query.is_empty() is True

    def test_parent_tree_model_ordering(self):
        assert LocationModel._meta.ordering == ('path_str',)
        assert LocationModelAdmin.ordering == ('path_str',)

        assert ItemModel._meta.ordering == ('path_str',)
        assert ItemModelAdmin.ordering == ('path_str',)

        def create(name, parent=None):
            instance = ItemModel.objects.create(user=self.normaluser, name=name, parent=parent)
            instance.full_clean()
            return instance

        # Create a "Special" case for the correct ordering:
        #  1. all "PC-1" entries
        #  2. all "PC1640" entries
        #
        # The correct order depends on the seperator, here: " 0 "

        pc1 = create(name='PC-1')
        pc1640 = create(name='PC1640 SD')
        create(name='FZ-502 Rev A 5.25″ Floppy', parent=pc1)
        create(name='1,44MB / 3.5" Floppy FD-235HF- 3800-U', parent=pc1)
        create(name='PC 1640ECD', parent=pc1640)

        data = list(ItemModel.objects.values_list('level', 'path_str', 'name'))
        assert data == [
            (1, 'pc1', 'PC-1'),
            (2, 'pc1 0 144mb35floppyfd235hf3800u', '1,44MB / 3.5" Floppy FD-235HF- 3800-U'),
            (2, 'pc1 0 fz502reva525floppy', 'FZ-502 Rev A 5.25″ Floppy'),
            (1, 'pc1640sd', 'PC1640 SD'),
            (2, 'pc1640sd 0 pc1640ecd', 'PC 1640ECD'),
        ]
