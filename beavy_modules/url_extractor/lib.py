
from pyembed.core import PyEmbed

from beavy.app import cache

from lassie import Lassie
import re

# lassie by default isn't extensive enough for us
# configure it so that it is.

from lassie.filters import FILTER_MAPS
FILTER_MAPS['meta']['open_graph']['map'].update({
    # general
    "og:type": "type",
    "og:site_name": "site_name",
})

FILTER_MAPS['meta']['generic']['pattern'] = re.compile(r"^(description|keywords|title|author|article:|music:|video:|book:)", re.I)
FILTER_MAPS['meta']['generic']['map'].update({
    # articles
    "article:published_time": "published_time",
    "article:modified_time": "modified_time",
    "article:expiration_time": "expiration_time",
    "article:section": "section",
    "article:section_url": "section_url",

    # music
    "music:duration": "duration",
    "music:release_date": "release_date",

    # video
    "video:duration": "duration",
    "video:release_date": "release_date",

    # author
    "author": "author",

    # book
    "book:author": "author",
    "book:isbn": "isbn",
    "book:release_date": "release_date",
})

# general configuration
pyembed = PyEmbed()

lassie = Lassie()
lassie.request_opts = {
    'headers':{
        # tell Lassie to tell others it is facebook
        'User-Agent': 'facebookexternalhit/1.1'
    }
}

@cache.memoize()
def extract_info(url):
    return lassie.fetch(url)


@cache.memoize()
def extract_oembed(url, **kwargs):
    return pyembed.embed(url, **kwargs)
