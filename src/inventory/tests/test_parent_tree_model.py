from bx_django_utils.test_utils.assert_queries import AssertQueries
from django.test import TestCase

from inventory.models import ItemModel
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
            (1, '1.', '1.'),
            (2, '1./1.1.', '1.1.'),
            (3, '1./1.1./1.1.1.', '1.1.1.'),
            (3, '1./1.1./1.1.2.', '1.1.2.'),
            (2, '1./1.2.', '1.2.'),
            (3, '1./1.2./1.2.1.', '1.2.1.'),
            (3, '1./1.2./1.2.2.', '1.2.2.'),
            (1, '2.', '2.'),
            (2, '2./2.1.', '2.1.'),
            (3, '2./2.1./2.1.1.', '2.1.1.'),
            (3, '2./2.1./2.1.2.', '2.1.2.'),
            (2, '2./2.2.', '2.2.'),
            (3, '2./2.2./2.2.1.', '2.2.1.'),
            (3, '2./2.2./2.2.2.', '2.2.2.'),
        ]

        item_2_1 = ItemModel.objects.get(name='2.1.')
        item_2_1.name = 'NEW 2.1. Name'
        with AssertQueries() as queries:
            item_2_1.save()

        data = list(ItemModel.objects.values_list('level', 'path_str', 'name'))
        assert data == [
            (1, '1.', '1.'),
            (2, '1./1.1.', '1.1.'),
            (3, '1./1.1./1.1.1.', '1.1.1.'),
            (3, '1./1.1./1.1.2.', '1.1.2.'),
            (2, '1./1.2.', '1.2.'),
            (3, '1./1.2./1.2.1.', '1.2.1.'),
            (3, '1./1.2./1.2.2.', '1.2.2.'),
            (1, '2.', '2.'),
            (2, '2./NEW 2.1. Name', 'NEW 2.1. Name'),
            (3, '2./NEW 2.1. Name/2.1.1.', '2.1.1.'),
            (3, '2./NEW 2.1. Name/2.1.2.', '2.1.2.'),
            (2, '2./2.2.', '2.2.'),
            (3, '2./2.2./2.2.1.', '2.2.1.'),
            (3, '2./2.2./2.2.2.', '2.2.2.'),
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
