from .extract_element import extract_element
from datetime import datetime


def extract_date(html):
    """Return the article date from the article HTML"""

    # List of xpaths for HTML tags that could contain a date
    # Tuple scores reflect confidence in these xpaths and the preference used for extraction
    xpaths = [
        ('//meta[@property="article:published_time"]/@content', 13),
        ('//meta[@property="og:updated_time"]/@content', 10),
        ('//meta[@property="article:published"]/@content', 7),
        ('//meta[@itemprop="datePublished"]/@content', 3),
        ('//time/@datetime', 3),
        ('//meta[@itemprop="dateModified"]/@content', 2),
        ('//meta[@property="article:modified_time"]/@content', 2),
    ]

    # Get all the dates
    extracted_dates = extract_element(html, xpaths)
    if len(extracted_dates) == 0:
        return None
    # Set the date_string as that with the highest score assigned by extract_element
    date_string = max(extracted_dates, key=lambda x: extracted_dates[x]["score"])
    return ensure_iso_date_format(date_string)


def ensure_iso_date_format(date_string, ignoretz=True):
    """Check date_string is in one of our supported formats and return it"""
    supported_date_formats = [
        "%Y-%m-%dT%H:%M:%S",     # '2014-10-24T17:32:46'
        "%Y-%m-%dT%H:%M:%S%z",   # '2014-10-24T17:32:46+12:00'
        "%Y-%m-%dT%H:%M:%SZ",    # '2014-10-24T17:32:46Z'
        "%Y-%m-%dT%H:%M:%S.%fZ"  # '2014-10-24T17:32:46.000Z'
    ]

    for date_format in supported_date_formats:
        try:
            # For python < 3.7, strptime() is not able to parse timezones containing
            # colons (eg. 2014-10-24T17:32:46+12:00). By stripping the colon here,
            # we ensure that all versions of python can parse datetimes like these
            if date_format == "%Y-%m-%dT%H:%M:%S%z" and date_string[-3] == ':':
                isodate = datetime.strptime(date_string[:-3] + date_string[-2:], date_format)
            else:
                isodate = datetime.strptime(date_string, date_format)
            if ignoretz:
                isodate = isodate.replace(tzinfo=None)
            return isodate.isoformat()
        except ValueError:
            pass
    return None
