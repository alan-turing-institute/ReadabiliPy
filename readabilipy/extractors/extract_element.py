from collections import defaultdict
import lxml.html
from ..text_manipulation import normalise_whitespace


def get_element_candidates(html, xpaths, score_lower_limit=0):
    """Return the relevant elements (e.g. titles, dates or bylines) from article HTML, specificed by xpaths.
        xpaths should be a list of tuples, each with the xpath and a reliability score
        An xpath will be ignored if its score is below the limit.
        The returned dictionary should have the processed elements as keys and dicts with scores and the xpaths used as values
    """
    # Parse the html and extract the contents using all xpaths
    lxml_html = lxml.html.fromstring(html)
    extracted_strings = defaultdict(int)

    # Get all elements specified and concatenate scores
    for extraction_xpath, score in xpaths:
        if score >= score_lower_limit:
            found_elements = lxml_html.xpath(extraction_xpath)
            if found_elements:
                # If just one found, put it in a list
                if isinstance(found_elements, lxml.etree._ElementUnicodeResult):
                    found_elements = [found_elements]
                # Otherwise we expect to get a list
                for found_element in found_elements:
                    if isinstance(found_element, lxml.etree._ElementUnicodeResult):
                        element = normalise_whitespace(found_element)
                        if element:
                            if element in extracted_strings:
                                extracted_strings[element]['score'] += score
                                if extraction_xpath not in extracted_strings[element]['xpaths']:
                                    extracted_strings[element]['xpaths'].append(extraction_xpath)
                            else:
                                extracted_strings[element] = {}
                                extracted_strings[element]['score'] = score
                                extracted_strings[element]['xpaths'] = [extraction_xpath]
    return extracted_strings


def extract_element(html, xpaths, process_dict_fn=None):
    """Return the relevant elements (titles, dates or bylines) from article HTML, specificed by xpaths.
        xpaths should be a list of tuples, each with the xpath and a reliability scores.
        Processing of the dictionary can be handled with the arg function.
        xpaths with a score of -1 will only be considered if no elements are found in the html by other xpaths
        The returned dictionary should have the processed elements as keys and dicts with scores and the xpaths used as values
    """

    extracted_strings = get_element_candidates(html, xpaths, score_lower_limit=0)

    # Edit the dictionary
    if process_dict_fn:
        extracted_strings = process_dict_fn(extracted_strings)

    # Only search with xpaths that have a score of -1 if nothing else can be found
    if not extracted_strings:
        extracted_strings = get_element_candidates(html, xpaths, score_lower_limit=-1)
    return extracted_strings
