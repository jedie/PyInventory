"""
    Remove this if https://github.com/boxine/bx_py_utils/pull/95 merged!
"""
from pathlib import Path

import pytest
from bs4 import BeautifulSoup
from bx_py_utils.test_utils.snapshot import assert_text_snapshot
from django.http import HttpResponse
from lxml import html


def validate_html(data):
    parser = html.HTMLParser(
        recover=False,  # Crash faster on broken HTML
    )
    parser.feed(data)
    parser.close()


def test_validate_html():
    validate_html('<p>Test</p>')
    validate_html('<a><b/></a>')

    from lxml.etree import XMLSyntaxError
    with pytest.raises(XMLSyntaxError) as exc_info:
        validate_html('<p> >broken< </p>')
    assert exc_info.value.args[0] == 'htmlParseStartTag: invalid element name, line 1, column 13'


def pretty_format_html(data):
    soup = BeautifulSoup(data, 'html.parser')
    return soup.prettify(
        formatter=None  # Do not perform any substitution
    )


def test_pretty_format_html():
    assert pretty_format_html('<p>Test</p>') == '<p>\n Test\n</p>'

    html = pretty_format_html('''
         \r\n <h1>X</h1> \r\n \r\n
        <p><strong>Test</strong></p> \r\n \r\n
    ''')
    assert html == '<h1>\n X\n</h1>\n<p>\n <strong>\n  Test\n </strong>\n</p>\n'


def assert_html_response_snapshot(
    response: HttpResponse,
    status_code: int = 200,
    **kwargs
):
    data = response.content.decode('utf-8')

    validate_html(data)
    data = pretty_format_html(data)

    assert_text_snapshot(
        got=data,
        extension='.html',
        self_file_path=Path(__file__),
        **kwargs
    )
    assert response.status_code == status_code, (
        f'Status code is {response.status_code} but excepted {status_code}'
    )
