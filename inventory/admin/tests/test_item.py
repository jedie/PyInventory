from unittest import mock
from uuid import UUID

from bx_django_utils.test_utils.html_assertion import HtmlAssertionMixin, assert_html_response_snapshot
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django.template.defaulttags import CsrfTokenNode, NowNode
from django.test import TestCase, override_settings
from django.urls import reverse
from model_bakery import baker

from inventory.admin.item import mass_change_category_action
from inventory.models import ItemMainCategory, ItemModel
from inventory_project.tests.fixtures import get_normal_user
from inventory_project.tests.mocks import MockInventoryVersionString


@override_settings(SECURE_SSL_REDIRECT=False)
class MassChangeCategoryActionAdminTest(HtmlAssertionMixin, TestCase):
    maxDiff = None

    def test_happy_path(self):
        normaluser = get_normal_user()
        self.client.force_login(normaluser)

        category1 = baker.make(ItemMainCategory, order=0, id=1, name='Category 1')
        category2 = baker.make(ItemMainCategory, order=1, id=2, name='Category 2')
        baker.make(
            ItemModel,
            name='A',
            user=normaluser,
            id=UUID('80dddef9-0000-0000-0000-000000000001'),
            category=category1,
        ).full_clean()
        baker.make(
            ItemModel,
            name='B',
            user=normaluser,
            id=UUID('80dddef9-0000-0000-0000-000000000002'),
            category=category1,
        ).full_clean()
        baker.make(
            ItemModel,
            name='C',
            user=normaluser,
            id=UUID('80dddef9-0000-0000-0000-000000000003'),
            category=category2,
        ).full_clean()
        baker.make(
            ItemModel,
            name='D',
            user=normaluser,
            id=UUID('80dddef9-0000-0000-0000-000000000004'),
            category=category2,
        ).full_clean()

        url = reverse('admin:inventory_itemmodel_changelist')
        self.assertEqual(url, '/admin/inventory/itemmodel/')

        ########################################################################################
        # Snapshot the Form:
        with (
            mock.patch.object(NowNode, 'render', return_value='MockedNowNode'),
            mock.patch.object(CsrfTokenNode, 'render', return_value='MockedCsrfTokenNode'),
            MockInventoryVersionString(),
        ):
            response = self.client.post(
                '/admin/inventory/itemmodel/',
                data={
                    ACTION_CHECKBOX_NAME: [
                        '80dddef9-0000-0000-0000-000000000002',
                        '80dddef9-0000-0000-0000-000000000003',
                    ],
                    'action': mass_change_category_action.__name__,
                },
            )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/item/mass_change_category_action.html')
        self.assert_html_parts(
            response,
            parts=(
                '<title>Change category for selected items | PyInventory vMockedVersionString</title>',
                '<p>Number of selected items: 2</p>',
                '<label for="id_category">New category:</label>',
                '<input type="hidden" name="action" value="mass_change_category_action">',
            ),
        )
        assert_html_response_snapshot(response, query_selector='#content', validate=False)

        ########################################################################################
        # Perform the action

        def get_info():
            return list(ItemModel.objects.order_by('pk').values_list('pk', 'category__name'))

        before = get_info()

        response = self.client.post(
            '/admin/inventory/itemmodel/',
            data={
                ACTION_CHECKBOX_NAME: [
                    '80dddef9-0000-0000-0000-000000000002',
                    '80dddef9-0000-0000-0000-000000000003',
                ],
                'action': mass_change_category_action.__name__,
                'category': category2.pk,
            },
        )
        self.assertRedirects(response, '/admin/inventory/itemmodel/', fetch_redirect_response=False)
        self.assert_messages(
            response,
            expected_messages=[
                '2 items have been assigned to the category "Category 2".',
            ],
        )

        after = get_info()
        self.assertEqual(
            before,
            [
                (UUID('80dddef9-0000-0000-0000-000000000001'), 'Category 1'),
                (UUID('80dddef9-0000-0000-0000-000000000002'), 'Category 1'),
                (UUID('80dddef9-0000-0000-0000-000000000003'), 'Category 2'),
                (UUID('80dddef9-0000-0000-0000-000000000004'), 'Category 2'),
            ],
        )
        self.assertEqual(
            after,
            [
                (UUID('80dddef9-0000-0000-0000-000000000001'), 'Category 1'),  # Not selected
                (UUID('80dddef9-0000-0000-0000-000000000002'), 'Category 2'),  # Changed
                (UUID('80dddef9-0000-0000-0000-000000000003'), 'Category 2'),  # Already there
                (UUID('80dddef9-0000-0000-0000-000000000004'), 'Category 2'),  # Not selected
            ],
        )
