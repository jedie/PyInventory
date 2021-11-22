from unittest import mock

from bx_django_utils.test_utils.html_assertion import HtmlAssertionMixin
from django.contrib.auth.models import User
from django.template.defaulttags import CsrfTokenNode, NowNode
from django.test import TestCase
from django_tools.unittest_utils.mockup import ImageDummy
from model_bakery import baker

from inventory import __version__
from inventory.models import MemoImageModel, MemoModel
from inventory.permissions import get_or_create_normal_user_group
from inventory_project.tests.temp_utils import assert_html_response_snapshot


class AdminAnonymousTests(TestCase):
    def test_login(self):
        response = self.client.get('/admin/inventory/memomodel/add/', HTTP_ACCEPT_LANGUAGE='en')
        self.assertRedirects(
            response,
            expected_url='/admin/login/?next=/admin/inventory/memomodel/add/'
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

        with mock.patch.object(NowNode, 'render', return_value='MockedNowNode'), \
                mock.patch.object(CsrfTokenNode, 'render', return_value='MockedCsrfTokenNode'):
            response = self.client.get('/admin/inventory/memomodel/add/')
        assert response.status_code == 200
        self.assert_html_parts(response, parts=(
            f'<title>Add Memo | PyInventory v{__version__}</title>',
        ))
        assert_html_response_snapshot(response=response, validate=False)

        assert MemoModel.objects.count() == 0

        response = self.client.post(
            path='/admin/inventory/memomodel/add/',
            data={
                'version': 0,  # VersionProtectBaseModel field
                'name': 'The Memo Name',
                'memo': 'This is a test Memo',

                'memoimagemodel_set-TOTAL_FORMS': '0',
                'memoimagemodel_set-INITIAL_FORMS': '0',
                'memoimagemodel_set-MIN_NUM_FORMS': '0',
                'memoimagemodel_set-MAX_NUM_FORMS': '1000',
                'memoimagemodel_set-__prefix__-position': '0',

                'memofilemodel_set-TOTAL_FORMS': '0',
                'memofilemodel_set-INITIAL_FORMS': '0',
                'memofilemodel_set-MIN_NUM_FORMS': '0',
                'memofilemodel_set-MAX_NUM_FORMS': '1000',
                'memofilemodel_set-__prefix__-position': '0',

                'memolinkmodel_set-TOTAL_FORMS': '0',
                'memolinkmodel_set-INITIAL_FORMS': '0',
                'memolinkmodel_set-MIN_NUM_FORMS': '0',
                'memolinkmodel_set-MAX_NUM_FORMS': '1000',
                'memolinkmodel_set-__prefix__-position': '0',

                '_save': 'Save',
            },
        )
        assert response.status_code == 302, response.content.decode('utf-8')  # Form error?
        self.assertRedirects(response, expected_url='/admin/inventory/memomodel/')

        data = list(MemoModel.objects.values_list('name', 'memo'))
        assert data == [('The Memo Name', 'This is a test Memo')]

        item = MemoModel.objects.first()

        self.assert_messages(response, expected_messages=[
            f'The Memo “<a href="/admin/inventory/memomodel/{item.pk}/change/">The Memo Name</a>”'
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
            path='/admin/inventory/memomodel/add/',
            data={
                'version': 0,  # VersionProtectBaseModel field
                'name': 'The Memo Name',
                'memo': 'This is a test Memo',

                'memoimagemodel_set-TOTAL_FORMS': '1',
                'memoimagemodel_set-INITIAL_FORMS': '0',
                'memoimagemodel_set-MIN_NUM_FORMS': '0',
                'memoimagemodel_set-MAX_NUM_FORMS': '1000',
                'memoimagemodel_set-0-position': '0',
                'memoimagemodel_set-__prefix__-position': '0',
                'memoimagemodel_set-0-image': img,

                'memofilemodel_set-TOTAL_FORMS': '0',
                'memofilemodel_set-INITIAL_FORMS': '0',
                'memofilemodel_set-MIN_NUM_FORMS': '0',
                'memofilemodel_set-MAX_NUM_FORMS': '1000',
                'memofilemodel_set-__prefix__-position': '0',

                'memolinkmodel_set-TOTAL_FORMS': '0',
                'memolinkmodel_set-INITIAL_FORMS': '0',
                'memolinkmodel_set-MIN_NUM_FORMS': '0',
                'memolinkmodel_set-MAX_NUM_FORMS': '1000',
                'memolinkmodel_set-__prefix__-position': '0',

                '_save': 'Save',
            },
        )
        assert response.status_code == 302, response.content.decode('utf-8')  # Form error?
        memo = MemoModel.objects.first() or MemoModel()
        self.assert_messages(response, expected_messages=[
            f'The Memo “<a href="/admin/inventory/memomodel/{memo.pk}/change/">The Memo Name</a>”'
            ' was added successfully.'
        ])
        self.assertRedirects(response, expected_url='/admin/inventory/memomodel/')

        data = list(MemoModel.objects.values_list('name', 'memo'))
        assert data == [('The Memo Name', 'This is a test Memo')]

        assert memo.user_id == self.normaluser.pk

        assert MemoImageModel.objects.count() == 1
        image = MemoImageModel.objects.first()
        assert image.name == 'test.png'
        assert image.memo == memo
        assert image.user_id == self.normaluser.pk
