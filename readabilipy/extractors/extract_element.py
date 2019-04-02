from collections import defaultdict
import lxml.html
import lxml.etree
from ..text_manipulation import normalise_whitespace


def extract_element(html, xpaths, return_all_unique=False):
    """Return the relevant element (title, date or byline) from article HTML
        xpaths should be a list of tuples, each with the xpath and a reliability score
    """

    # Parse the html and extract the contents using all xpaths
    lxml_html = lxml.html.fromstring(html)
    extracted_strings = defaultdict(int)

    # Get all elements specified and concatenate scores
    for extraction_xpath, score in xpaths:
        for found_element in lxml_html.xpath(extraction_xpath):
            # Only proceed for xpaths that get text, not a html element
            if type(found_element) == lxml.etree._ElementUnicodeResult:
                element = normalise_whitespace(found_element)
                if element:
                    extracted_strings[element] += score
    # Return highest scoring element
    if not extracted_strings:
        return None
    if return_all_unique:  # In this case return a list of all unique elements
        return list(extracted_strings.keys())
    return max(extracted_strings, key=extracted_strings.get)  # In this case just highest scoring
