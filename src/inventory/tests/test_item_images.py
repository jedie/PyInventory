import tempfile
from unittest import mock

from django.http import FileResponse
from django.test import TestCase, override_settings
from model_bakery import baker

from inventory.models import ItemImageModel
from inventory.tests.fixtures.users import get_normal_pyinventory_user


class ItemImagesTestCase(TestCase):
    def test_basics(self):
        pyinventory_user1 = get_normal_pyinventory_user(id=1)
        pyinventory_user2 = get_normal_pyinventory_user(id=2)

        with tempfile.TemporaryDirectory() as tmpdir, override_settings(MEDIA_ROOT=tmpdir):
            print(tmpdir)

            with self.assertLogs('inventory') as logs:
                with mock.patch('inventory.models.item.get_random_string', return_value='DrgCCsMrdIBJ'):
                    image_instance = baker.make(
                        ItemImageModel,
                        user=pyinventory_user1,
                        _create_files=True
                    )
                assert image_instance.image is not None
                url = image_instance.image.url
                # url = f'/media/{image_instance.image}'
                assert url == '/media/user_1/DrgCCsMrdIBJ/mock_img.jpeg'
                assert logs.output == [
                    "INFO:inventory.models.item:"
                    "Upload filename: 'user_1/DrgCCsMrdIBJ/mock_img.jpeg'"
                ]

            # Anonymous user can't access:

            with self.assertLogs('inventory') as logs, self.assertLogs('django'):
                response = self.client.get(url)
                assert response.status_code == 403
            assert logs.output == [
                'ERROR:inventory.views.media_files:Anonymous try to access files from: 1'
            ]

            # Wrong user should not access:

            self.client.force_login(user=pyinventory_user2)

            with self.assertLogs('inventory') as logs, self.assertLogs('django'):
                response = self.client.get(url)
                assert response.status_code == 403
            assert logs.output == [
                'ERROR:inventory.views.media_files:Wrong user ID: 2 is not 1'
            ]

            # The right user should access:

            self.client.force_login(user=pyinventory_user1)

            response = self.client.get(url)
            assert response.status_code == 200
            assert isinstance(response, FileResponse)
            assert response.getvalue() == image_instance.image.read()
