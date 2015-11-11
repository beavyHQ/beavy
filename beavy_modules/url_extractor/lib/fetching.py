from pyembed.core import PyEmbed

from lassie.core import Lassie
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

class AmazonISBNFinder():
    def _check(self, data):
        return data.get("type", None) == 'book' and data.get("site_name", "").lower().startswith("amazon.")

    def __call__(self, soup, data, url=None):
        if not self._check(data): return
        # amazon hides the ISBN inside the keywords
        # title + 1 => publisher
        # title + 2 => ISBN
        # everything after => categories

        try:
            title_idx = data["keywords"].index(data['title'])
            data.update({
                "authors": data["keywords"][:title_idx],
                "publisher": data["keywords"][title_idx + 1],
                "ISBN": data["keywords"][title_idx + 2],
                "categories": data["keywords"][title_idx + 3:]
            })
        except (ValueError, KeyError):
            # not found. ignored.
            pass



class PostProcessingLassie(Lassie):

    POST_PROCESSORS = [
        AmazonISBNFinder()
    ]

    def _filter_meta_data(self, source, soup, data, url=None):
        super(PostProcessingLassie, self)._filter_meta_data(source, soup, data, url=url)

        if source == "generic":
            # we are in the last generic parsing,
            # do the post_processing
            for processor in self.POST_PROCESSORS:
                processor(soup, data, url=url)

        return data

lassie = PostProcessingLassie()
lassie.request_opts = {
    'headers':{
        # tell Lassie to tell others it is facebook
        'User-Agent': 'facebookexternalhit/1.1'
    }
}
