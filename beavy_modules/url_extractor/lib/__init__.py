
from beavy.app import cache
from .fetching import lassie, pyembed

@cache.memoize()
def extract_info(url):
    return lassie.fetch(url)

@cache.memoize()
def extract_oembed(url, **kwargs):
    return pyembed.embed(url, **kwargs)
