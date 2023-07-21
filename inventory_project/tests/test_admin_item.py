import datetime
from unittest import mock

from bx_django_utils.test_utils.datetime import MockDatetimeGenerator
from bx_django_utils.test_utils.html_assertion import HtmlAssertionMixin, assert_html_response_snapshot
from bx_py_utils.test_utils.snapshot import assert_html_snapshot
from django.template.defaulttags import CsrfTokenNode, NowNode
from django.test import TestCase, override_settings
from django.utils import timezone
from django_tools.unittest_utils.mockup import ImageDummy
from override_storage import locmem_stats_override_storage
from reversion.models import Revision

from inventory.models import ItemImageModel, ItemModel
from inventory_project.tests.fixtures import get_normal_user
from inventory_project.tests.mocks import MockInventoryVersionString


ITEM_FORM_DEFAULTS = {
    'version': 0,  # VersionProtectBaseModel field
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
}
ITEM_FORM_DEFAULTS = tuple(ITEM_FORM_DEFAULTS.items())


@override_settings(SECURE_SSL_REDIRECT=True)
class AdminAnonymousTests(HtmlAssertionMixin, TestCase):
    def test_login(self):
        # HTTP -> HTTPS redirect:
        response = self.client.get('/admin/', HTTP_ACCEPT_LANGUAGE='en')
        self.assertRedirects(
            response,
            expected_url='https://testserver/admin/',
            status_code=301,  # Permanent redirect
            fetch_redirect_response=False,
        )

        response = self.client.get(path='/admin/inventory/itemmodel/add/', secure=True, HTTP_ACCEPT_LANGUAGE='en')
        self.assertRedirects(
            response, expected_url='/admin/login/?next=/admin/inventory/itemmodel/add/', fetch_redirect_response=False
        )
        with mock.patch.object(
            CsrfTokenNode, 'render', return_value='MockedCsrfTokenNode'
        ), MockInventoryVersionString():
            response = self.client.get(path='/admin/login/', secure=True, HTTP_ACCEPT_LANGUAGE='en')
            self.assert_html_parts(
                response,
                parts=(
                    '<title>Log in | PyInventory vMockedVersionString</title>',
                    '<label class="required" for="id_username">Username:</label>',
                    '<label class="required" for="id_password">Password:</label>',
                ),
            )
        assert_html_response_snapshot(response, validate=False)


@override_settings(SECURE_SSL_REDIRECT=False)
class AdminTestCase(HtmlAssertionMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.normaluser = get_normal_user()

    def test_normal_user_create_minimal_item(self):
        offset = datetime.timedelta(minutes=1)
        with mock.patch.object(timezone, 'now', MockDatetimeGenerator(offset=offset)), mock.patch.object(
            NowNode, 'render', return_value='MockedNowNode'
        ), mock.patch.object(
            CsrfTokenNode, 'render', return_value='MockedCsrfTokenNode'
        ), MockInventoryVersionString():
            self.client.force_login(self.normaluser)

            response = self.client.get('/admin/inventory/itemmodel/add/')
            assert response.status_code == 200
            self.assert_html_parts(response, parts=('<title>Add Item | PyInventory vMockedVersionString</title>',))
            assert_html_response_snapshot(response=response, validate=False)

            assert ItemModel.objects.count() == 0

            post_data = dict(ITEM_FORM_DEFAULTS)
            response = self.client.post(
                path='/admin/inventory/itemmodel/add/',
                data=post_data,
            )
            assert response.status_code == 302, response.content.decode('utf-8')  # Form error?
            self.assertRedirects(response, expected_url='/admin/inventory/itemmodel/')

            data = list(ItemModel.objects.values_list('kind__name', 'name', 'version'))
            assert data == [('kind', 'name', 2)]  # FIXME: Save call done two times!

            item = ItemModel.objects.first()

            self.assert_messages(
                response,
                expected_messages=[
                    f'The Item “<a href="/admin/inventory/itemmodel/{item.pk}/change/">name</a>”'
                    ' was added successfully.'
                ],
            )

            assert item.user_id == self.normaluser.pk

            # Test django-tools VersionProtectBaseModel integration:

            assert item.version == 2  # current Version in DB
            post_data['version'] = 1  # Try to overwrite with older version
            post_data['name'] = 'A new Name!'
            response = self.client.post(
                path=f'/admin/inventory/itemmodel/{item.pk}/change/',
                data=post_data,
            )
            self.assert_html_parts(
                response,
                parts=(
                    '<title>Change Item | PyInventory vMockedVersionString</title>',
                    '<li>Version error: Overwrite version 2 with 1 is forbidden!</li>',
                    '<pre>- &quot;name&quot;\n+ &quot;A new Name!&quot;</pre>',
                ),
            )
            html = response.content.decode('utf-8')
            html = html.replace(str(item.pk), '<removed-UUID>')
            assert_html_snapshot(got=html, validate=False)

        # django-revision integration:
        comments = list(Revision.objects.order_by('date_created').values_list('comment', flat=True))
        self.assertEqual(comments, ['Added.'])

    def test_new_item_with_image(self):
        """
        https://github.com/jedie/PyInventory/issues/33
        """
        self.client.force_login(self.normaluser)

        img = ImageDummy(width=1, height=1, format='png').in_memory_image_file(filename='test.png')

        post_data = dict(ITEM_FORM_DEFAULTS)
        post_data.update(
            {
                'itemimagemodel_set-TOTAL_FORMS': '1',
                'itemimagemodel_set-0-position': '0',
                'itemimagemodel_set-0-image': img,
            }
        )

        with locmem_stats_override_storage() as storage_stats:
            response = self.client.post(
                path='/admin/inventory/itemmodel/add/',
                data=post_data,
            )
            self.assertRedirects(response, expected_url='/admin/inventory/itemmodel/')

            data = list(ItemModel.objects.values_list('kind__name', 'name'))
            assert data == [('kind', 'name')]

            item = ItemModel.objects.first()

            self.assert_messages(
                response,
                expected_messages=[
                    f'The Item “<a href="/admin/inventory/itemmodel/{item.pk}/change/">name</a>”'
                    ' was added successfully.'
                ],
            )

            assert item.user_id == self.normaluser.pk

            assert ItemImageModel.objects.count() == 1
            image = ItemImageModel.objects.first()
            assert image.name == 'test.png'
            assert image.item == item
            assert image.user_id == self.normaluser.pk

            # Test image file should be stored:
            self.assertEqual(storage_stats.save_cnt, 1)

    def test_auto_group_items(self):
        self.client.force_login(self.normaluser)

        offset = datetime.timedelta(minutes=1)
        with mock.patch.object(timezone, 'now', MockDatetimeGenerator(offset=offset)):
            for main_item_no in range(1, 3):
                main_item = ItemModel.objects.create(
                    id=f'00000000-000{main_item_no}-0000-0000-000000000000',
                    user=self.normaluser,
                    name=f'main item {main_item_no}',
                )
                main_item.full_clean()
                for sub_item_no in range(1, 3):
                    sub_item = ItemModel.objects.create(
                        id=f'00000000-000{main_item_no}-000{sub_item_no}-0000-000000000000',
                        user=self.normaluser,
                        parent=main_item,
                        name=f'sub item {main_item_no}.{sub_item_no}',
                    )
                    sub_item.full_clean()

        names = list(ItemModel.objects.order_by('id').values_list('name', flat=True))
        assert names == [
            'main item 1',
            'sub item 1.1',
            'sub item 1.2',
            'main item 2',
            'sub item 2.1',
            'sub item 2.2',
        ]

        with mock.patch.object(NowNode, 'render', return_value='MockedNowNode'), mock.patch.object(
            CsrfTokenNode, 'render', return_value='MockedCsrfTokenNode'
        ), MockInventoryVersionString():
            response = self.client.get(
                path='/admin/inventory/itemmodel/',
            )
            assert response.status_code == 200
        self.assert_html_parts(
            response,
            parts=(
                '<title>Select Item to change | PyInventory vMockedVersionString</title>',
                '<a href="/admin/inventory/itemmodel/00000000-0001-0000-0000-000000000000/change/">'
                '<strong>main item 1</strong></a>',
                '<a href="/admin/inventory/itemmodel/00000000-0001-0001-0000-000000000000/change/">'
                'main item 1 › <strong>sub item 1.1</strong></a>',
            ),
        )
        assert_html_response_snapshot(response=response, validate=False)
