import logging
import os
import json
import pandas as pd

from pathlib import Path

from .helper import settings

logger = logging.getLogger(settings.project_name)


class CashFeedParser:
    """Class for parsing feeds from folder home_directory/rss_data"""

    html_path = ''

    def _out_parsed_data(self, out_data):
        """this method outputs parsed from cash information to console"""
        print('\nTitle: ', out_data["title"])
        print('Date: ', out_data["pubdate"])
        print('Link: ', out_data["link"])
        print('Media: ')
        for list_item_media in out_data['media']:
            print(f'{list_item_media}' + '\n')
        logger.info('news item printed to console')

    def _get_feed_date(self, feed_date):

        month_stamp = {
            'Jan': 1,
            'Feb': 2,
            'Mar': 3,
            'Apr': 4,
            'May': 5,
            'Jun': 6,
            'Jul': 7,
            'Aug': 8,
            'Sep': 9,
            'Oct': 10,
            'Nov': 11,
            'Dec': 12
        }

        if not feed_date:
            return ""

        if feed_date[4] == " ":
            feed_day = feed_date[5:7]
            feed_year = feed_date[12:16]
            feed_month = month_stamp[feed_date[8:11]]
            date_to_compare = f'{feed_year}{feed_month}{feed_day}'
            return date_to_compare

        if feed_date[4] == "-":
            feed_day = feed_date[8:10]
            feed_year = feed_date[:4]
            feed_month = feed_date[5:7]
            date_to_compare = f'{feed_year}{feed_month}{feed_day}'
            return date_to_compare

    def get_cashed_news(self, input_args, data_dir):

        source_link = input_args.source
        news_date = input_args.date
        limit = input_args.limit
        data_to_convert = []

        logger.info(f'preparing cashed news with publication date: {news_date}')
        if source_link == 'all':
            for file in os.listdir(data_dir):
                try:
                    file.index('json')
                    with open(Path(data_dir, file)) as json_file:
                        for line in json_file:
                            one_feed = json.loads(line)
                            date_from_feed = self._get_feed_date(one_feed['pubdate'])
                            if date_from_feed == news_date:
                                if limit == 0:
                                    logger.info('news output limit reached')
                                    # df = pd.DataFrame(data_to_convert)
                                    # df.to_html(self.html_path)
                                    return 0

                                data_to_convert.append(one_feed)
                                if not input_args.verbose:
                                    self._out_parsed_data(one_feed)
                                limit -= 1
                except ValueError:
                    pass

                if self.html_path:
                    df = pd.DataFrame(data_to_convert)
                    df.to_html(self.html_path)
        else:
            for file in os.listdir(data_dir):
                name_link = source_link.split('/')
                pattern_name_link = name_link[2].replace(".", "-")
                try:
                    file.index(pattern_name_link)
                    file.index('json')
                    with open(Path(data_dir, file)) as json_file:
                        for line in json_file:
                            one_feed = json.loads(line)
                            date_from_feed = self._get_feed_date(one_feed['pubdate'])
                            if date_from_feed == news_date:
                                if limit == 0:
                                    logger.info('news output limit reached')
                                    return 0

                                data_to_convert.append(one_feed)
                                if not input_args.verbose:
                                    self._out_parsed_data(one_feed)
                                limit -= 1
                    if self.html_path:
                        df = pd.DataFrame(data_to_convert)
                        df.to_html(self.html_path)
                except ValueError:
                    pass

        if limit == input_args.limit:
            logger.info("there are not news for selected source and date,"
                        "try to use 'all' as source or another date")
        return 0
