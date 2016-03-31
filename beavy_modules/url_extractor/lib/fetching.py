from lassie.core import Lassie
import requests
import re

# lassie by default isn't extensive enough for us
# configure it so that it is.

from lassie.filters import FILTER_MAPS

FILTER_MAPS['meta']['open_graph']['pattern'] = re.compile(
    r"^(og:|author:|article:|music:|video:|book:)", re.I)

FILTER_MAPS['meta']['open_graph']['map'].update({
    # general
    "og:type": "type",
    "og:site_name": "site_name",

    # video
    # LIST, and we don't have list support atm
    # "og:video:tag": "tag",

    # at least used by meetup.com!
    "og:country-name": "country_name",
    "og:locality": "locality",
    "og:latitude": "latitude",
    "og:longitude": "longitude",
    "og:locale": "locale",

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


FILTER_MAPS['meta']['generic']['pattern'] = re.compile(
    r"^(description|keywords|title|generator)")
FILTER_MAPS['meta']['generic']['map']['generator'] = 'generator'


def _matches(data, **kwargs):
    for key, match in kwargs.items():
        try:
            given_value = data[key]
        except KeyError:
            return False
        else:
            if isinstance(match, re._pattern_type):
                if not match.match(given_value):
                    return False
            elif callable(match):
                if not match(given_value):
                    return False
            else:
                if match != given_value:
                    return False
    return True


class AmazonISBNFinder:

    def __call__(self, soup, data, url=None):
        if not _matches(data,
                        type='book',
                        site_name=lambda x: x.lower().startswith("amazon")
                        ): return
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


class AlternateFinder:
    def __call__(self, soup, data, url=None):
        def mapper(link):
            return (link.get("type") or
                    link.get("media") or
                    link.get("hreflang") or
                    link.get("href").split("://", 1)[0],
                    link.get("href"))
        data["alternates"] = target = {}

        for name in ("alternate", "alternative"):
            target.update(dict([mapper(link)
                                for link in soup.find_all('link',
                                                          {'rel': name})]))


class OEmbedExtractor:

    REMAP = ["author_name", "author_url", "licence",
             "licence_url", "url", "title", "type"]

    def __call__(self, soup, data, url=None):
        try:
            link = data["alternates"]["application/json+oembed"]
        except KeyError:
            # inofficial link
            try:
                link = data["alternates"]["text/json+oembed"]
            except KeyError:
                return

        data["oembed"] = requests.Session().get(link).json()

        for key in self.REMAP:
            if key not in data['oembed']:
                continue
            if not data.get(key, False):
                data[key] = data["oembed"][key]


class SoundcloudInfoExtractor:

    MATCHER = re.compile(r"^soundcloud:")

    def __call__(self, soup, data, url=None):
        if not _matches(data, type="music.song", site_name="SoundCloud"):
            return

        data["soundcloud"] = dict([(m.get("property")[11:], m.get("content"))
                                   for m in soup.find_all('meta',
                                                          {'property':
                                                           self.MATCHER})])


class ArticleMetaExtractor:

    def __call__(self, soup, data, url=None):
        if not _matches(data, type="article"):
            return

        if not data.get("copyright", False):
            copy = soup.find("meta", {'name': "copyright"})
            if copy:
                data["copyright"] = copy.get("content")

        if not data.get("publisher", False):
            tag = soup.find("meta", {'name': "cre"})

            if tag:
                data["publisher"] = tag.get("content")
            elif "copyright" in data:
                data["publisher"] = data["copyright"]

        if not data.get("genre", False):
            genre = soup.find("meta", {'itemprop': "genre"})
            if genre:
                data["genre"] = genre.get("content")


class MediaWikiExtractor:
    def __call__(self, soup, data, url=None):
        if not _matches(data,
                        generator=lambda x: x.lower().startswith("mediawiki")
                        ) or data.get("type", False):
            return

        for iD, key in (('firstHeading', 'title'),
                        ('siteSub', 'site_name')):
            if data.get(key, False):
                continue

            obj = soup.find(id=iD)
            if obj:
                data[key] = obj.string

        content = soup.find(id="mw-content-text")
        if content:
            data["type"] = 'article:wiki'

            # find the first image:
            first_image = content.find("img")
            if first_image:
                data["images"].append({
                    "src": first_image.get("src"),
                    "type": "contentImage"
                })

            first_para = content.find("p")
            if first_para:
                data["description"] = first_para.text


class YoutubeExtractor:

    def __call__(self, soup, data, url=None):
        if not _matches(data, type="video", site_name="YouTube"):
            return

        baseContent = soup.find(id="eow-description")
        if baseContent:
            data['full_description'] = baseContent.text


class BloggerExtractor:

    def __call__(self, soup, data, url=None):
        if not _matches(data, generator="blogger") or\
           data.get("description", False):
            return

        blog_content = soup.find('div', class_="post-content")
        if blog_content:
            # bingo
            for img in blog_content.find_all("img", limit=3):
                data['images'].append({
                    "src": img.get("src"),
                    "type": "contentImage"
                })

            data['description'] = blog_content.text[:500]
            data["type"] = "article:blog"


class SimpleInfoFallbackExtractor:

    def __call__(self, soup, data, url=None):
        if data.get("description", False):
            return

        for query in [dict(id="content"),
                      dict(role="content"),
                      dict(role="main"),
                      dict(id="main"),
                      dict(class_="content"),
                      dict(class_="main"),
                      dict(id="page"),
                      dict(class_="page")]:
            box = soup.find(**query)
            if box:
                paragraphs = [x for x in map(lambda x: x.text,
                                             box.find_all(["div", "p"],
                                                          limit=5))
                              if x and len(x) > 50]
                if paragraphs:
                    data['description'] = paragraphs[0]
                    for img in box.find_all("img", limit=3):
                        data['images'].append({
                            "src": img.get("src"),
                            "type": "contentImage"
                        })
                    # first found: stop the loop!
                    break


class PostProcessingLassie(Lassie):

    POST_PROCESSORS = [
        # Generic Finders
        AlternateFinder(),
        OEmbedExtractor(),  # OEmbed only works after Alternate!


        # Mid specific:
        # Fetches for e.g. WikiPedia Content
        MediaWikiExtractor(),
        # Newspapers (like NYTimes):
        ArticleMetaExtractor(),
        # Blogger Style
        BloggerExtractor(),

        # Specific Platforms:
        AmazonISBNFinder(),
        SoundcloudInfoExtractor(),
        YoutubeExtractor(),

        # If we don't find anything, extract from content
        SimpleInfoFallbackExtractor()
    ]

    def _filter_meta_data(self, source, soup, data, url=None):
        super(PostProcessingLassie, self)._filter_meta_data(source,
                                                            soup,
                                                            data,
                                                            url=url)

        if source == "generic":
            # we are in the last generic parsing,
            # do the post_processing
            for processor in self.POST_PROCESSORS:
                processor(soup, data, url=url)

        return data

# this is what is exported
extractor = PostProcessingLassie()
# tell Lassie to tell others it is facebook
extractor.request_opts = {'headers': {'User-Agent': 'facebookexternalhit/1.1'}}
