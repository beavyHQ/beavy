# flake8: noqa
import pytest
from urllib.parse import urlparse
from .fetching import extractor

class Number:
    def __init__(self, num=0):
        self.num = num
    def __eq__(self, other):
        if not isinstance(other, int):
            other = int(other)
        return self.num <= other

class StartsWith:
    def __init__(self, str):
        self.str = str
    def __eq__(self, other):
        return other.startswith(self.str)

class Present:
    def __init__(self, type_=None):
        self._type = type_
    def __eq__(self, other):
        if self._type:
            return isinstance(other, self._type)
        return other is not None

class Contains:
    def __init__(self, str):
        self.str = str
    def __eq__(self, other):
        return self.str in other

class HasItems:
    def __init__(self, items=[]):
        self.items = items

    def __eq__(self, other):
        for it in self.items:
            if not it in other:
                return False
        return True

class URL:

    def scheme(self, inp):
        self._scheme = inp
        return self

    def netloc(self, inp):
        self._netloc = inp
        return self

    def path(self, inp):
        self._path = inp
        return self

    def hostname(self, inp):
        self._hostname = inp
        return self

    def port(self, inp):
        self._port = inp
        return self

    def username(self, inp):
        self._username = inp
        return self

    def password(self, inp):
        self._password = inp
        return self

    def params(self, inp):
        self._params = inp
        return self

    def scheme_check(self, inp):
        self._scheme_check = inp
        return self

    def netloc_check(self, inp):
        self._netloc_check = inp
        return self

    def path_check(self, inp):
        self._path_check = inp
        return self

    def hostname_check(self, inp):
        self._hostname_check = inp
        return self

    def port_check(self, inp):
        self._port_check = inp
        return self

    def username_check(self, inp):
        self._username_check = inp
        return self

    def password_check(self, inp):
        self._password_check = inp
        return self

    def params_check(self, inp):
        self._params_check = inp
        return self

    def __eq__(self, other):
        url = urlparse(other)

        for p in ("scheme", "netloc", "path", "hostname", "port",
                  "username", "password", "params"):
            attr = "_{}".format(p)
            if hasattr(self, attr):
                if not getattr(url, p) == getattr(self, attr):
                    assert False, "{} faulty: {} isn't {}".format(url, p, getattr(self, attr))

            check_attr = "{}_check".format(attr)
            if hasattr(self, check_attr):
                if not getattr(self, check_attr)(getattr(url, p), url):
                    assert False, "{} faulty: {} failed check".format(url, p)

        return True


def ImageUrl(endswith, scheme=None, hostname=None):
    url = URL().path_check(lambda p, u: p.endswith(endswith))
    if scheme:
        url.scheme(scheme)
    if hostname:
        url.hostname(hostname)
    return url


def AndroidAppURL(appid):
    return URL().scheme("android-app").hostname(appid)


def IOSAppURL(appid):
    return URL().scheme("ios-app").hostname(appid)


@pytest.mark.slow
@pytest.mark.external
def test_blogger_example():
    assert extractor.fetch("http://buzz.blogger.com/2015/09/https-support-coming-to-blogspot.html") == {
        "alternates": {
            "application/atom+xml": URL().scheme("https").path_check(lambda p,x: p.startswith("/feeds")),
            "application/rss+xml": URL().scheme("https").path_check(lambda p,x: p.startswith("/feeds"))
        },
        "description": StartsWith("This morning we posted an update about Blogspot to Google"),
        "generator": "blogger",
        "site_name": "Blogger Buzz",
        "images": [
            {
                "src": ImageUrl("unnamed.png", "http"),
                "type": "og:image"
            },
            {
                "src": ImageUrl("favicon.ico", "https"),
                "type": "favicon"
            }
        ],
        "locale": "en_US",
        "title": "HTTPS support coming to Blogspot",
        "type": "article:blog",
        "url": "https://blogger.googleblog.com/2015/09/https-support-coming-to-blogspot.html",
        "videos": []
    }

@pytest.mark.slow
@pytest.mark.external
def test_amazon_example():
    assert extractor.fetch("http://www.amazon.de/Fall-Jane-Eyre-Roman-Unterhaltung/dp/3423212934/ref=sr_1_1?ie=UTF8") == {
        "ISBN": "3423212934",
        "alternates": {},
        "authors": [
            "Jasper Fforde",
            "Lorenz Stern"
        ],
        "categories": [
            "Belletristik / Science Fiction / Fantasy",
            "England",
            "Englische Belletristik",
            "Roman",
            "Erz\u00e4hlung",
            "Fantasy",
            "Belletristik / Fantastische Literatur",
            "Belletristik in \u00dcbersetzung",
            "Comic (Humor) Fantasy",
            "Kriminalromane & Mystery: weibliche Ermittler"
        ],
        "description": "Der Fall Jane Eyre: Roman (dtv Unterhaltung)",
        "images": [
            {
                "src": ImageUrl(".jpg", "http").hostname_check(lambda p,u: p.endswith("amazon.com")),
                "type": "og:image"
            }
        ],
        "keywords": [
            "Jasper Fforde",
            "Lorenz Stern",
            "Der Fall Jane Eyre: Roman (dtv Unterhaltung)",
            "Deutscher Taschenbuch Verlag",
            "3423212934",
            "Belletristik / Science Fiction / Fantasy",
            "England",
            "Englische Belletristik",
            "Roman",
            "Erz\u00e4hlung",
            "Fantasy",
            "Belletristik / Fantastische Literatur",
            "Belletristik in \u00dcbersetzung",
            "Comic (Humor) Fantasy",
            "Kriminalromane & Mystery: weibliche Ermittler"
        ],
        "publisher": "Deutscher Taschenbuch Verlag",
        "site_name": "Amazon.de",
        "title": "Der Fall Jane Eyre: Roman (dtv Unterhaltung)",
        "type": "book",
        "url": "http://www.amazon.de/dp/3423212934/ref=tsm_1_fb_lk",
        "videos": []
    }



@pytest.mark.slow
@pytest.mark.external
def test_wikipedia_example():
    assert extractor.fetch("https://en.wikipedia.org/wiki/Polygon") == {
        "alternates": {
            "android-app": AndroidAppURL("org.wikipedia")
                                .path_check(lambda p,x: p.endswith("Polygon")),
            "application/x-wiki": "/w/index.php?title=Polygon&action=edit"
        },
        "description": StartsWith("In elementary geometry, a polygon /\u02c8p\u0252l\u026a\u0261\u0252n/ is a plane figure that is bounded by a finite chain of straight line segments closing in a loop to form a closed chain or circuit. These segments are called its edges or sides, and the points where two edges meet are the polygon's vertices (singular: vertex) or corners. The interior of the polygon is sometimes called its body. An n-gon is a polygon with n sides."),
        "generator": StartsWith("MediaWiki"),
        "images": [
            {
                "src": ImageUrl("400px-Assorted_polygons.svg.png", None ,"upload.wikimedia.org"),
                "type": "contentImage"
            },
            {
                "src": ImageUrl(".ico", "https" ,"en.wikipedia.org"),
                "type": "favicon"
            }
        ],
        "locale": "en_US",
        "site_name": "From Wikipedia, the free encyclopedia",
        "title": "Polygon",
        "type": "article:wiki",
        "url": "https://en.wikipedia.org/wiki/Polygon",
        "videos": []
    }



@pytest.mark.slow
@pytest.mark.external
def test_meetup_com_event_example():
    assert extractor.fetch("http://www.meetup.com/opentechschool-berlin/events/226129991/") == {
        "alternates": HasItems(["de-DE", "en", "x-default"]),
        "country_name": "de",
        "description": "ABOUT:The meet-up is all about Ruby and Rails (but also about all the other things you can do with Ruby).We are a friendly group that meets every monday at seven o'clock to learn together and work o",
        "images": [
            {
                "src": URL().scheme("http")
                            .path_check(lambda p,x: "highres" in p and p.endswith("jpeg")),
                "type": "og:image"
            }
        ],
        "keywords": [
            "Germany",
            "Berlin",
            "softwaredev",
            "Learners",
            "group",
            "club",
            "event",
            "community",
            "local",
            "networking",
            "meet",
            "sharing",
            "Meetup"
        ],
        "latitude": "52.52",
        "locale": "en_US",
        "locality": "Berlin",
        "longitude": "13.38",
        "site_name": "Meetup",
        "title": "OpenTechSchool Berlin",
        "type": "activity",
        "url": "http://www.meetup.com/opentechschool-berlin/events/226129991/",
        "videos": []
    }


@pytest.mark.slow
@pytest.mark.external
def test_soundcloud_song_example():
    assert extractor.fetch("https://soundcloud.com/bassmelodie/bassmelodie-wintermelancholie") == {
        "alternates": {
            "android-app": AndroidAppURL("com.soundcloud.android"),
            "ios-app": URL().scheme("ios-app"),
            "only screen and (max-width: 640px)": URL()
                                .scheme("https")
                                .hostname("m.soundcloud.com"),
            "text/json+oembed": URL().scheme("https")
                                     .hostname("soundcloud.com")
                                     .path("/oembed"),
            "text/xml+oembed": URL().scheme("https")
                                    .hostname("soundcloud.com")
                                    .path("/oembed")
        },
        "author_name": "Bassmelodie",
        "author_url": URL().scheme("https")
                                .hostname("soundcloud.com")
                                .path("/bassmelodie"),
        "description": "Winter has its ups and downs... Lots of people are alone and don't have anyone whom they are able to share their feelings and emotions with. Sometimes it's worth to think not only about oneself. Ther",
        "images": [
            {
                "height": 500,
                "src": ImageUrl(".jpg", "https").hostname_check(lambda h, x: h.endswith("sndcdn.com")),
                "type": "og:image",
                "width": 500
            },
            {
                "src": ImageUrl(".ico", "https").hostname_check(lambda h, x: h.endswith("sndcdn.com")),
                "type": "favicon"
            }
        ],
        "keywords": [
            "record",
            "sounds",
            "share",
            "sound",
            "audio",
            "tracks",
            "music",
            "soundcloud"
        ],
        "locale": "en_US",
        "oembed": {
            "author_name": "Bassmelodie",
            "author_url": "https://soundcloud.com/bassmelodie",
            "description": "Winter has its ups and downs... \nLots of people are alone and don't have anyone whom they are able to share their feelings and emotions with. Sometimes it's worth to think not only about oneself. There are plenty of people out there who don't have anyone and who are alone. But there are also people who allegedly have everything they need. Nevertheless, they get a feeling of deep melancholy. \nYou can never be sure that such emotions will once hit you.\nThis set is dedicated to all those people...",
            "height": 400,
            "html": "<iframe width=\"100%\" height=\"400\" scrolling=\"no\" frameborder=\"no\" src=\"https://w.soundcloud.com/player/?visual=true&url=https%3A%2F%2Fapi.soundcloud.com%2Ftracks%2F181196205&show_artwork=true\"></iframe>",
            "provider_name": "SoundCloud",
            "provider_url": "http://soundcloud.com",
            "thumbnail_url": "http://i1.sndcdn.com/artworks-000100023660-j8gjf5-t500x500.jpg",
            "title": "Bassmelodie | Wintermelancholie by Bassmelodie",
            "type": "rich",
            "version": 1.0,
            "width": "100%"
        },
        "site_name": "SoundCloud",
        "soundcloud": {
            "comments_count": Number(200),
            "download_count": Number(0),
            "like_count": Number(4052),
            "play_count": Number(73265),
            "user": "https://soundcloud.com/bassmelodie"
        },
        "title": "Bassmelodie | Wintermelancholie",
        "type": "music.song",
        "url": URL().scheme("https")
                    .hostname("soundcloud.com")
                    .path("/bassmelodie/bassmelodie-wintermelancholie"),
        "videos": []
    }


@pytest.mark.slow
@pytest.mark.external
def test_slidesCom_example():
    assert extractor.fetch("http://slides.com/benjaminkampmann/component-oriented-ux/") == {
        "alternates": {},
        "description": "Understanding UI as reusable components and building it in a modular way are the new black in web development. But how exactly do you apply these latest technologies while still allowing overall themes and customization as we are used to? In this case study, we will look under the hood of beavy to understand how it uses CSS Modules and React to marry having highly complex, reusable UI-components and ensuring they can be completely customized at the same time. And what that means for the overall design process. --- This talk has been presented at UpFront #62, Nov 10th 2015, Berlin: http://www.meetup.com/up-front-ug/events/226053994/",
        "images": [
            {
                "src": ImageUrl("decks.jpg", "https", "s3.amazonaws.com"),
                "type": "og:image"
            },
            {
                "src": ImageUrl("decks.jpg", "https", "s3.amazonaws.com"),
                "type": "twitter:image"
            }
        ],
        "site_name": "Slides",
        "title": "Component-Oriented UX For The Win\u2026 But How? by Benjamin Kampmann",
        "type": "article",
        "url": "http://slides.com/benjaminkampmann/component-oriented-ux",
        "videos": []
    }

@pytest.mark.slow
@pytest.mark.external
def test_nytimes_example():
    assert extractor.fetch("http://www.nytimes.com/2015/11/15/arts/music/le1f-speaks-out-like-his-fearless-models-on-riot-boi.html") == {
        "alternates": {
            "android-app": AndroidAppURL("com.nytimes.android")
                                .path_check(lambda p,x: p.endswith("/100000004021164")),
            "http": "http://mobile.nytimes.com/2015/11/15/arts/music/le1f-speaks-out-like-his-fearless-models-on-riot-boi.html"
        },
        "description": "The rapper talks about a range of influences he drew on \u2014 Amanda Blank, M.I.A., Dev Hynes and others \u2014 in addressing misogyny, homophobia and more in his first full-length album.",
        "genre": "News",
        "images": [
            {
                "src": ImageUrl("facebookJumbo.jpg", "http", "static01.nyt.com"),
                "type": "og:image"
            },
            {
                "src": ImageUrl("favicon.ico", "https", "static01.nyt.com"),
                "type": "favicon"
            }
        ],
        "keywords": HasItems([
            "Music",
            "Rap and Hip-Hop"
        ]),
        "locale": "en_US",
        "publisher": "The New York Times",
        "section": "Music",
        "section_url": "http://www.nytimes.com/pages/arts/index.html",
        "title": " Le1f Speaks Out, Like His Fearless Models, on \u2018Riot Boi\u2019",
        "type": "article",
        "url": "http://www.nytimes.com/2015/11/15/arts/music/le1f-speaks-out-like-his-fearless-models-on-riot-boi.html",
        "videos": []
    }


@pytest.mark.slow
@pytest.mark.external
def test_zeitDe_example():
    assert extractor.fetch("http://www.zeit.de/politik/ausland/2015-11/polen-unabhaengigkeit-marsch-nationalisten") == {
        "alternates": {
            "application/rss+xml": URL().scheme("http")
                                        .hostname("newsfeed.zeit.de")
                                        .path("/index")
        },
        "description": "Die Unabh\u00e4ngigkeitsparaden in Polen waren einmal bunt und lustig. Das ist vorbei, auch weil der Extremismus in der Politik angekommen ist.",
        "images": [
            {
                "src": ImageUrl("favicon.ico", "http", "images.zeit.de"),
                "type": "favicon"
            }
        ],
        "keywords": [
            "Politik",
            "Unabhängigkeitstag",
            "Polen",
            "Nationalismus",
            "Rechtsextremismus",
            "Jaros\u0142aw Kaczy\u0144ski"
        ],
        "locale": "de_DE",
        "site_name": "ZEIT ONLINE",
        "title": Contains("Unabh\u00e4ngigkeitstag: Radikal ist in Polen zum Mainstream geworden"),
        "type": "article",
        "url": "http://www.zeit.de/politik/ausland/2015-11/polen-unabhaengigkeit-marsch-nationalisten",
        "videos": []
    }


@pytest.mark.slow
@pytest.mark.external
def test_flickr_image_example():
    assert extractor.fetch("https://www.flickr.com/photos/wbaiv/4332173964/in/photolist-7APwoy") == {
        "alternates": {
            "application/json+oembed": URL().scheme("https")
                                            .hostname("www.flickr.com")
                                            .path_check(lambda p,x: p.endswith("oembed")),
            "text/xml+oembed": URL().scheme("https")
                                    .hostname("www.flickr.com")
                                    .path_check(lambda p,x: p.endswith("oembed"))
        },
        "author_name": "wbaiv",
        "author_url": "https://www.flickr.com/photos/wbaiv/",
        "description": "This is the nose gear for the City of Everett, with big beavy blocks attached to the airplane to keep it in one place no matter how much the wind blows!  102-0233_IMG",
        "images": [
            {
                "height": 500,
                "src":  ImageUrl(".jpg", "https", "c1.staticflickr.com"),
                "type": "og:image",
                "width": 375
            }
        ],
        "locale": "en_US",
        "oembed": {
            "author_name": "wbaiv",
            "author_url": "https://www.flickr.com/photos/wbaiv/",
            "cache_age": 3600,
            "flickr_type": "photo",
            "height": "500",
            "html": "<a data-flickr-embed=\"true\" href=\"https://www.flickr.com/photos/wbaiv/4332173964/\" title=\"747-100 prototype nose gear by wbaiv, on Flickr\"><img src=\"https://farm5.staticflickr.com/4047/4332173964_e60fa3d95a.jpg\" width=\"375\" height=\"500\" alt=\"747-100 prototype nose gear\"></a><script async src=\"https://embedr.flickr.com/assets/client-code.js\" charset=\"utf-8\"></script>",
            "license": "Attribution-ShareAlike License",
            "license_id": "5",
            "license_url": "https://creativecommons.org/licenses/by-sa/2.0/",
            "provider_name": "Flickr",
            "provider_url": "https://www.flickr.com/",
            "thumbnail_height": 150,
            "thumbnail_url": "https://farm5.staticflickr.com/4047/4332173964_e60fa3d95a_q.jpg",
            "thumbnail_width": 150,
            "title": "747-100 prototype nose gear",
            "type": "photo",
            "url": "https://farm5.staticflickr.com/4047/4332173964_e60fa3d95a.jpg",
            "version": "1.0",
            "web_page": "https://www.flickr.com/photos/wbaiv/4332173964/",
            "web_page_short_url": "https://flic.kr/p/7APwoy",
            "width": "375"
        },
        "site_name": "Flickr - Photo Sharing!",
        "title": "747-100 prototype nose gear",
        "type": "flickr_photos:photo",
        "url": "https://www.flickr.com/photos/wbaiv/4332173964/",
        "videos": []
    }


@pytest.mark.slow
@pytest.mark.external
def test_tedCom_example():
    assert extractor.fetch("http://www.ted.com/talks/andreas_ekstrom_the_moral_bias_behind_your_search_results") == {
        "alternates": HasItems(["application/json+oembed","application/xml+oembed", "x-default", "en"]),
        "author_name": "Andreas Ekstr\u00f6m",
        "author_url": "http://www.ted.com/speakers/andreas_ekstrom",
        "description": "Search engines have become our most trusted sources of information and arbiters of truth. But can we ever get an unbiased search result? Swedish author and journalist Andreas Ekstr\u00f6m argues that such a thing is a philosophical impossibility. In this thoughtful talk, he calls on us to strengthen the bonds between technology and the humanities, and he reminds us that behind every algorithm is a set of personal beliefs that no code can ever completely eradicate.",
        "duration": "558",
        "images": [
            {
                "height": 550,
                "secure_src": ImageUrl(".jpg").hostname_check(lambda h,u: h.startswith("tedcdn")),
                "src": ImageUrl(".jpg").hostname_check(lambda h,u: h.startswith("tedcdn")),
                "type": "og:image",
                "width": 1050
            },
            {
                "src":  ImageUrl("favicon.svg").hostname_check(lambda h,u: h.startswith("tedcdn")),
                "type": "favicon"
            },
            {
                "src": ImageUrl("favicon.ico").hostname_check(lambda h,u: h.startswith("tedcdn")),
                "type": "favicon"
            }
        ],
        "keywords": [
            "TED",
            "talks",
            "Google",
            "Internet",
            "TEDx",
            "algorithm",
            "communication",
            "computers",
            "decision-making",
            "society",
            "software",
            "technology",
            "web"
        ],
        "locale": "en_US",
        "oembed": {
            "author_name": "Andreas Ekstr\u00f6m",
            "author_url": "http://www.ted.com/speakers/andreas_ekstrom",
            "description": "Search engines have become our most trusted sources of information and arbiters of truth. But can we ever get an unbiased search result? Swedish author and journalist Andreas Ekstr\u00f6m argues that such a thing is a philosophical impossibility. In this thoughtful talk, he calls on us to strengthen the bonds between technology and the humanities, and he reminds us that behind every algorithm is a set of personal beliefs that no code can ever completely eradicate.",
            "height": 315,
            "html": "<iframe src=\"https://embed-ssl.ted.com/talks/andreas_ekstrom_the_moral_bias_behind_your_search_results.html\" width=\"560\" height=\"315\" frameborder=\"0\" scrolling=\"no\" webkitAllowFullScreen mozallowfullscreen allowFullScreen></iframe>",
            "provider_name": "TED",
            "provider_url": "http://ted.com",
            "thumbnail_height": 180,
            "thumbnail_url": ImageUrl(".jpg").hostname_check(lambda h,u: h.startswith("tedcdn")),
            "thumbnail_width": 240,
            "title": "Andreas Ekstr\u00f6m: The moral bias behind your search results",
            "type": "video",
            "url": "http://www.ted.com/talks/andreas_ekstrom_the_moral_bias_behind_your_search_results",
            "version": "1.0",
            "width": 560
        },
        "release_date": "1447173342",
        "title": "The moral bias behind your search results",
        "type": "video.other",
        "url": "http://www.ted.com/talks/andreas_ekstrom_the_moral_bias_behind_your_search_results",
        "videos": []
    }

@pytest.mark.slow
@pytest.mark.external
def test_youtube_example():
    assert extractor.fetch("https://www.youtube.com/watch?v=SQ5wYZqHQGo?t=505") == {
        "alternates": {
            "android-app": AndroidAppURL("com.google.android.youtube"),
            "application/json+oembed": URL().scheme("http")
                                            .hostname("www.youtube.com")
                                            .path("/oembed"),
            "handheld": URL().scheme("http")
                             .hostname("m.youtube.com"),
            "ios-app": IOSAppURL("544007664"),
            "only screen and (max-width: 640px)": URL().scheme("http")
                                                       .hostname("m.youtube.com"),
            "text/xml+oembed": URL().scheme("http")
                                    .hostname("www.youtube.com")
                                    .path("/oembed")
        },
        "author_name": "O'Reilly",
        "author_url": "https://www.youtube.com/user/OreillyMedia",
        "description": "From the 2015 Velocity Conference in New York: I\u2019m going to talk about cognitive bias in operations land. I will go through two examples. The first example i...",
        "full_description": "From the 2015 Velocity Conference in New York: I\u2019m going to talk about cognitive bias in operations land. I will go through two examples.The first example is how cognitive biases can help us miss the next great thing. In this case, I will show how we could have almost missed the Docker revolution. I\u2019ll use this example to draw parallels and build up a transition to my second point.The second example is the meat of the talk. In this example I\u2019ll reflect on how blindly rejecting ideas from others unlike yourself is the biggest diversity/integration issue in tech and society.The talk will end with bold assertions about why we are in the tech industry. I will fall short of proposing a solution, but will leave with tech\u2019s problems are society\u2019s problems, and we have to think bigger in our search for solutions.About Bryan Liles (DigitalOcean):Bryan Liles works on strategic initiatives for DigitalOcean. In layman\u2019s terms, this means he writes OSS for DigitalOcean and others. He helps communities move their software to the public cloud, and gets to speak at conferences on topics ranging from Machine Learning to how build the next generation of developers. When not thinking about code, Bryan races cars in straight lines and around turns and builds robots and devicesWatch more from Velocity NYC 2015: https://goo.gl/PZAqiYVisit the Velocity website: http://velocityconf.com/Don't miss an upload! Subscribe! http://goo.gl/szEauhStay Connected to O'Reilly Media by Email - http://goo.gl/YZSWbOFollow O'Reilly Media:http://plus.google.com/+oreillymediahttps://www.facebook.com/OReillyhttps://twitter.com/OReillyMedia",
        "images": [
            {
                "src": ImageUrl("hqdefault.jpg", "https").hostname_check(lambda h,u: h.endswith(".ytimg.com")),
                "type": "og:image"
            },
            {
                "src": ImageUrl("hqdefault.jpg", "https").hostname_check(lambda h,u: h.endswith(".ytimg.com")),
                "type": "twitter:image"
            },
            {
                "src": ImageUrl(".ico", "https").hostname_check(lambda h,u: h.endswith(".ytimg.com")),
                "type": "favicon"
            },
            {
                "src": ImageUrl(".png", "https").hostname_check(lambda h,u: h.endswith(".ytimg.com")),
                "type": "favicon"
            },
            {
                "src": ImageUrl(".png", "https").hostname_check(lambda h,u: h.endswith(".ytimg.com")),
                "type": "favicon"
            },
            {
                "src": ImageUrl(".png", "https").hostname_check(lambda h,u: h.endswith(".ytimg.com")),
                "type": "favicon"
            },
            {
                "src": ImageUrl(".png", "https").hostname_check(lambda h,u: h.endswith(".ytimg.com")),
                "type": "favicon"
            }
        ],
        "keywords": [
            "O'Reilly Media (Publisher)",
            "digitalocean",
            "velocity new york",
            "velocity 2015",
            "velocity conference",
            "Bryan Liles",
            "Operating System (Software Genre)",
            "cognitive bias"
        ],
        "locale": Present(str), # Locale depends on origin of request ...
        "oembed": {
            "author_name": "O'Reilly",
            "author_url": "https://www.youtube.com/user/OreillyMedia",
            "height": 270,
            "html": "<iframe width=\"480\" height=\"270\" src=\"https://www.youtube.com/embed/SQ5wYZqHQGo?feature=oembed\" frameborder=\"0\" allowfullscreen></iframe>",
            "provider_name": "YouTube",
            "provider_url": "https://www.youtube.com/",
            "thumbnail_height": 360,
            "thumbnail_url": "https://i.ytimg.com/vi/SQ5wYZqHQGo/hqdefault.jpg",
            "thumbnail_width": 480,
            "title": "The Darker Side of Tech - Bryan Liles keynote",
            "type": "video",
            "version": "1.0",
            "width": 480
        },
        "site_name": "YouTube",
        "title": "The Darker Side of Tech - Bryan Liles keynote",
        "type": "video",
        "url": "https://www.youtube.com/watch?v=SQ5wYZqHQGo",
        "videos": [
            {
                "height": 720,
                "secure_src": ImageUrl("SQ5wYZqHQGo", "https", "www.youtube.com"),
                "src": ImageUrl("SQ5wYZqHQGo", "http", "www.youtube.com"),
                "width": 1280
            },
            {
                "height": 720,
                "src": ImageUrl("SQ5wYZqHQGo", "https", "www.youtube.com"),
                "width": 1280
            }
        ]
    }
