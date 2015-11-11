import lassie
from pyembed.core import PyEmbed

from beavy.app import cache

pyembed = PyEmbed()

@cache.memoize()
def extract_info(url):
    return lassie.fetch(url)


@cache.memoize()
def extract_oembed(url, **kwargs):
    return pyembed.embed('http://www.youtube.com/watch?v=_PEdPBEpQfY', **kwargs)
