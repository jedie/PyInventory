import os
import tempfile

import pytest
from PIL import Image


# Avoid django.core.exceptions.SynchronousOnlyOperation:
os.environ.setdefault('DJANGO_ALLOW_ASYNC_UNSAFE', '1')


@pytest.fixture(scope='session')
def browser_context_args(browser_context_args):
    browser_context_args['ignore_https_errors'] = True
    return browser_context_args


@pytest.fixture(scope='function')
def png_image():
    format = 'png'
    with tempfile.NamedTemporaryFile(prefix='test_image', suffix=f'.{format}') as tmp:
        image_size = (1, 1)
        pil_image = Image.new('RGB', image_size)
        pil_image.save(tmp, format=format)
        tmp.seek(0)
        yield tmp
