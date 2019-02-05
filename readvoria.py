"""readvoria - reads news from voria.gr"""

import configparser
import feedparser
import pprint
import os
import sqlite3
from contextlib import closing

URL = 'http://www.voria.gr/rss'
database_file = 'database.sqlite3'


class FeedEntry:
    def __init__(self, title, link, summary=None, content=None):
        self.title = title
        self.link = link
        self.summary = summary
        self.content = content

    def __repr__(self):
        return f'{self.__class__.__name__}("{self.title}", "{self.link}", summary="{self.summary}", ' \
            f'content="{self.content}")'


schema_sql = """
CREATE TABLE FeedEntries (
    uri TEXT PRIMARY KEY,
    text TEXT
);
"""


def create_database(*, force=True):
    if force:
        try:
            os.remove(database_file)
        except OSError:
            pass
    with closing(sqlite3.connect(database_file)) as conn:
        cfp = configparser.ConfigParser()
        cfp.read('readvoria.ini')
        create_sql = cfp.get('sql', 'create', raw=True)
        conn.executescript(create_sql)
        conn.commit()


def get_rss_feed():
    feed = feedparser.parse(URL)
    return [FeedEntry(feed_entry['title'], feed_entry['link'], summary=feed_entry['summary'])
            for feed_entry in feed['entries']]


if __name__ == '__main__':
    create_database(force=False)
    rss_feed = get_rss_feed()
    pprint.pprint(rss_feed)
    latest = rss_feed.pop()
