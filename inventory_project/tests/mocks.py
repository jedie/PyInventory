from unittest import mock

from bx_py_utils.test_utils.context_managers import MassContextManager

from inventory import context_processors


class MockInventoryVersionString(MassContextManager):
    def __init__(self):
        self.mocks = [
            mock.patch.object(context_processors, '__version__', self),
        ]

    def __repr__(self):
        return 'MockedVersionString'
