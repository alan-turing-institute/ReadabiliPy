from bs4 import BeautifulSoup
from ..text_manipulation import normalise_whitespace
from ..plain_html import unwrap_elements
import lxml.html


def extract_element(html, xpaths):
    """Return the relevant element (title, date or byline) from article HTML
        xpaths should be a list of tuples, each with the xpath and a reliability score
    """

    # Discard certain html elements while keeping contents
    soup = BeautifulSoup(html)
    unwrap_elements(soup)
    html = soup.prettify()

    # Parse the html and extract the contents using all xpaths
    lxml_html = lxml.html.fromstring(html)
    elements = []
    element_tuples = []
    for extraction_xpath, score in xpaths:
        for found_element in lxml_html.xpath(extraction_xpath):
            element = normalise_whitespace(found_element)
            element_tuples.append((element, score))
            elements.append(element)

    if len(elements) == 0:
        return None  # Return None when no xpath elements in the HTML
    else:
        # Returns the most common element by default
        # Returns the most reliable (highest score) element when elements equally common
        if len(elements) == len(set(elements)):  # if all elements unique
            return max(element_tuples, key=lambda item: item[1])[0]
        else:
            return max(set(elements), key=elements.count)
