import pytest

from datetime import datetime
from pathlib import Path

from rss_reader.rss_parser import RssParserClass


@pytest.fixture
def rss_reader_object():
    return RssParserClass()


@pytest.mark.parametrize(
    "source_link, expected_filename",
    [
        (
            "https://yandex.ru/rss",
            "2021_12_23_yandex-ru_12_23_48.json"
        ),
        (
            "https://google.com/rss",
            "2021_12_23_google-com_12_23_48.json"
        )
    ],
)
def test_set_data_file_name(mocker, rss_reader_object, source_link, expected_filename):
    arg_link = source_link
    date_mock = mocker.patch("rss_reader.rss_parser.datetime")
    date_mock.now.return_value = datetime(year=2021, month=12, day=23, hour=12, minute=23, second=48)
    rss_reader_object.data_dir = "c:\\dir"
    rss_reader_object.set_data_file_name(arg_link)
    assert rss_reader_object._data_path == Path(rss_reader_object.data_dir, expected_filename)


def test_parse_with_parse_feed(mocker, rss_reader_object):
    # Given
    response_text = """<?xml version="1.0" encoding="UTF-8"?>
                        <rss xmlns:media="http://search.yahoo.com/mrss/" version="2.0">
                        <channel>
                        <title>Yahoo News - Latest News &amp; Headlines</title>
                        <link>https://www.yahoo.com/news</link>
                        <description>The latest news and headlines from Yahoo! News. Get breaking news stories and in-d
                        epth
                         coverage with videos and photos.</description>
                        <language>en-US</language>
                        <copyright>Copyright (c) 2021 Yahoo! Inc. All rights reserved</copyright>
                        <pubDate>Sun, 26 Dec 2021 08:01:42 -0500</pubDate>
                        <ttl>5</ttl><image><title>Yahoo News - Latest News &amp; Headlines</title>
                        <link>https://www.yahoo.com/news</link>
                        <url>http://l.yimg.com/rz/d/yahoo_news_en-US_s_f_p_168x21_news.png</url></image>
                        <item><title>Alex Jones' wife arrested on domestic violence charge</title>
                        <link>https://news.yahoo.com/alex-jones-wife-arrested-domestic-204930217.html</link>
                        <pubDate>2021-12-25T20:49:30Z</pubDate>
                        <source url="http://www.ap.org/">Associated Press</source>
                        <guid isPermaLink="false">alex-jones-wife-arrested-domestic-204930217.html</guid>
                        <media:content height="86" url="https://s.yimg.com/" width="130"/>
                        <media:credit role="publishing company"/>
                        </item>
                        </channel>
                        </rss>"""

    dict_need = {
        'title': "Alex Jones' wife arrested on domestic violence charge",
        'pubdate': '2021-12-25T20:49:30Z',
        'link': 'https://news.yahoo.com/alex-jones-wife-arrested-domestic-204930217.html\n                        ',
        'media':
            ['https://s.yimg.com/',
             ]
    }

    input_args_mock = mocker.MagicMock(name="input_args_mock")
    input_args_mock.source = "https://yandex.com/rss"
    input_args_mock.limit = 5

    resp_mock = mocker.MagicMock(name="resp_mock")
    resp_mock.content = response_text

    requests_mock = mocker.patch("rss_reader.rss_parser.requests")
    requests_mock.get.return_value = resp_mock

    out_parsed_data_mock = mocker.patch("rss_reader.rss_parser.RssParserClass._out_parsed_data")

    # When
    return_value = rss_reader_object.parse(input_args_mock)

    # Then
    assert return_value == 0
    assert dict_need == rss_reader_object._parsed_data
    out_parsed_data_mock.assert_called_once()


def test_out_parsed_data_flag_json_false(mocker, rss_reader_object):
    # Given
    dict_need = {
        'title': "Alex Jones' wife arrested on domestic violence charge",
        'pubdate': '2021-12-25T20:49:30Z',
        'link': 'https://news.yahoo.com/alex-jones-wife-arrested-domestic-204930217.html\n                    ',
        'media':
            ['https://s.yimg.com/uu/api/res/1.2/fH2d5KVDBklSDjZAqAEwDQ--~B/aD0yNDIyO3c9MzYzMzthcHBpZD15dGFjaHlvbg--'
             '/https://media.zenfs.com/en/ap.org/1595587ae18e78690dd32c16469db9f2'
             ]
    }
    log_info_mock = mocker.patch("rss_reader.rss_parser.logger.info")

    # When
    rss_reader_object._out_parsed_data(dict_need)

    # Then
    log_info_mock.assert_called_with('news item printed to console')


def test_out_parsed_data_flag_json_true_no_error(mocker, rss_reader_object):
    # Given
    dict_need = {
        'title': "Alex Jones' wife arrested on domestic violence charge",
        'pubdate': '2021-12-25T20:49:30Z',
        'link': 'https://news.yahoo.com/alex-jones-wife-arrested-domestic-204930217.html\n                    ',
        'media':
            ['https://s.yimg.com/uu/api/res/1.2/fH2d5KVDBklSDjZAqAEwDQ--~B/aD0yNDIyO3c9MzYzMzthcHBpZD15dGFjaHlvbg--'
             '/https://media.zenfs.com/en/ap.org/1595587ae18e78690dd32c16469db9f2'
             ]
    }
    rss_reader_object.flag_json = True
    rss_reader_object._data_path = "c:\\"
    log_info_mock = mocker.patch("rss_reader.rss_parser.logger.info")
    mocker.patch("rss_reader.rss_parser.open")
    mocker.patch("rss_reader.rss_parser.json")

    # When
    rss_reader_object._out_parsed_data(dict_need)

    # Then
    log_info_mock.assert_called_with('news item saved to file: c:\\')


def test_out_parsed_data_flag_json_true_with_error(mocker, rss_reader_object):
    # Given
    dict_need = {}
    rss_reader_object.flag_json = True
    rss_reader_object._data_path = "c:\\"
    log_info_mock = mocker.patch("rss_reader.rss_parser.logger.error")
    open_mock = mocker.patch("rss_reader.rss_parser.open")
    open_mock.side_effect = FileNotFoundError

    # When
    rss_reader_object._out_parsed_data(dict_need)

    # Then
    log_info_mock.assert_called_with('JSON file cannot be created, ')
