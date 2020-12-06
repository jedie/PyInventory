import tempfile
from unittest import mock

from django.http import FileResponse
from django.test import TestCase, override_settings
from django_tools.serve_media_app.models import UserMediaTokenModel
from model_bakery import baker

from inventory.models import ItemImageModel
from inventory.tests.fixtures.users import get_normal_pyinventory_user


class ItemImagesTestCase(TestCase):
    def test_basics(self):
        with mock.patch('secrets.token_urlsafe', return_value='user1token'):
            pyinventory_user1 = get_normal_pyinventory_user(id=1)

        with mock.patch('secrets.token_urlsafe', return_value='user2token'):
            pyinventory_user2 = get_normal_pyinventory_user(id=2)

        token1_instance = UserMediaTokenModel.objects.get(user=pyinventory_user1)
        assert repr(token1_instance) == (
            f"<UserMediaTokenModel: user:1 token:'user1token' ({token1_instance.pk})>"
        )
        token2_instance = UserMediaTokenModel.objects.get(user=pyinventory_user2)
        assert repr(token2_instance) == (
            f"<UserMediaTokenModel: user:2 token:'user2token' ({token2_instance.pk})>"
        )

        with tempfile.TemporaryDirectory() as temp:
            with override_settings(MEDIA_ROOT=temp):
                with mock.patch('secrets.token_urlsafe', return_value='12345678901234567890'):
                    image_instance = baker.make(
                        ItemImageModel,
                        user=pyinventory_user1,
                        _create_files=True
                    )

                assert image_instance.image is not None
                url = image_instance.image.url
                assert url == '/media/user1token/12345678901234567890/mock_img.jpeg'

                # Anonymous has no access:
                response = self.client.get('/media/user1token/12345678901234567890/mock_img.jpeg')
                assert response.status_code == 403

                # Can't access with wrong user:
                self.client.force_login(pyinventory_user2)
                response = self.client.get('/media/user1token/12345678901234567890/mock_img.jpeg')
                assert response.status_code == 403

                # Can access with the right user:
                self.client.force_login(pyinventory_user1)
                response = self.client.get('/media/user1token/12345678901234567890/mock_img.jpeg')
                assert response.status_code == 200
                assert isinstance(response, FileResponse)
                assert response.getvalue() == image_instance.image.open('rb').read()

                # Test whats happen, if token was deleted
                UserMediaTokenModel.objects.all().delete()
                response = self.client.get('/media/user1token/12345678901234567890/mock_img.jpeg')
                assert response.status_code == 400  # SuspiciousOperation -> HttpResponseBadRequest
