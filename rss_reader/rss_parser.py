import json
import bs4.element
import requests
import re
import logging

from pathlib import Path
from bs4 import BeautifulSoup
from datetime import datetime
from .helper import settings

logger = logging.getLogger(settings.project_name)


class RssParserClass:
    """Class for parsing news feeds from RSS"""

    def __init__(self):
        self._parsed_data = {
            "title": "",
            "pubdate": "",
            "link": "",
            "media": [],
        }
        self._list_media = []
        self._data_path = ''

        self.flag_json = False
        self.data_dir = ''

    def set_data_file_name(self, arg_link):
        """this method to format an easy-to-read file name for data cashing"""
        if arg_link != 'all':
            curr_time = datetime.now()
            name_link = arg_link.split('/')
            str_name_link = name_link[2].replace(".", "-")
            file_name = (
                    f'{curr_time.date().year}' + '_' + f'{curr_time.date().month}' + '_' + f'{curr_time.date().day}'
                    + '_' + f'{str_name_link}' + '_' + f'{curr_time.time().hour}' + '_' + f'{curr_time.time().minute}'
                    + '_' + f'{curr_time.time().second}' + '.json'
            )
            self._data_path = Path(self.data_dir, file_name)

    def _out_parsed_data(self, out_data):
        """this method outputs parsed information to console or data file,
           depends on input argument --json"""
        if self.flag_json:
            try:
                with open(self._data_path, "a") as outfile:
                    json.dump(out_data, outfile)
                    outfile.write("\n")
                logger.info('news item saved to file: ' + f'{self._data_path}')
            except FileNotFoundError as file_error:
                print('path', self._data_path)
                logger.error(f'JSON file cannot be created, {file_error}')
        else:
            print('\nTitle: ', out_data["title"])
            print('Date: ', out_data["pubdate"])
            print('Link: ', out_data["link"])
            print('Media: ')
            for list_item_media in out_data['media']:
                print(f'{list_item_media}' + '\n')
            logger.info('news item printed to console')

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
                logger.info('news output limit reached')
                break

            self._out_parsed_data(self._parsed_data)
            limit -= 1

    def parse(self, input_args):
        """this method produce RSS items from the RSS link"""
        link = input_args.source
        limit = input_args.limit
        try:
            resp = requests.get(link)
        except RuntimeError:
            logger.error('content by link does not exist, parse did not execute')
            return 0

        soup_page = BeautifulSoup(resp.content, "html.parser")
        news_list = soup_page.findAll("item")

        self._parse_feed(news_list, limit)
        logger.info('parse is successfully done')
        return 0
