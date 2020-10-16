import pytest
from django.test import TestCase


@pytest.mark.django_db
class AdminAnonymousTests(TestCase):
    """
    Anonymous will be redirected to the login page.
    """

    def test_login_en(self):
        response = self.client.get("/admin/", HTTP_ACCEPT_LANGUAGE="en")
        self.assertRedirects(response, expected_url="/admin/login/?next=/admin/")

    def test_login_de(self):
        response = self.client.get("/admin/", HTTP_ACCEPT_LANGUAGE="de")
        self.assertRedirects(response, expected_url="/admin/login/?next=/admin/")
