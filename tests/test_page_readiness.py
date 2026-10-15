import pytest

from parser_2gis.parser.parsers.main import MainParser


class _FakeRemote:
    def __init__(self, result):
        self.result = result
        self.expression = ''

    def execute_script(self, expression):
        self.expression = expression
        return self.result


def _parser_with_remote(result):
    parser = object.__new__(MainParser)
    parser._chrome_remote = _FakeRemote(result)
    return parser


def test_page_readiness_uses_document_state_not_xhr_counter():
    parser = _parser_with_remote(True)

    assert parser._page_is_ready(timeout=0, poll_interval=0) is True
    assert 'document.readyState' in parser._chrome_remote.expression
    assert 'openHTTPs' not in parser._chrome_remote.expression


def test_page_readiness_timeout_is_non_fatal():
    parser = _parser_with_remote(False)

    assert parser._page_is_ready(timeout=0, poll_interval=0) is False


class _PageRemote:
    def __init__(self, title, body):
        self.title = title
        self.body = body

    def execute_script(self, expression):
        return self.title if expression == 'document.title' else self.body


def test_captcha_is_reported_explicitly_without_bypass():
    parser = object.__new__(MainParser)
    parser._chrome_remote = _PageRemote(
        '2GIS Captcha',
        'Мы заметили подозрительную активность. Подтвердите, что вы не робот.',
    )

    with pytest.raises(RuntimeError, match='не обходит CAPTCHA'):
        parser._raise_if_access_blocked()


def test_normal_page_is_not_reported_as_captcha():
    parser = object.__new__(MainParser)
    parser._chrome_remote = _PageRemote('Аптеки в Москве', 'Результаты поиска')

    parser._raise_if_access_blocked()
