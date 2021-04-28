from bx_py_utils.test_utils.html_assertion import HtmlAssertionMixin
from django.contrib.auth.models import User
from django.test import TestCase
from django_tools.unittest_utils.mockup import ImageDummy
from model_bakery import baker

from inventory import __version__
from inventory.models import ItemImageModel, ItemModel
from inventory.permissions import get_or_create_normal_user_group


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
            User, is_staff=True, is_active=True, is_superuser=False
        )
        assert cls.normaluser.user_permissions.count() == 0
        group = get_or_create_normal_user_group()[0]
        cls.normaluser.groups.set([group])

    def test_normal_user_create_minimal_item(self):
        self.client.force_login(self.normaluser)

        response = self.client.get('/admin/inventory/itemmodel/add/')
        assert response.status_code == 200
        self.assert_html_parts(response, parts=(
            f'<title>Add Item | PyInventory v{__version__}</title>',
        ))

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
            f'The Item "<a href="/admin/inventory/itemmodel/{item.pk}/change/"> - name</a>"'
            f' was added successfully.'
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
            f'The Item "<a href="/admin/inventory/itemmodel/{item.pk}/change/"> - name</a>"'
            f' was added successfully.'
        ])

        assert item.user_id == self.normaluser.pk

        assert ItemImageModel.objects.count() == 1
        image = ItemImageModel.objects.first()
        assert image.name == 'test.png'
        assert image.item == item
        assert image.user_id == self.normaluser.pk
