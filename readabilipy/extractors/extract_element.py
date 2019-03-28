from collections import defaultdict
import lxml.html
from ..text_manipulation import normalise_whitespace


def extract_element(html, xpaths):
    """Return the relevant element (title, date or byline) from article HTML
        xpaths should be a list of tuples, each with the xpath and a reliability score
    """

    # Parse the html and extract the contents using all xpaths
    lxml_html = lxml.html.fromstring(html)
    extracted_strings = defaultdict(int)

    # Get all elements specified and concatenate scores
    for extraction_xpath, score in xpaths:
        for found_element in lxml_html.xpath(extraction_xpath):
            element = normalise_whitespace(found_element)
            if element:
                extracted_strings[element] += score

    # Return highest scoring element
    if not extracted_strings:
        return None
    return max(extracted_strings, key=extracted_strings.get)
