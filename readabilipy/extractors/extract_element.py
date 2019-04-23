from collections import defaultdict
import lxml.html
from ..text_manipulation import normalise_whitespace


def get_element_candidates(html, xpaths, score_lower_limit=0):

    # Parse the html and extract the contents using all xpaths
    lxml_html = lxml.html.fromstring(html)
    extracted_strings = defaultdict(int)

    # Get all elements specified and concatenate scores
    for extraction_xpath, score in xpaths:
        if score >= score_lower_limit:
            found_elements = lxml_html.xpath(extraction_xpath)
            if found_elements:
                # If just one found
                if isinstance(found_elements, lxml.etree._ElementUnicodeResult):
                    element = normalise_whitespace(found_elements)
                    if element:
                        extracted_strings[element] += score
                # If a list of elements found:
                else:
                    for found_element in found_elements:
                        if isinstance(found_element, lxml.etree._ElementUnicodeResult):
                            element = normalise_whitespace(found_element)
                            if element:
                                extracted_strings[element] += score
    return extracted_strings


def extract_element(html, xpaths, process_dict_fn=None):
    """Return the relevant element (title, date or byline) from article HTML
        xpaths should be a list of tuples, each with the xpath and a reliability score
    """

    extracted_strings = get_element_candidates(html, xpaths, score_lower_limit=0)

    # Edit the dictionary
    if process_dict_fn:
        extracted_strings = process_dict_fn(extracted_strings)

    # Only search with xpaths that have a score of -1 if nothing else can be found
    if not extracted_strings:
        extracted_strings = get_element_candidates(html, xpaths, score_lower_limit=-1)
    print(extracted_strings)
    # Return highest scoring element
    if not extracted_strings:
        return None
    return max(extracted_strings, key=extracted_strings.get)
