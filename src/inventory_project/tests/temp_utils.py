"""
    Remove this if https://github.com/boxine/bx_py_utils/pull/95 merged!
"""
import inspect
from pathlib import Path

import pytest
from bs4 import BeautifulSoup
from bx_py_utils.test_utils.snapshot import assert_text_snapshot
from django.http import HttpResponse
from lxml import etree
from lxml.etree import XMLSyntaxError


def cutout(text, line_no, column, extra_lines=2):
    assert isinstance(text, str)
    assert line_no >= 0
    assert column >= 0
    assert extra_lines >= 0

    lines = text.splitlines()
    line_count = len(lines)

    assert line_no <= line_count

    from_line = line_no - extra_lines - 1
    if from_line < 0:
        from_line = 0

    to_line = line_no + extra_lines
    if to_line > line_count:
        to_line = line_count

    line_no_width = len(str(from_line)) + 1

    lines = lines[from_line: to_line]
    result = []
    for no, line in enumerate(lines, from_line + 1):
        result.append(
            f'{no:0{line_no_width}} {line}'
        )
        if no == line_no:
            result.append(
                f'{"-"*(line_no_width+column+1)}^'
            )

    return '\n'.join(result)


def test_cutout():
    text = inspect.cleandoc('''
        line 1
        line 2
        01234567890 line 3
        line 4
        line 5
    ''')

    output = cutout(text, line_no=3, column=5, extra_lines=1)
    assert output == inspect.cleandoc('''
        02 line 2
        03 01234567890 line 3
        --------^
        04 line 4
    ''')

    output = cutout(text, line_no=3, column=1, extra_lines=0)
    assert output == inspect.cleandoc('''
        03 01234567890 line 3
        ----^
    ''')

    output = cutout(text, line_no=3, column=10, extra_lines=2)
    assert output == inspect.cleandoc('''
        01 line 1
        02 line 2
        03 01234567890 line 3
        -------------^
        04 line 4
        05 line 5
    ''')

    text = '\n'.join(f'The Line {no}' for no in range(20))
    output = cutout(text, line_no=18, column=9, extra_lines=2)
    assert output == inspect.cleandoc('''
        016 The Line 15
        017 The Line 16
        018 The Line 17
        -------------^
        019 The Line 18
        020 The Line 19
    ''')


class InvalidHtml(AssertionError):
    """
    XMLSyntaxError with better error messages: used in validate_html()
    """

    def __init__(self, *args):
        self.args = args

        data, origin_err = args
        assert isinstance(data, str)
        assert isinstance(origin_err, XMLSyntaxError)

        self.origin_msg = origin_err.msg

        line_no, column = origin_err.position
        self.cutoput_text = cutout(data, line_no, column, extra_lines=3)

    def __str__(self):
        return (
            f'{self.origin_msg}\n'
            f'{"-"*80}\n'
            f'{self.cutoput_text}\n'
            f'{"-"*80}'
        )


def validate_html(data, **parser_kwargs):
    parser = etree.XMLParser(**parser_kwargs)
    try:
        parser.feed(data)
        parser.close()
    except XMLSyntaxError as err:
        raise InvalidHtml(data, err)


def test_validate_html():
    validate_html('<p>Test</p>')
    validate_html('<a><b/></a>')

    validate_html('<foo></foo>')
    validate_html('<nav></nav>')
    validate_html('<nav class="sticky" id="nav-sidebar"></nav>')

    with pytest.raises(InvalidHtml) as exc_info:
        validate_html(inspect.cleandoc('''
            <no-html>
                <foo>
                    <bar>
                        <h1>Test</h1>
                        <p> >broken< </p>
                        <p>the end</p>
                    <bar>
                </foo>
            </no-html>
        '''))
    error_message = str(exc_info.value)
    assert error_message == inspect.cleandoc('''
        StartTag: invalid element name, line 5, column 25
        --------------------------------------------------------------------------------
        02     <foo>
        03         <bar>
        04             <h1>Test</h1>
        05             <p> >broken< </p>
        ----------------------------^
        06             <p>the end</p>
        07         <bar>
        08     </foo>
        --------------------------------------------------------------------------------
    ''')


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
    validate: bool = True,
    **kwargs
):
    data = response.content.decode('utf-8')

    if validate:
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
