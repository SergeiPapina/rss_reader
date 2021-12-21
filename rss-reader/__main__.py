from .rss_reader import RssReaderClass

if __name__ == '__main__':
    rss = RssReaderClass()
    args = rss.get_args()
    rss.parse(args.source, args.limit)
