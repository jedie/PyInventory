from pathlib import Path

from bx_py_utils.test_utils.snapshot import assert_html_snapshot
from django.http import HttpResponse


def assert_html_response_snapshot(
    response: HttpResponse,
    status_code: int = 200,
    validate: bool = True,
):
    """
    TODO: Move to bx_django_utils
    """
    data = response.content.decode('utf-8')

    assert response.status_code == status_code, (
        f'Status code is {response.status_code} but excepted {status_code}'
    )

    assert_html_snapshot(
        got=data,
        self_file_path=Path(__file__),
        validate=validate
    )
