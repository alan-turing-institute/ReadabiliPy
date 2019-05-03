from .extract_element import extract_element
from contextlib import suppress
from dateutil import parser
from pendulum import from_format


def extract_date(html):
    """Return the article date from the article HTML"""

    # List of xpaths for HTML tags that could contain a date
    # Tuple scores reflect confidence in these xpaths and the preference used for extraction
    # Some of the xpaths also have a specific format we expect the date html element to be
    xpaths = [
        ('//meta[@property="article:published_time"]/@content', 24),
        ('//meta[@property="article:published"]/@content', 20),
        ('//meta[@name="Last-Modified"]/@content', 1, 'YYYY-MM-DD hh:mm:ss'),
        ('//meta[@name="dcterms.created"]/@content', 1),
        ('//meta[@name="published_time_telegram"]/@content', 1),
        ('//meta[@property="og:article:published_time"]/@content', 1),
        ('//meta[@itemprop="datePublished"]/@content', 2),
        ('//time/@datetime', 6),
        ('//time/text()', 1),
        ('//div[@class="keyvals"]/@data-content_published_date', 1),
        ('//div[@class="subarticle"]/p/text()', -1, 'MMMM D, YYYY'),
        ('//div[@class="text"]/p/text()', -1, 'MMMM D, YYYY'),
        ('//div[@class="publish-date"]/text()', 1, '[Published] hh:mm A [EST] MMM DD, YYYY'),
        ('//span[@class="timestamp "]/text()', 1),
        ('//span[@class="article-element__meta-item"]/text()[contains(., "posted")]', 1, 'MMM DD YYYY'),
        ('//span[@class="updated"]/text()', 1, 'YYYY-MM-DD'),
        ('//span[@class="entry-date"]/text()', 1, 'MMM D, YYYY'),
        ('//p[@itemprop="datePublished"]/text()', 1, 'MMMM DD, YYYY'),
        ('//p[@class="entry-byline"]//time[@class="entry-date"]/@datetime', 1),
    ]

    # Get all the dates
    extracted_dates = extract_element(html, xpaths)
    if not extracted_dates:
        return None
    # Select date with highest score
    date_string = max(extracted_dates, key=lambda x: extracted_dates[x].get('score'))
    # Assign the format variable if the the highest scoring xpath used has one
    xpaths_used = extracted_dates[date_string]['xpaths']
    format = None
    high_score = 0
    for xpath in xpaths_used:
        for tuple in xpaths:
            if tuple[0] == xpath:
                if tuple[1] > high_score:
                    high_score = tuple[1]
                    if len(tuple) == 3:
                        format = tuple[2]

    return standardise_datetime_format(date_string, format=format)


def standardise_datetime_format(date_string, ignoretz=True, format=None, **kwargs):
    """Get an isoformat date string from a date string in any format"""

    if format:  # When format specified, use Pendulum
        with suppress(ValueError):
            return from_format(date_string, format).replace(tzinfo=None).isoformat()

    with suppress(ValueError):  # When no format specified, use dateutil to make use of fuzzy param
        return parser.parse(date_string, ignoretz=ignoretz, fuzzy=True, **kwargs).isoformat()
    return None
