import rssr.persistent
import feedparser
import os


_dir = os.path.abspath(os.path.dirname(__file__))

def test_format():

    with open(os.path.join(_dir, 'samples/sample_feed01.atom')) as data:
        d = feedparser.parse(data.read()).entries
        for item in d:
            # Just execute to check "format" working collectly.
            print(rssr.persistent.format(item))
