from .extract_element import extract_element
from datetime import datetime


def extract_date(html):
    """Return the article date from the article HTML"""

    # List of xpaths for HTML tags that could contain a date
    # Tuple scores reflect confidence in these xpaths and the preference used for extraction
    xpaths = [
        ('//meta[@property="article:published_time"]/@content', 13),
        ('//meta[@property="article:modified_time"]/@content', 2),
        ('//meta[@property="article:published"]/@content', 7),
        ('//meta[@property="og:updated_time"]/@content', 10),
        ('//meta[@itemprop="dateModified"]/@content', 2),
        ('//meta[@itemprop="datePublished"]/@content', 3),
        ('//time/@datetime', 3),
    ]

    # Get all the dates
    extracted_dates = extract_element(html, xpaths)
    if len(extracted_dates) == 0:
        return None
    # Set the date_string as that with the highest score assigned by extract_element
    date_string = max(extracted_dates, key=lambda x: extracted_dates[x].get('score'))
    return ensure_iso_date_format(date_string)


def ensure_iso_date_format(date_string, ignoretz=True):
    """Check date_string is in one of our supported formats and return it"""
    supported_date_formats = [
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%fZ"
    ]
    for date_format in supported_date_formats:
        try:
            isodate = datetime.strptime(date_string, date_format)
            if ignoretz:
                isodate = isodate.replace(tzinfo=None)
            return isodate.isoformat()
        except ValueError:
            pass
    return None
