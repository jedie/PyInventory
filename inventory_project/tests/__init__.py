import os
import sys
import unittest.util
from pathlib import Path

import django
from bx_py_utils.test_utils.deny_requests import deny_any_real_request
from manage_django_project.config import project_info


def pre_configure_tests() -> None:
    print(f'Configure unittests via "load_tests Protocol" from {Path(__file__).relative_to(Path.cwd())}')

    # Hacky way to display more "assert"-Context in failing tests:
    _MIN_MAX_DIFF = unittest.util._MAX_LENGTH - unittest.util._MIN_DIFF_LEN
    unittest.util._MAX_LENGTH = int(os.environ.get('UNITTEST_MAX_LENGTH', 300))
    unittest.util._MIN_DIFF_LEN = unittest.util._MAX_LENGTH - _MIN_MAX_DIFF

    # Deny any request via docket/urllib3 because tests they should mock all requests:
    deny_any_real_request()

    project_info.initialize()

    DJANGO_SETTINGS_MODULE = project_info.config.test_settings
    print(f'Set {DJANGO_SETTINGS_MODULE=}', file=sys.stderr)
    os.environ['DJANGO_SETTINGS_MODULE'] = DJANGO_SETTINGS_MODULE

    django.setup()


def load_tests(loader, tests, pattern):
    """
    Use unittest "load_tests Protocol" as a hook to setup test environment before running tests.
    https://docs.python.org/3/library/unittest.html#load-tests-protocol
    """
    pre_configure_tests()
    return loader.discover(start_dir=Path(__file__).parent, pattern=pattern)
