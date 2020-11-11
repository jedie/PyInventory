import logging

from bx_py_utils.filename import clean_filename
from django.utils.crypto import get_random_string


logger = logging.getLogger(__name__)


def get_filename(filename, request):
    random_string = get_random_string()
    filename = clean_filename(filename)
    filename = f'{random_string}/{filename}'
    logger.info(f'Upload filename: {filename!r}')
    return filename
