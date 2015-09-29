import rssr.persistent
import feedparser
import os
import glob


_dir = os.path.abspath(os.path.dirname(__file__))

def test_format():
    
    for filename in glob.glob(os.path.join(_dir, 'samples/sample_feed*')):
        with open(filename) as data:
            d = feedparser.parse(data.read()).entries
            for item in d:
                # Just execute to check "format" working collectly.
                print(rssr.persistent.format(item))
