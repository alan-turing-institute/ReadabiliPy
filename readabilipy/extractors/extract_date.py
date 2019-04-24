from .extract_element import extract_element
from contextlib import suppress
from dateutil import parser


def extract_date(html):
    """Return the article date from the article HTML"""

    # List of xpaths for HTML tags that could contain a date
    # Tuple scores reflect confidence in these xpaths and the preference used for extraction
    xpaths = [
        ('//meta[@property="article:published_time"]/@content', 24),  # Unlike with title, makes sense to have extremely high confidence in popular date tags
        ('//meta[@property="article:published"]/@content', 20),
        ('//meta[@name="Last-Modified"]/@content', 1),
        ('//meta[@name="dcterms.created"]/@content', 1),
        ('//meta[@name="published_time_telegram"]/@content', 1),
        ('//meta[@property="og:article:published_time"]/@content', 1),
        ('//meta[@itemprop="datePublished"]/@content', 2),
        ('//time[contains(@class, "entry-date")]/@datetime', 3),
        ('//time/@datetime', 6),
        ('//time/text()', 1),
        ('//div[@class="keyvals"]/@data-content_published_date', 1),
        ('//div/time/@datetime', 1),
        ('//div[@class="subarticle"]/p/text()', -1),
        ('//div[@class="text"]/p/text()', -1),
        ('//div[@class="publish-date"]/text()', 1),
        ('//span[@class="timestamp "]/text()', 1),
        ('//span[@class="article-element__meta-item"]/text()[contains(., "posted")]', 1),
        ('//span[@class="updated"]/text()', 1),
        ('//span[@class="entry-date"]/text()', 1),
        ('//p[@itemprop="datePublished"]/text()', 1),
        ('//p[@class="entry-byline"]//time[@class="entry-date"]/@datetime', 1),
        ('substring(//*[comment()[contains(., "By")]]/comment(), "-")', 1), # conservativehq
        ('substring-after(//p[@class="text-muted"]/text()[contains(., "Posted")], ",")', 2), # redstatewatcher
    ]

    # Get the date
    date_string = extract_element(html, xpaths)
    print(date_string)
    dayfirst = False
    if date_string:
        if "By" in date_string:
            dayfirst = True
    if date_string:
        return standardise_datetime_format(date_string, dayfirst=dayfirst)
    return None


def standardise_datetime_format(date_string, **kwargs):
    """Get an isoformat date string from a date string in any format"""

    with suppress(ValueError):
        return parser.parse(date_string, ignoretz=True, fuzzy=True, **kwargs).isoformat()
    return None
