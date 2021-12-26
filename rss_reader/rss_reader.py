import argparse
import logging

from .helper import settings
from .cash_parser import CashFeedParser
from .rss_parser import RssParserClass

logger = logging.getLogger(settings.project_name)


def get_args(list_args):
    """this method realise processing of input arguments"""

    input_args = list_args.parse_args()

    if input_args.verbose:
        logger_stdout_handler = logging.StreamHandler()
        logger_stdout_handler.setLevel(logging.INFO)
        logger.addHandler(logger_stdout_handler)
        logger.info(f'log information printed to console')

    if input_args.limit:
        logger.info(f'the limit for news topics is {input_args.limit}')

    if input_args.json:
        logger.info('news directed to cash directory')

    if input_args.date:
        logger.info(f'module be search news feed in cashed files by date: {input_args.date}')

    if input_args.to_html:
        logger.info('news be converted to HTML file')

    return input_args


def main():
    logger.info('execution begin')

    # argparse setup
    arguments = argparse.ArgumentParser()
    arguments.version = 'Version 1.3'
    arguments.add_argument("source", help="RSS link, use 'all' with argument --data to search in all sources",
                           default="all")
    arguments.add_argument("--version", action="version", help="Print version info")
    arguments.add_argument("--verbose", action="store_true", help="Outputs verbose status messages")
    arguments.add_argument("--json", action="store_true", help="Print result as JSON in stdout")
    arguments.add_argument("--limit", action='store', type=int, default=200,
                           help="Limit news topics if this parameter provided")
    arguments.add_argument("--date", action='store', type=str,
                           help="Date to select cashed news topics if this parameter provided")
    arguments.add_argument("--to-html", action="store", type=str, help="convert data feed to HTML file")

    args = get_args(arguments)
    rss = RssParserClass()
    rss.data_dir = settings.data_dir
    rss.flag_json = args.json

    rss_cash = CashFeedParser()
    if rss.flag_json:
        rss.set_data_file_name(args.source)

    if args.to_html:
        rss.html_path = args.to_html
        rss_cash.html_path = args.to_html

    if not args.date:
        rss.parse(args)

    if args.date:
        rss_cash.get_cashed_news(args, settings.data_dir)


if __name__ == '__main__':
    main()
