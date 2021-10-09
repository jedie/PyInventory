import datetime
import logging
from unittest.mock import patch

import requests_mock
from bx_django_utils.test_utils.datetime import MockDatetimeGenerator
from bx_py_utils.test_utils.datetime import parse_dt
from django.test import TestCase
from django.utils import timezone
from model_bakery import baker

from inventory.models import ItemLinkModel, ItemModel


class ItemLinkModelTestCase(TestCase):
    def test_set_name_by_request(self):
        with self.assertLogs('django_tools'):
            item = baker.make(ItemModel)

            link = ItemLinkModel(
                item=item,
                url='http://test.tld/foo/bar'
            )

            offset = datetime.timedelta(seconds=30)
            with patch.object(timezone, 'now', MockDatetimeGenerator(offset)):
                with requests_mock.Mocker() as m:
                    m.get('http://test.tld/foo/bar', text='No title')

                    assert link.last_check is None
                    with self.assertLogs('inventory.models.links', level=logging.WARNING) as logs:
                        link.full_clean()
                        assert link.page_title is None
                        assert link.name is None
                        assert link.last_check == parse_dt('2000-01-01T00:00:30+0000')

                    logs = logs.output
                    assert logs == [
                        "WARNING:inventory.models.links:No title found in 'http://test.tld/foo/bar'"
                    ]

                    # We should not create request on every admin save call

                    with self.assertLogs('inventory.models.links', level=logging.DEBUG) as logs:
                        link.full_clean()
                        assert link.page_title is None
                        assert link.name is None

                    logs = logs.output
                    assert logs == [
                        'DEBUG:inventory.models.links:Last check is 0:00:30 ago.',
                        "INFO:inventory.models.links:Skip request for: 'http://test.tld/foo/bar'"
                    ]

                    # Next try after 1 Min

                    m.get('http://test.tld/foo/bar', text='<title>A <boom>Title</boom>!</title>')
                    with self.assertLogs('inventory.models.links', level=logging.INFO) as logs:
                        link.full_clean()
                        assert link.page_title == 'A Title!'
                        assert link.name == 'A Title!'

                    logs = logs.output
                    assert logs == [
                        "INFO:inventory.models.links:Found title: 'A <boom>Title</boom>!'"
                    ]

                # Don't make requests, if we have a link name!

                with requests_mock.Mocker():
                    with self.assertLogs('inventory.models.links', level=logging.DEBUG) as logs:
                        link.full_clean()
                        assert link.page_title == 'A Title!'
                        assert link.name == 'A Title!'

                    logs = logs.output
                    assert logs == [
                        (
                            "DEBUG:inventory.models.links:Skip link request:"
                            " because we have a name: 'A Title!'"
                        )
                    ]
