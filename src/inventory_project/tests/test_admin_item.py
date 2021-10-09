import datetime
import logging
from unittest import mock

from bx_django_utils.test_utils.datetime import MockDatetimeGenerator
from bx_django_utils.test_utils.html_assertion import HtmlAssertionMixin
from django.contrib.auth.models import User
from django.template.defaulttags import CsrfTokenNode
from django.test import TestCase
from django.utils import timezone
from django_tools.unittest_utils.mockup import ImageDummy
from model_bakery import baker

from inventory import __version__
from inventory.models import ItemImageModel, ItemModel
from inventory.permissions import get_or_create_normal_user_group
from inventory_project.tests.temp_utils import assert_html_response_snapshot


class AdminAnonymousTests(TestCase):
    def test_login(self):
        response = self.client.get('/admin/inventory/itemmodel/add/', HTTP_ACCEPT_LANGUAGE='en')
        self.assertRedirects(
            response,
            expected_url='/admin/login/?next=/admin/inventory/itemmodel/add/'
        )


class AdminTestCase(HtmlAssertionMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.normaluser = baker.make(
            User, username='NormalUser',
            is_staff=True, is_active=True, is_superuser=False
        )
        assert cls.normaluser.user_permissions.count() == 0
        group = get_or_create_normal_user_group()[0]
        cls.normaluser.groups.set([group])

    def test_normal_user_create_minimal_item(self):
        self.client.force_login(self.normaluser)

        with mock.patch.object(CsrfTokenNode, 'render', return_value='MockedCsrfTokenNode'):
            response = self.client.get('/admin/inventory/itemmodel/add/')
        assert response.status_code == 200
        self.assert_html_parts(response, parts=(
            f'<title>Add Item | PyInventory v{__version__}</title>',
        ))
        assert_html_response_snapshot(response=response, validate=False)

        assert ItemModel.objects.count() == 0

        response = self.client.post(
            path='/admin/inventory/itemmodel/add/',
            data={
                'kind': 'kind',
                'name': 'name',

                'itemimagemodel_set-TOTAL_FORMS': '0',
                'itemimagemodel_set-INITIAL_FORMS': '0',
                'itemimagemodel_set-MIN_NUM_FORMS': '0',
                'itemimagemodel_set-MAX_NUM_FORMS': '1000',
                'itemimagemodel_set-__prefix__-position': '0',

                'itemfilemodel_set-TOTAL_FORMS': '0',
                'itemfilemodel_set-INITIAL_FORMS': '0',
                'itemfilemodel_set-MIN_NUM_FORMS': '0',
                'itemfilemodel_set-MAX_NUM_FORMS': '1000',
                'itemfilemodel_set-__prefix__-position': '0',

                'itemlinkmodel_set-TOTAL_FORMS': '0',
                'itemlinkmodel_set-INITIAL_FORMS': '0',
                'itemlinkmodel_set-MIN_NUM_FORMS': '0',
                'itemlinkmodel_set-MAX_NUM_FORMS': '1000',
                'itemlinkmodel_set-__prefix__-position': '0',

                '_save': 'Save',
            },
        )
        self.assertRedirects(response, expected_url='/admin/inventory/itemmodel/')

        data = list(ItemModel.objects.values_list('kind__name', 'name'))
        assert data == [('kind', 'name')]

        item = ItemModel.objects.first()

        self.assert_messages(response, expected_messages=[
            f'The Item “<a href="/admin/inventory/itemmodel/{item.pk}/change/"> - name</a>”'
            ' was added successfully.'
        ])

        assert item.user_id == self.normaluser.pk

    def test_new_item_with_image(self):
        """
        https://github.com/jedie/PyInventory/issues/33
        """
        self.client.force_login(self.normaluser)

        img = ImageDummy(width=1, height=1, format='png').in_memory_image_file(filename='test.png')

        response = self.client.post(
            path='/admin/inventory/itemmodel/add/',
            data={
                'kind': 'kind',
                'name': 'name',

                'itemimagemodel_set-TOTAL_FORMS': '1',
                'itemimagemodel_set-INITIAL_FORMS': '0',
                'itemimagemodel_set-MIN_NUM_FORMS': '0',
                'itemimagemodel_set-MAX_NUM_FORMS': '1000',
                'itemimagemodel_set-0-position': '0',
                'itemimagemodel_set-__prefix__-position': '0',
                'itemimagemodel_set-0-image': img,

                'itemfilemodel_set-TOTAL_FORMS': '0',
                'itemfilemodel_set-INITIAL_FORMS': '0',
                'itemfilemodel_set-MIN_NUM_FORMS': '0',
                'itemfilemodel_set-MAX_NUM_FORMS': '1000',
                'itemfilemodel_set-__prefix__-position': '0',

                'itemlinkmodel_set-TOTAL_FORMS': '0',
                'itemlinkmodel_set-INITIAL_FORMS': '0',
                'itemlinkmodel_set-MIN_NUM_FORMS': '0',
                'itemlinkmodel_set-MAX_NUM_FORMS': '1000',
                'itemlinkmodel_set-__prefix__-position': '0',

                '_save': 'Save',
            },
        )
        self.assertRedirects(response, expected_url='/admin/inventory/itemmodel/')

        data = list(ItemModel.objects.values_list('kind__name', 'name'))
        assert data == [('kind', 'name')]

        item = ItemModel.objects.first()

        self.assert_messages(response, expected_messages=[
            f'The Item “<a href="/admin/inventory/itemmodel/{item.pk}/change/"> - name</a>”'
            ' was added successfully.'
        ])

        assert item.user_id == self.normaluser.pk

        assert ItemImageModel.objects.count() == 1
        image = ItemImageModel.objects.first()
        assert image.name == 'test.png'
        assert image.item == item
        assert image.user_id == self.normaluser.pk

    def test_auto_group_items(self):
        self.client.force_login(self.normaluser)

        offset = datetime.timedelta(minutes=1)
        with mock.patch.object(timezone, 'now', MockDatetimeGenerator(offset=offset)):
            for main_item_no in range(1, 3):
                main_item = ItemModel.objects.create(
                    id=f'00000000-000{main_item_no}-0000-0000-000000000000',
                    user=self.normaluser,
                    name=f'main item {main_item_no}'
                )
                main_item.full_clean()
                for sub_item_no in range(1, 3):
                    sub_item = ItemModel.objects.create(
                        id=f'00000000-000{main_item_no}-000{sub_item_no}-0000-000000000000',
                        user=self.normaluser,
                        parent=main_item,
                        name=f'sub item {main_item_no}.{sub_item_no}'
                    )
                    sub_item.full_clean()

        names = list(ItemModel.objects.order_by('id').values_list('name', flat=True))
        assert names == [
            'main item 1', 'sub item 1.1', 'sub item 1.2',
            'main item 2', 'sub item 2.1', 'sub item 2.2',
        ]

        # Default mode, without any GET parameter -> group "automatic":

        with mock.patch.object(CsrfTokenNode, 'render', return_value='MockedCsrfTokenNode'), \
                self.assertLogs(logger='inventory', level=logging.DEBUG) as logs:
            response = self.client.get(
                path='/admin/inventory/itemmodel/',
            )
            assert response.status_code == 200
        self.assert_html_parts(response, parts=(
            f'<title>Select Item to change | PyInventory v{__version__}</title>',

            '<a href="/admin/inventory/itemmodel/00000000-0001-0000-0000-000000000000/change/">'
            'main item 1</a>',

            '<li><a href="/admin/inventory/itemmodel/00000000-0001-0001-0000-000000000000/change/">'
            'sub item 1.1</a></li>',
        ))
        assert logs.output == [
            'INFO:inventory.admin.item:Group items: True (auto mode: True)',
            'DEBUG:inventory.admin.item:Display sub items inline',
            'DEBUG:inventory.admin.item:Display sub items inline'
        ]
        assert_html_response_snapshot(response=response, validate=False)

        # Search should disable grouping:

        with mock.patch.object(CsrfTokenNode, 'render', return_value='MockedCsrfTokenNode'), \
                self.assertLogs(logger='inventory', level=logging.DEBUG) as logs:
            response = self.client.get(
                path='/admin/inventory/itemmodel/?q=sub+item+2.',
            )
            assert response.status_code == 200
        self.assert_html_parts(response, parts=(
            '<input type="text" size="40" name="q" value="sub item 2." id="searchbar" autofocus>',
            '2 results (<a href="?">6 total</a>)',

            '<a href="/admin/inventory/itemmodel/00000000-0002-0001-0000-000000000000/change/">'
            'sub item 2.1</a>',

            '<a href="/admin/inventory/itemmodel/00000000-0002-0002-0000-000000000000/change/">'
            'sub item 2.2</a>',
        ))
        assert logs.output == [
            # grouping disabled?
            'INFO:inventory.admin.item:Group items: False (auto mode: True)'
        ]
        assert_html_response_snapshot(response=response, validate=False)
