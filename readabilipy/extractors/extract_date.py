from .extract_element import extract_element
from contextlib import suppress
from dateutil import parser
from pendulum import from_format


def extract_date(html):
    """Return the article date from the article HTML"""

    # List of xpaths for HTML tags that could contain a date
    # Tuple scores reflect confidence in these xpaths and the preference used for extraction
    xpaths = [
        ('//meta[@property="article:published_time"]/@content', 24),  # 'YYYY-MM-DD' or None
        ('//meta[@property="article:published"]/@content', 20),
        ('//meta[@name="Last-Modified"]/@content', 1),  # 'YYYY-MM-DD hh:mm:ss'
        ('//meta[@name="dcterms.created"]/@content', 1),
        ('//meta[@name="published_time_telegram"]/@content', 1),
        ('//meta[@property="og:article:published_time"]/@content', 1),
        ('//meta[@itemprop="datePublished"]/@content', 2),
        ('//time/@datetime', 6),
        ('//time/text()', 1),
        ('//div[@class="keyvals"]/@data-content_published_date', 1),
        ('//div/time/@datetime', 1),  # 'ddd MMM D YYYY HH:mm:ss'
        ('//div[@class="subarticle"]/p/text()', -1),  # 'MMMM D, YYYY'
        ('//div[@class="text"]/p/text()', -1),  # 'MMMM D, YYYY'
        ('//div[@class="publish-date"]/text()', 1),  # '[Published] hh:mm A [EST] MMM DD, YYYY'
        ('//span[@class="timestamp "]/text()', 1),
        ('//span[@class="article-element__meta-item"]/text()[contains(., "posted")]', 1),  # 'MMM DD YYYY'
        ('//span[@class="updated"]/text()', 1),  # 'YYYY-MM-DD'
        ('//span[@class="entry-date"]/text()', 1),  # 'MMM D, YYYY'
        ('//p[@itemprop="datePublished"]/text()', 1),  # 'MMMM DD, YYYY'
        ('//p[@class="entry-byline"]//time[@class="entry-date"]/@datetime', 1),
    ]

    # Get the date
    extracted_dates = extract_element(html, xpaths)
    if not extracted_dates:
        return None
    # date_string = max(extracted_dates, key=extracted_dates.get)
    date_string = max(extracted_dates, key=lambda x: extracted_dates[x].get('score'))
    if date_string:
        return standardise_datetime_format(date_string)
    return None


def standardise_datetime_format(date_string, ignoretz=True, format=None, **kwargs):
    """Get an isoformat date string from a date string in any format"""

    if format:  # When format specified, use Pendulum
        return from_format(date_string, format).replace(tzinfo=None).isoformat()

    with suppress(ValueError):  # When no format specified, use dateutil to make use of fuzzy param
        return parser.parse(date_string, ignoretz=ignoretz, fuzzy=True, **kwargs).isoformat()
    return None
