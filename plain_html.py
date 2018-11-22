from bs4 import BeautifulSoup
from bs4.element import Comment, NavigableString
import regex
import unicodedata


def string_element_types():
    return [NavigableString, Comment]


def elements_to_delete():
    html5_form_elements = ['button', 'datalist', 'fieldset', 'form', 'input', 'label', 'legend', 'meter', 'optgroup',
                            'option', 'output', 'progress', 'select', 'textarea']
    html5_image_elements = ['area', 'img', 'map', 'picture', 'source']
    html5_media_elements = ['audio', 'track', 'video']
    html5_embedded_elements = ['embed', 'math', 'object', 'param', 'svg']
    html5_interactive_elements = ['details', 'dialog', 'summary']
    html5_scripting_elements = ['canvas', 'noscript', 'script', 'template']
    html5_data_elements = ['data', 'link', 'time']
    html5_formatting_elements = ['style']
    html5_navigation_elements = ['nav']

    elements = html5_form_elements + html5_image_elements + html5_media_elements  \
        + html5_embedded_elements + html5_interactive_elements + html5_scripting_elements + html5_data_elements \
        + html5_formatting_elements + html5_navigation_elements

    return elements


def block_level_whitelist():
    elements = ['article', 'aside', 'blockquote', 'caption', 'colgroup', 'col', 'div', 'dl', 'dt', 'dd', 'figure',
                'figcaption', 'footer', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'header', 'li', 'main', 'ol', 'p', 'pre',
                'section', 'table', 'tbody', 'thead' 'tfoot', 'tr', 'td', 'th', 'ul']
    return elements

def normalise_unicode(text):
    # Normalise unicode such that things that are visually equivalent map to the same
    # unicode string where possible
    normal_form = "NFKC"
    text = unicodedata.normalize(normal_form, text)
    return text


def normalise_whitespace(text):
    # Replace runs of multiple whitespace characters with a single space as this is what happens when HTML text is
    # displayed
    text = regex.sub("\s+", " ", text)
    # Remove leading and trailing whitespace
    text = text.strip()
    return text


def normalise_text(text):
    # Normalise unicode first to try and standardise whitespace characters as much as possible before normalising them
    text = normalise_unicode(text)
    text = normalise_whitespace(text)
    return text


def consolidate_child_text(element):
    prev_child = None
    for child in element.children:
        # If both previous and current child are strings, append the current string to the previous string and
        # remove the current string
        if prev_child and type(prev_child) is NavigableString and type(child) is NavigableString:
            text = normalise_text("{prev} {cur}", prev=str(prev_child), cur=str(child))
            prev_child.replace_with(NavigableString(text))
            child.extract()
            # As we've removed the current child, we leave prev_child untouched
        else:
            # Do nothing and set current child as previous child for next iteration
            prev_child = child
    return


def process_element(element):
    # Remove elements that we don't want to keep at all
    if element.name in elements_to_delete():
        element.extract()
    # String elements don't have children and are always retained so just normalise the string and return
    elif type(element) in string_element_types():
        # Treat Beautiful Soup text elements as strings when normalising as normalisation returns a copy of the string
        text = str(element)
        normalised_text = normalise_text(text)
        # Replace the element with a new string element of the same type, but containing the normalised text
        element.replace_with(type(element)(normalised_text))
    # Otherwise, process potentially complex element
    else:
        # We want to process all the children of the element before we process the element itself.
        for child in element.children:
            # Process the child element. Note that processing an element will often replace it with a modified version,
            # so we can't re-use our references to the child for further processing
            process_element(child)
        # NOTE: We query for the elements children again because most children will be replaced when processed above,
        # so any existing references to the children from before they were processed are likely to be invalid
        # 1. Consolidate consecutive strings into single strings
        consolidate_child_text(element)
        # 2. Replace 'hr' and 'br' defined paragraph breaks with real 'p's (for us do this for even single 'br's
        #    After string consolidation, we can just wrap the previous and next elements if they are NavigableText and
        #    then drop the 'br' or 'hr' (NOT QUITE: if parent is 'p' can't just wrap text with p. Need to split 'p'
        #    into two
        make_virtual_paragraphs_concrete(element)
        # One or more consecutive 'hr's or two or more consecutive 'br's indicates a paragraph break. Find any in the
        # children of this element and ensure the blocks of text that come before and afterwards are in separate
        # whitelisted block level elements.



        # After processing each child we want to ensure that all conceptual paragraphs are
        # Once we have processed all children, process this element
        # 1. Remove elements that we don't want to keep at all
        if element.name in elements_to_delete():
            element.extract()
        # 2. Deal with elements that have special handling
        # 2a. Replace 'quote' elements with quotation marks. We can safely use getText() as we have already processed all
        # child elements
        elif element.name == 'q':
            element.replace_with("\"{}\"".format(normalise_textelement.getText(" ", strip=True)))
        # 2b. Replace 'sub' element with '_' prefix
        elif element.name == 'sub':
            element.replace_with("_{}".format(normalise_text(element.getText(" ", strip=True))))
        # 2b. Replace 'sup' element with '^' prefix
        elif element.name == 'sup':
            element.replace_with("^{}".format(normalise_text(element.getText(" ", strip=True))))
        # 3. Replace all other elements with their text contents
        else:
            element.replace_with(normalise_text(element.getText(" ", strip=True)))
        return
        'br'
        'hr'
    return
