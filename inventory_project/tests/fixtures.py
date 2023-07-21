import tempfile

from django.contrib.auth.models import User
from model_bakery import baker
from PIL import Image

from inventory.permissions import get_or_create_normal_user_group


def get_normal_user():
    user = baker.make(
        User,
        id=1,
        username='NormalUser',
        is_staff=True,
        is_active=True,
        is_superuser=False,
    )
    assert user.user_permissions.count() == 0
    group = get_or_create_normal_user_group()[0]
    user.groups.set([group])
    user.full_clean()
    return user


class TempImageFile:
    def __init__(self, prefix='test_image', format='png', size=(1, 1)):
        self.format = format
        self.image_size = size
        self.temp = tempfile.NamedTemporaryFile(prefix=prefix, suffix=f'.{format}')

    def __enter__(self):
        self.temp_file = self.temp.__enter__()
        pil_image = Image.new('RGB', self.image_size)
        pil_image.save(self.temp_file, format=self.format)
        self.temp_file.seek(0)
        return self.temp_file

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.temp_file.__exit__(exc_type, exc_val, exc_tb)
