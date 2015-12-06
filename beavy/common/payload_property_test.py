
from .payload_property import PayloadProperty

# from unittest import mock


class TestObject():

    def __init__(self):
        self.payload = {}

    title = PayloadProperty("title")
    header_o = PayloadProperty("other", "content.header")
    header_p = PayloadProperty("p", "content.header")


def test_simple(mocker):
    TestObject.title.flag_modified = mocker.MagicMock()
    t = TestObject()
    assert t.payload == {}
    t.title = "test"
    assert t.payload == {'title': 'test'}
    TestObject.title.flag_modified.assert_called_once_with(t, "payload")


def test_deeper(mocker):
    TestObject.header_o.flag_modified = mocker.MagicMock()
    TestObject.header_p.flag_modified = mocker.MagicMock()
    t = TestObject()
    assert t.payload == {}
    t.header_o = "oh. header"
    assert t.payload == {'content': {'header': {"other": 'oh. header'}}}
    TestObject.header_o.flag_modified.assert_called_with(t, "payload")
