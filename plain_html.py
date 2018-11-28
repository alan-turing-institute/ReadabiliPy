from bs4 import BeautifulSoup, CData, Comment, Doctype
from .text_manipulation import normalise_text

BREAK_INDICATOR = "|CLOSE_AND_REOPEN|"

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
    # html5_header_elements = ['head']

    elements = html5_form_elements + html5_image_elements + html5_media_elements  \
        + html5_embedded_elements + html5_interactive_elements + html5_scripting_elements + html5_data_elements \
        + html5_formatting_elements + html5_navigation_elements

    return elements


def elements_to_replace_with_contents():
    """Elements that we will discard while keeping their contents."""
    elements = ['a', 'abbr', 'address', 'b', 'bdi', 'bdo', 'center', 'cite', 'code', 'del', 'dfn', 'em', 'i', 'html', 'ins', 'kbs',
                'mark', 'rb', 'ruby', 'rp', 'rt', 'rtc', 's', 'samp', 'small', 'span', 'strong', 'u', 'var', 'wbr']
    return elements


def special_elements():
    """Elements that we will discard while keeping their contents that need additional processing."""
    elements = ['q', 'sub', 'sup']
    return elements


def block_level_whitelist():
    """Elements that we will always accept."""
    elements = ['article', 'aside', 'blockquote', 'caption', 'colgroup', 'col', 'div', 'dl', 'dt', 'dd', 'figure',
                'figcaption', 'footer', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'header', 'li', 'main', 'ol', 'p', 'pre',
                'section', 'table', 'tbody', 'thead' 'tfoot', 'tr', 'td', 'th', 'ul']
    elements += ['title']
    return elements


# def remove_metadata(soup):
#     """Remove comments and doctype as well as meta, title and head elements."""
#     for comment in soup.findAll(string=lambda text:any([isinstance(text, x) for x in [CData, Comment, Doctype]])):
#         print("Removing comment:", comment)
#         comment.extract()
#     # for element in soup.find_all(["title", "meta", "head"]):
#     #     print("Removing meta-element:", element)
#     #     element.decompose()


def remove_blacklist(soup):
    """Remove all blacklisted elements."""
    for element_name in elements_to_delete():
        for element in soup.find_all(element_name):
            print("REMOVING:", element.name, str(element))
            element.decompose()


def flatten_elements(soup):
    """Flatten all elements where we are only interested in their contents."""
    for element_name in elements_to_replace_with_contents():
        for element in soup.find_all(element_name):
            element.unwrap()


def process_special_elements(soup):
    """Flatten special elements while processing their contents."""
    for element_name in special_elements():
        for element in soup.find_all(element_name):
            if element.name == "q":
                element.string = '"{0}"'.format(element.string)
            if element.name == "sub":
                element.string = "_{0}".format(element.string)
            if element.name == "sup":
                element.string = "^{0}".format(element.string)
            element.unwrap()


def remove_empty_strings(soup):
    """Remove any strings which contain only whitespace. Without this, consecutive linebreaks may not be identified correctly."""
    for element in soup.find_all(string=True):
        if not normalise_text(str(element)):
            element.extract()


def identify_linebreaks(soup):
    """Identify linebreaks."""
    # Iterate through the <br> elements in the tree
    for element in soup.find_all("br"):
        # If the next element is not another <br> then count how long the chain is up to this point
        if element.next_sibling.name != "br":
            br_element_chain = [element]
            while br_element_chain[-1].previous_sibling.name == "br":
                br_element_chain.append(br_element_chain[-1].previous_sibling)

            # If there's only one <br> then we strip it out
            if len(br_element_chain) == 1:
                br_element_chain[0].decompose()
            # If there are multiple <br>s then we replace them with BREAK_INDICATOR
            else:
                br_element_chain[0].replace_with(BREAK_INDICATOR)
                for element in br_element_chain[1:]:
                    element.decompose()

    # Iterate through the tree, replacing <hr> with BREAK_INDICATOR
    for element in soup.find_all("hr"):
        # This check is needed since we're modifying the list while iterating through it
        if element.name == "hr":
            element.replace_with(BREAK_INDICATOR)


def apply_linebreaks(soup):
    """Replace linebreak markers with close-parent reopen-parent."""
    # Iterate through the tree, splitting elements which contain BREAK_INDICATOR
    for element in soup.find_all(string=True):
        if BREAK_INDICATOR in element:
            # Split the text into two or more fragments (there maybe be multiple BREAK_INDICATORs in the string)
            text_fragments = [s.strip() for s in str(element).split(BREAK_INDICATOR)]

            # Make a list of connected parent elements (the first of which is the original element)
            parent_elements = [element.parent]
            for _ in range(len(text_fragments) - 1):
                new_element = soup.new_tag(element.parent.name)
                parent_elements[-1].insert_after(new_element)
                parent_elements.append(new_element)

            # Set the string for each element
            for parent_element, text_fragment in zip(parent_elements, text_fragments):
                parent_element.string = text_fragment


def normalise_strings(soup):
    """Remove extraneous whitespace and fix unicode issues in all strings."""
    # Iterate over all strings in the tree (including bare strings outside tags)
    for element in soup.find_all(string=True):
        # Treat Beautiful Soup text elements as strings when normalising since normalisation returns a copy of the string
        text = str(element)
        normalised_text = normalise_text(text)
        # Replace the element with a new string element of the same type, but containing the normalised text
        element.replace_with(type(element)(normalised_text))


def consolidate_text(soup):
    """Join any consecutive NavigableStrings together with spaces."""
    # Iterate over all strings in the tree
    for element in soup.find_all(string=True):
        # If the previous element is the same type then extract the current string and append to previous
        if type(element.previous_sibling) is type(element):
            text = " ".join([str(element.previous_sibling), str(element)])
            element.previous_sibling.replace_with(text)
            element.extract()


def wrap_bare_text(soup):
    """Wrap any remaining bare text in <p> tags."""
    # Iterate over all strings in the tree
    for element in soup.find_all(string=True):
        # Identify any strings whose parent is not a whitelisted element
        if element.parent.name not in block_level_whitelist():
            # ... and wrap them in <p> tags
            p_element = soup.new_tag("p")
            p_element.string = element
            element.replace_with(p_element)


def strip_attributes(soup):
    """Strip tag attributes."""
    for element in soup.find_all():
        element.attrs = {}

# def remove_empty_elements(soup):
#     """Remove any elements which contain only whitespace."""

#     for element in soup.find_all():
#         if not element.contents:
#             print("  ELEMENT:", element.name, str(element).strip(), element.contents)
#             element.decompose()

def recursively_flatten(soup):
    """Recursively replace any elements which contain 0 or 1 children."""
    def single_replace():
        nRemoved = 0
        for element in soup.find_all():
            print("ALL:", element.name, len(list(element.children)), "->", str(element).strip())
        for element in soup.find_all(lambda elem:len(list(elem.children)) == 0):
            print(":", element.name, len(list(element.children)), "->", str(element).strip())
            element.decompose()
            nRemoved += 1
        print("Removed", nRemoved)
        return nRemoved

    # single_replace()
    # while True:
    #     single_replace():
    #         break
    while single_replace():
        print("\n\n\n")
        pass



def PRINTALL(soup):
    for element in soup.find_all():
        print("  ELEMENT:", element.name, len(list(element.children)))

def parse_to_tree(html):
    # Convert the HTML into a Soup parse tree
    # soup = BeautifulSoup(html, "html.parser")
    soup = BeautifulSoup(html, "html5lib")

    # # Remove comments, as well as meta, title and head elements
    # remove_metadata(soup)

    # Remove blacklisted elements
    remove_blacklist(soup)

    # PRINTALL(soup)

    # Flatten elements where we want to keep the text but drop the containing tag
    flatten_elements(soup)

    # print("*V post-flatten_elements V*")
    # PRINTALL(soup)
    # print("*^ post-flatten_elements ^*")

    # Process elements with special innerText handling
    process_special_elements(soup)

    # print("*V post-process_special_elements V*")
    # PRINTALL(soup)
    # print("*^ post-process_special_elements ^*")

    # Remove empty string elements
    remove_empty_strings(soup)

    # print("*V post-remove_empty_strings V*")
    # PRINTALL(soup)
    # print("*^ post-remove_empty_strings ^*")

    # Replace <br> and <hr> elements with break indicator
    identify_linebreaks(soup)

    # print("*V post-identify_linebreaks V*")
    # PRINTALL(soup)
    # print("*^ post-identify_linebreaks ^*")

    # Normalise all strings, removing whitespace and fixing unicode issues
    normalise_strings(soup)

    # print("*V post-normalise_strings V*")
    # PRINTALL(soup)
    # print("*^ post-normalise_strings ^*")

    # Consolidate text, joining any consecutive NavigableStrings together
    consolidate_text(soup)

    # print("*V post-consolidate_text V*")
    # PRINTALL(soup)
    # print("*^ post-consolidate_text ^*")

    # Wrap any remaining bare text in <p> tags
    wrap_bare_text(soup)

    # print("*V post-wrap_bare_text V*")
    # PRINTALL(soup)
    # print("*^ post-wrap_bare_text ^*")

    # Strip tag attributes
    strip_attributes(soup)

    # print("*V post-strip_attributes V*")
    # PRINTALL(soup)
    # print("*^ post-strip_attributes ^*")

    # Replace the linebreak placeholders
    apply_linebreaks(soup)

    # print("*V post-apply_linebreaks V*")
    # PRINTALL(soup)
    # print("*^ post-apply_linebreaks ^*")

    # # Recursively replace any elements which contain 0 or 1 children
    # recursively_flatten(soup)

    # PRINTALL(soup)

    # Finally wrap the whole tree in a div
    root = soup.new_tag("div")
    root.append(soup)
    return root