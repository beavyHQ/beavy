
from beavy.app import cache
from .fetching import extractor

@cache.memoize()
def extract_info(url):
    return extractor.fetch(url)
