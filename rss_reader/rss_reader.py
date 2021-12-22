import argparse
import json
import bs4.element
import requests
import re
import pathlib
import os
import logging

from pathlib import Path
from bs4 import BeautifulSoup
from datetime import datetime


class RssReaderClass:
    _parsed_data = {
        "title": "",
        "pubdate": "",
        "link": "",
        "media": [],
    }
    _list_media = []
    _flag_json = False
    _flag_verbose = False
    _log_dir = str(Path.home() / 'rss_log')
    _data_dir = str(Path.home() / 'rss_data')
    _data_path = ''
    _log_path = ''

    def __init__(self):
        # argparse setup
        self.arguments = argparse.ArgumentParser()
        self.arguments.version = 'Version 1.2'
        self.arguments.add_argument("source", help="RSS link", default="https://news.yahoo.com/rss/")
        self.arguments.add_argument("--version", action="version", help="Print version info")
        self.arguments.add_argument("--verbose", action="store_true", help="Outputs verbose status messages")
        self.arguments.add_argument("--json", action="store_true", help="Print result as JSON in stdout")
        self.arguments.add_argument("--limit", action='store', type=int, default=200,
                                    help="Limit news topics if this parameter provided")
        # check existing data directory, create if needed
        self._check_dir()
        # logger setup
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        logger_stdout_handler = logging.StreamHandler()
        self._log_path = Path(self._log_dir, 'rss_log.log')
        logger_file_handler = logging.FileHandler(self._log_path)
        logger_stdout_handler.setLevel(logging.WARNING)
        logger_file_handler.setLevel(logging.INFO)
        logger_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        logger_file_handler.setFormatter(logger_formatter)
        self.logger.addHandler(logger_file_handler)
        self.logger.addHandler(logger_stdout_handler)
        self.logger.info('\nlog begin')

    def _check_dir(self):
        if not Path(self._data_dir).exists():
            os.mkdir(self._data_dir)
        if not Path(self._log_dir).exists():
            os.mkdir(self._log_dir)

    def get_args(self):
        input_args = self.arguments.parse_args()

        if input_args.verbose:
            self._flag_verbose = True
            logger_stdout_handler = logging.StreamHandler()
            logger_stdout_handler.setLevel(logging.INFO)
            self.logger.addHandler(logger_stdout_handler)
            self.logger.info(f'log information printed to stdout')

        if input_args.limit:
            self.logger.info(f'the limit for news topics is {input_args.limit}')

        if input_args.json:
            self._flag_json = True
            curr_time = datetime.now()
            file_name = (
                    f'{curr_time.date().year}' + '_' + f'{curr_time.date().month}' + '_' + f'{curr_time.date().day}'
                    + '_' + f'{curr_time.time().hour}' + '_' + f'{curr_time.time().minute}' + '_' +
                    f'{curr_time.time().second}' + '.json'
            )
            self._data_path = Path(self._data_dir, file_name)
            self.logger.info('news directed to file: ' + f'{self._data_path}')

        return input_args

    def _out_parsed_data(self, list_pd):
        if self._flag_json:
            try:
                with open(self._data_path, "a") as outfile:
                    json.dump(list_pd, outfile)
                    outfile.write("\n")
                self.logger.info('news saved to file: ' + f'{self._data_path}')
            except IndentationError:
                self.logger.error('JSON file cannot be created')
        else:
            print('\nTitle: ' + list_pd["title"])
            print('Date: ' + list_pd["pubdate"])
            print('Link: ' + list_pd["link"])
            print('Media: ')
            lis = list_pd['media']
            for l1 in lis:
                print(f'{l1}' + '\n')
            print("\n")
            self.logger.info('news printed to console')

    def _parse_feed(self, news_list, limit):
        pubdate_pattern = r"pubdate|pubDate"
        link_pattern = r"http://|https://"
        media_pattern = r"media:content|enclosure"

        for get_feed in news_list:
            self._list_media.clear()
            self._parsed_data["title"] = get_feed.title.text
            for news in get_feed.contents:
                if type(news) == bs4.element.NavigableString:
                    if re.search(link_pattern, f'{news}', re.IGNORECASE):
                        self._parsed_data["link"] = news
                if type(news) == bs4.element.CData:
                    if re.search(link_pattern, f'{news}', re.IGNORECASE):
                        self._parsed_data["link"] = f'{news}'
                if type(news) == bs4.element.Tag:
                    if news.text:
                        if re.search(pubdate_pattern, f'{news}', re.IGNORECASE):
                            self._parsed_data["pubdate"] = news.text
                        if re.search(media_pattern, f'{news}', re.IGNORECASE):
                            if news.attrs:
                                self._list_media.append(news.attrs['url'])
                            else:
                                news_link = news.text.split("href=")
                                del news_link[0]
                                for gh in news_link:
                                    g = gh.split("target")
                                    self._list_media.append(g[0])
                            self._parsed_data["media"] = self._list_media
                    else:
                        if re.search(media_pattern, f'{news}', re.IGNORECASE):
                            new_link = news.attrs['url']
                            self._list_media.append(new_link)
                            self._parsed_data["media"] = self._list_media

            if limit > 0:
                self._out_parsed_data(self._parsed_data)
                limit -= 1

    def parse(self, link, limit):

        try:
            resp = requests.get(link)
        except RuntimeError:
            self.logger.error('content by link does not exist')
            return 0

        soup_page = BeautifulSoup(resp.content, "html.parser")
        news_list = soup_page.findAll("item")

        self._parse_feed(news_list, limit)
        self.logger.info('parse is successfully done')
        return 0


def main():
    rss = RssReaderClass()
    args = rss.get_args()
    print(args)
    rss.parse(args.source, args.limit)


if __name__ == '__main__':
    main()
