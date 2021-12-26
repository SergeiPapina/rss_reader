import pytest

from datetime import datetime
from pathlib import Path

from rss_reader.rss_parser import RssParserClass

@pytest.fixture
def rss_reader_object():
    return RssParserClass()

def test_set_data_file_name(mocker, rss_reader_object):
    arg_link = "https://yandex.ru/rss"
    date_mock = mocker.patch("rss_reader.rss_parser.datetime")
    date_mock.now.return_value = datetime(year=2021, month=12, day=23, hour=12, minute=23, second=48)
    rss_reader_object.data_dir = "c:\\dir"
    rss_reader_object.set_data_file_name(arg_link)
    assert rss_reader_object._data_path == Path(rss_reader_object.data_dir, "2021_12_23_yandex-ru_12_23_48.json")
