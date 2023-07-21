from unittest import mock

from bx_django_utils.test_utils.html_assertion import HtmlAssertionMixin, assert_html_response_snapshot
from django.template.defaulttags import CsrfTokenNode, NowNode
from django.test import TestCase, override_settings

from inventory_project.tests.fixtures import get_normal_user
from inventory_project.tests.mocks import MockInventoryVersionString


@override_settings(SECURE_SSL_REDIRECT=False)
class AdminTestCase(HtmlAssertionMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.normaluser = get_normal_user()

    def test_empty_change_list(self):
        self.client.force_login(self.normaluser)
        with mock.patch.object(NowNode, 'render', return_value='MockedNowNode'), mock.patch.object(
            CsrfTokenNode, 'render', return_value='MockedCsrfTokenNode'
        ), MockInventoryVersionString():
            response = self.client.get(
                path='/admin/inventory/locationmodel/',
            )
            assert response.status_code == 200
        self.assert_html_parts(
            response,
            parts=(
                '<title>Select Location to change | PyInventory vMockedVersionString</title>',
                '<a href="/admin/inventory/locationmodel/add/" class="addlink">Add Location</a>',
                '<p class="paginator">0 Locations</p>',
            ),
        )
        assert_html_response_snapshot(response=response, validate=False)
