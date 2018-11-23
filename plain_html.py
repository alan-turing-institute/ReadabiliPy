from bs4 import BeautifulSoup
from bs4.element import Comment, NavigableString
import regex
import unicodedata


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


def elements_to_replace_with_contents():
    """Elements that we will discard while keeping their contents."""
    elements = ['a', 'abbr', 'address', 'b', 'bdi', 'bdo', 'cite', 'code', 'del', 'dfn', 'em', 'i', 'ins', 'kbs',
                'mark', 'q', 'rb', 'ruby', 'rp', 'rt', 'rtc', 's', 'samp', 'small', 'span', 'strong', 'u', 'var', 'wbr']
    return elements


def block_level_whitelist():
    """Elements that we will always accept."""
    elements = ['article', 'aside', 'blockquote', 'caption', 'colgroup', 'col', 'div', 'dl', 'dt', 'dd', 'figure',
                'figcaption', 'footer', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'header', 'li', 'main', 'ol', 'p', 'pre',
                'section', 'table', 'tbody', 'thead' 'tfoot', 'tr', 'td', 'th', 'ul']
    return elements


def normalise_unicode(text):
    """Normalise unicode such that things that are visually equivalent map to the same unicode string where possible."""
    normal_form = "NFKC"
    text = unicodedata.normalize(normal_form, text)
    return text


def normalise_whitespace(text):
    """Replace runs of whitespace characters with a single space as this is what happens when HTML text is displayed."""
    text = regex.sub("\s+", " ", text)
    # Remove leading and trailing whitespace
    text = text.strip()
    return text


def normalise_text(text):
    """Normalise unicode and whitespace."""
    # Normalise unicode first to try and standardise whitespace characters as much as possible before normalising them
    text = normalise_unicode(text)
    text = normalise_whitespace(text)
    return text


def remove_blacklist(soup):
    """Remove all blacklisted elements."""
    for element_name in elements_to_delete():
        for element in soup.find_all(element_name):
            element.decompose()


def flatten_elements(soup):
    """Flatten all elements where we are only interested in their contents."""
    for element_name in elements_to_replace_with_contents():
        for element in soup.find_all(element_name):
            element.unwrap()


def reformat_linebreaks(soup):
    """Replace linebreaks with close-parent reopen-parent."""

    BREAK_INDICATOR = "|CLOSE_AND_REOPEN|"

    # Iterate through the tree, removing single <br> and replacingmultiple <br> with BREAK_INDICATOR
    for element in soup.find_all("br"):
        # This check is needed since we're modifying the list while iterating through it
        if element.name == "br":
            # Start with empty list and populate it with all consecutive <br> elements
            element_list, current = [], element
            while current.name == "br":
                element_list.append(current)
                current = current.next_sibling
            # If there's only one <br> then we strip it out
            if len(element_list) == 1:
                element_list[0].decompose()
            # If there are multiple <br>s then we replace them with BREAK_INDICATOR
            else:
                element_list[0].replace_with(BREAK_INDICATOR)
                for element in element_list[1:]:
                    element.decompose()

    # Iterate through the tree, replacing <hr> with BREAK_INDICATOR
    for element in soup.find_all("hr"):
        # This check is needed since we're modifying the list while iterating through it
        if element.name == "hr":
            element.replace_with(BREAK_INDICATOR)
    
    # print_all(soup)

    # Iterate through the tree again replacing BREAK_INDICATOR with close-parent reopen-parent
    for element in soup.descendants:
        element_as_string = str(element)

        # For each element where we find a BREAK_INDICATOR, replace this with a "close-parent reopen-parent" string
        if BREAK_INDICATOR in element_as_string:
            multielement_string = element_as_string.replace(BREAK_INDICATOR, "</{0}><{0}>".format(element.name))

            # Now we need to re-parse this string to correctly split it into elements
            parse_tree = BeautifulSoup(multielement_string, "html.parser")            

            # ... and replace the element with the parsed output
            element.replace_with(parse_tree)


def normalise_strings(soup):
    # Iterate over all strings in the tree (including bare strings outside tags)
    for element in soup.find_all(string=True):
        # Treat Beautiful Soup text elements as strings when normalising since normalisation returns a copy of the string
        text = str(element)
        normalised_text = normalise_text(text)
        # Replace the element with a new string element of the same type, but containing the normalised text
        element.replace_with(type(element)(normalised_text))


def consolidate_text(soup):
    # Iterate over all strings in the tree
    for element in soup.find_all(string=True):
        # If the previous element is the same type then extract the current string and append to previous
        if type(element.previous_sibling) is type(element):
            text = " ".join([str(element.previous_sibling), str(element)])
            element.previous_sibling.replace_with(text)
            element.extract()


def wrap_bare_text(soup):
    # Iterate over all strings in the tree
    for element in soup.find_all(string=True):
        # Identify any strings whose parent is not a whitelisted element
        if element.parent.name not in block_level_whitelist():
            # ... and wrap them in <p> tags
            p_element = soup.new_tag("p")
            p_element.string = element
            element.replace_with(p_element)

# def print_all(soup):
#     for element in soup.descendants:
#         print(type(element), element.name, element)


def parse_to_tree(html, content_digests=False, node_indexes=False):
    # Convert the HTML into a Soup parse tree
    soup = BeautifulSoup(html, "html.parser")

    # Remove blacklisted elements
    remove_blacklist(soup)

    # Flatten elements where we want to keep the text but drop the containing tag
    flatten_elements(soup)
    
    # Replace <br> and <hr> elements
    reformat_linebreaks(soup)

    # Consolidate text 
    consolidate_text(soup)

    # Normalise all strings
    normalise_strings(soup)

    # Wrap any remaining bare text in <p> tags
    wrap_bare_text(soup)

    # Finally wrap the whole tree in a div
    root = soup.new_tag("div")
    root.append(soup)
    return root




# if __name__ == "__main__":
#     html="""
#         <article>
#         <header>
#             <h2>Lorem ipsum dolor sit amet</h2>
#             <p>Consectetur adipiscing elit</p>
#         </header>
#         <p>Vestibulum leo nulla, imperdiet a pellentesque ultrices aliquam.</p>
#         <button type="button">Click Me!</button>
#         </article>
#         <datalist id=sexes>
#             <option value="Female">
#             <option value="Male">
#         </datalist>
#         <span>Some text here</span>
#         <p class="something">Some extra text, single-broken,<br/> that is split with double <br/><br/> line breaks in such a way that
#         it is wrapped<hr/>and has horizontal rules as well as <br/><br/><br/> triple
#         line breaks</p>

#         <a href="whatever">here are <cite>nested</cite> flat elements</a>
#         <p>Here is
#         a paragraph
#         with non-syntactical line-breaks
#         </p>

#         And finish with some bare
#         text that has linebreaks
#         in odd places

#         Another piece of text
#         <br>
#         <br>
#         A new paragaph
#         <br>
#         I should be merged with the previous paragraph
#     """
#     parsed_html = parse_html(html, node_indexes=True)
#     print(parsed_html.prettify())