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
        "%Y-%m-%dT%H:%M:%S",  # e.g. '2014-10-24T17:32:46'
        "%Y-%m-%dT%H:%M:%S%z",  # e.g. '2014-10-24T17:32:46+12:00'
        "%Y-%m-%dT%H:%M:%S.%fZ"  # e.g. '2019-02-15T15:54:50.000Z'
    ]

    for date_format in supported_date_formats:
        try:
            if date_format == "%Y-%m-%dT%H:%M:%S%z" and ":" == date_string[-3:-2]:  # Below required for Python versions < 3.7
                date_string = date_string[:-3] + date_string[-2:]  # Remove colon between hours and minutes of timezone
            if 'Z' in date_string and '000Z' not in date_string:  # Below required for Python versions < 3.7
                date_string = date_string.replace('Z', '')  # Remove Z so we can interpret e.g. '2019-02-18T17:52:10Z'
            isodate = datetime.strptime(date_string, date_format)
            if ignoretz:
                isodate = isodate.replace(tzinfo=None)
            return isodate.isoformat()
        except ValueError:
            pass
    return None
