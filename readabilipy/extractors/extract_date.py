from .extract_element import extract_element
import re


def extract_date(html):
    """Return the article date from the article HTML"""

    # List of xpaths for HTML tags that could contain a date
    # Tuple scores reflect confidence in these xpaths and the preference used for extraction
    # Some of the xpaths also have a specific format we expect the date html element to be
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

    if not ignoretz:
        return date_string
    expression = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}"
    if re.search(expression, date_string):
        return re.search(expression, date_string).group(0)
    return None
