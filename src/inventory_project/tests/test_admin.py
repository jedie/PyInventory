from django.test import TestCase


class AdminAnonymousTests(TestCase):
    """
    Anonymous will be redirected to the login page.
    """

    def test_login_en(self):
        response = self.client.get('/admin/', secure=True, HTTP_ACCEPT_LANGUAGE='en')
        self.assertRedirects(
            response, expected_url='/admin/login/?next=/admin/', fetch_redirect_response=False
        )

    def test_login_de(self):
        response = self.client.get('/admin/', secure=True, HTTP_ACCEPT_LANGUAGE='de')
        self.assertRedirects(
            response, expected_url='/admin/login/?next=/admin/', fetch_redirect_response=False
        )
