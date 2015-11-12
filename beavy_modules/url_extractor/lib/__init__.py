
from beavy.app import cache
from .fetching import lassie

@cache.memoize()
def extract_info(url):
    return lassie.fetch(url)
