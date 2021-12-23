import argparse
import json
import bs4.element
import requests
import re
import os
import logging

from pathlib import Path
from bs4 import BeautifulSoup
from datetime import datetime


class RssReaderClass:
    """Class for parsing news feeds from RSS"""

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
        self.arguments.version = 'Version 1.3'
        self.arguments.add_argument("source", help="RSS link", default="https://news.yahoo.com/rss/")
        self.arguments.add_argument("--version", action="version", help="Print version info")
        self.arguments.add_argument("--verbose", action="store_true", help="Outputs verbose status messages")
        self.arguments.add_argument("--json", action="store_true", help="Print result as JSON in stdout")
        self.arguments.add_argument("--limit", action='store', type=int, default=200,
                                    help="Limit news topics if this parameter provided")

        # check existing data and log directory, create if needed
        self._check_dir()

        # logger setup
        self._set_log_file_name()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        logger_stdout_handler = logging.StreamHandler()
        logger_file_handler = logging.FileHandler(self._log_path)
        logger_stdout_handler.setLevel(logging.WARNING)
        logger_file_handler.setLevel(logging.INFO)
        logger_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        logger_file_handler.setFormatter(logger_formatter)
        self.logger.addHandler(logger_file_handler)
        self.logger.addHandler(logger_stdout_handler)
        self.logger.info('log begin')

    def _check_dir(self):
        """the method to control directories for logging and data cashing"""
        if not Path(self._data_dir).exists():
            os.mkdir(self._data_dir)
        if not Path(self._log_dir).exists():
            os.mkdir(self._log_dir)

    def _set_data_file_name(self, arg_link):
        """this method to format an easy-to-read file name for data cashing"""
        curr_time = datetime.now()
        name_link = arg_link.split('/')
        str_name_link = name_link[2].replace(".", "-")
        file_name = (
                f'{curr_time.date().year}' + '_' + f'{curr_time.date().month}' + '_' + f'{curr_time.date().day}'
                + '_' + f'{str_name_link}' + '_' + f'{curr_time.time().hour}' + '_' + f'{curr_time.time().minute}'
                + '_' + f'{curr_time.time().second}' + '.json'
        )
        self._data_path = Path(self._data_dir, file_name)

    def _set_log_file_name(self):
        """this method to format an easy-to-read file name for logging"""
        curr_time = datetime.now()
        file_name = (
                f'{curr_time.date().year}' + '_' + f'{curr_time.date().month}' + '_' + f'{curr_time.date().day}'
                + '_' + f'{curr_time.time().hour}' + '_' + f'{curr_time.time().minute}'
                + '_' + f'{curr_time.time().second}' + 'rss_log.log'
        )
        self._log_path = Path(self._log_dir, file_name)

    def _out_parsed_data(self, out_data):
        """this method outputs parsed information to console or data file,
           depends on input argument --json"""
        if self._flag_json:
            try:
                with open(self._data_path, "a") as outfile:
                    json.dump(out_data, outfile)
                    outfile.write("\n")
                self.logger.info('news item saved to file: ' + f'{self._data_path}')
            except IndentationError:
                self.logger.error('JSON file cannot be created')
        else:
            print('\nTitle: ', out_data["title"])
            print('Date: ', out_data["pubdate"])
            print('Link: ', out_data["link"])
            print('Media: ')
            for list_item_media in out_data['media']:
                print(f'{list_item_media}' + '\n')
            self.logger.info('news item printed to console')

    def _parse_feed(self, news_list, limit):
        """this method produce parsed information from the RSS item until the limit
           argument will not be reached. the limit depends on input argument --limit """
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
            if limit == 0:
                self.logger.info('news output limit reached')
                break

            self._out_parsed_data(self._parsed_data)
            limit -= 1

    def parse(self, link, limit):
        """this method produce RSS items from the RSS link"""
        try:
            resp = requests.get(link)
        except RuntimeError:
            self.logger.error('content by link does not exist, parse did not execute')
            return 0

        soup_page = BeautifulSoup(resp.content, "html.parser")
        news_list = soup_page.findAll("item")

        self._parse_feed(news_list, limit)
        self.logger.info('parse is successfully done')
        return 0

    def get_args(self):
        """this method realise processing of input arguments"""
        input_args = self.arguments.parse_args()

        if input_args.verbose:
            self._flag_verbose = True
            logger_stdout_handler = logging.StreamHandler()
            logger_stdout_handler.setLevel(logging.INFO)
            self.logger.addHandler(logger_stdout_handler)
            self.logger.info(f'log information printed to console')

        if input_args.limit:
            self.logger.info(f'the limit for news topics is {input_args.limit}')

        if input_args.json:
            self._flag_json = True
            self._set_data_file_name(input_args.source)
            self.logger.info('news directed to file: ' + f'{self._data_path}')

        return input_args


def main():
    rss = RssReaderClass()
    args = rss.get_args()
    rss.parse(args.source, args.limit)


if __name__ == '__main__':
    main()
