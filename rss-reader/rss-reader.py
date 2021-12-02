import argparse
import json
import bs4.element
import requests
import logging
import re
import pathlib

from pathlib import Path
from bs4 import BeautifulSoup
from datetime import datetime

arguments = argparse.ArgumentParser()
arguments.version = 'Version 1.0'
arguments.add_argument("source", help="RSS link", default="https://news.yahoo.com/rss/")
arguments.add_argument("--version", action="version", help="Print version info")
arguments.add_argument("--verbose", action="store_true", help="Outputs verbose status messages")
arguments.add_argument("--json", action="store_true", help="Print result as JSON in stdout")
arguments.add_argument("--limit", action='store', type=int, default=200,
                       help="Limit news topics if this parameter provided")

args = arguments.parse_args()
lim = 200

parsed_data = {
    "title": "",
    "pubdate": "",
    "link": "",
    "media": [],
}
list_media = []

file_name = 'null.json'

if args.verbose:
    print('log information in job')

if args.limit:
    print(f'the limit for news topics is {args.limit}')
    lim = args.limit

if args.json:
    curr_time = datetime.now()
    file_name = (f'{curr_time.date().year}' + '_' + f'{curr_time.date().month}' + '_' + f'{curr_time.date().day}' +
              '_' + f'{curr_time.time().hour}' + '_' + f'{curr_time.time().minute}' + '_' + f'{curr_time.time().second}' +
              '.json')
    dir_path = Path(pathlib.Path(), 'data', file_name)
    print('news directed to file: ' + f'{dir_path}')

def out_parsed_data(list_pd, file_name):
    if args.json:
        with open(dir_path, "a") as outfile:
            json.dump(list_pd, outfile)
            outfile.write("\n")
    else:
        print('\nTitle: ' + list_pd["title"])
        print('Date: ' + list_pd["pubdate"])
        print('Link: ' + list_pd["link"])
        print('Media: ')
        lis = list_pd['media']
        for l1 in lis:
            print(f'{l1}' + '\n')
        print("\n")

def parse_feed(news_list, limit):
    pubdate_pattern = r"pubdate|pubDate"
    link_pattern = r"http://|https://"
    media_pattern = r"media:content|enclosure"

    for get_feed in news_list:
        list_media.clear()
        parsed_data["title"] = get_feed.title.text
        for news in get_feed.contents:
            if type(news) == bs4.element.NavigableString:
                if re.search(link_pattern, f'{news}', re.IGNORECASE):
                    parsed_data["link"] = news
            if type(news) == bs4.element.CData:
                if re.search(link_pattern, f'{news}', re.IGNORECASE):
                    parsed_data["link"] = f'{news}'
            if type(news) == bs4.element.Tag:
                if news.text:
                    if re.search(pubdate_pattern, f'{news}', re.IGNORECASE):
                        parsed_data["pubdate"] = news.text
                    if re.search(media_pattern, f'{news}', re.IGNORECASE):
                        if news.attrs:
                            list_media.append(news.attrs['url'])
                        else:
                            ghh = news.text.split("href=")
                            del ghh[0]
                            for gh in ghh:
                                g = gh.split("target")
                                list_media.append(g[0])
                        parsed_data["media"] = list_media
                else:
                    if re.search(media_pattern, f'{news}', re.IGNORECASE):
                        ghh = news.attrs['url']
                        list_media.append(ghh)
                        parsed_data["media"] = list_media

        if limit > 0:
            out_parsed_data(parsed_data, file_name)
            limit -= 1


def parse(link, limit):

    try:
        resp = requests.get(link)
    except:
        return link + ' can not be load'

    soup_page = BeautifulSoup(resp.content, "html.parser")
    news_list = soup_page.findAll("item")

    parse_feed(news_list, limit)

    return 0


#print(parse("https://habr.com/ru/rss/hubs/all/", 3))
parse(args.source, args.limit)
