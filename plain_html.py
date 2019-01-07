"""Turn input HTML into a cleaned parsed tree."""
from bs4 import BeautifulSoup, CData, Comment, Doctype
from .text_manipulation import normalise_text

BREAK_INDICATOR = "|BREAK_HERE|"


def elements_to_delete():
    """Elements that will be deleted together with their contents."""
    html5_form_elements = ['button', 'datalist', 'fieldset', 'form', 'input',
                           'label', 'legend', 'meter', 'optgroup', 'option',
                           'output', 'progress', 'select', 'textarea']
    html5_image_elements = ['area', 'img', 'map', 'picture', 'source']
    html5_media_elements = ['audio', 'track', 'video']
    html5_embedded_elements = ['embed', 'iframe', 'math', 'object', 'param', 'svg']
    html5_interactive_elements = ['details', 'dialog', 'summary']
    html5_scripting_elements = ['canvas', 'noscript', 'script', 'template']
    html5_data_elements = ['data', 'link']
    html5_formatting_elements = ['style']
    html5_navigation_elements = ['nav']

    elements = html5_form_elements + html5_image_elements \
        + html5_media_elements + html5_embedded_elements \
        + html5_interactive_elements + html5_scripting_elements \
        + html5_data_elements + html5_formatting_elements \
        + html5_navigation_elements

    return elements


def elements_to_replace_with_contents():
    """Elements that we will discard while keeping their contents."""
    elements = ['a', 'abbr', 'address', 'b', 'bdi', 'bdo', 'center', 'cite',
                'code', 'del', 'dfn', 'em', 'i', 'html', 'ins', 'kbs', 'mark',
                'rb', 'ruby', 'rp', 'rt', 'rtc', 's', 'samp', 'small', 'span',
                'strong', 'time', 'u', 'var', 'wbr']
    return elements


def special_elements():
    """Elements that we will discard while keeping their contents that need
    additional processing."""
    elements = ['q', 'sub', 'sup']
    return elements


def block_level_whitelist():
    """Elements that we will always accept."""
    elements = ['article', 'aside', 'blockquote', 'caption', 'colgroup', 'col',
                'div', 'dl', 'dt', 'dd', 'figure', 'figcaption', 'footer',
                'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'header', 'li', 'main',
                'ol', 'p', 'pre', 'section', 'table', 'tbody', 'thead',
                'tfoot', 'tr', 'td', 'th', 'ul']
    return elements


def structural_elements():
    """Structural elements we do no further processing on (though we do remove attributes and alter their contents)"""
    return ['html', 'head', 'body']


def metadata_elements():
    """Metadata elements we do no further processing on (though we do remove attributes and alter their contents)"""
    return ['meta', 'link', 'base', 'title']


def linebreak_elements():
    return ['br', 'hr']


def known_elements():
    """All elements that we know by name."""
    return structural_elements() + metadata_elements() + linebreak_elements() + elements_to_delete() \
        + elements_to_replace_with_contents() + special_elements() \
        + block_level_whitelist()


def remove_metadata(soup):
    """Remove comments and doctype. These are not rendered by browsers."""
    for comment in soup.findAll(string=lambda text: any([isinstance(text, x) for x in [Comment, Doctype]])):
        comment.extract()


def process_cdata(soup):
    """Remove CData. We were a bit worried about potentially removing content here but satisfied ourselves it won't
    be displayed by most browsers in most cases (see https://github.com/alan-turing-institute/ReadabiliPy/issues/32)"""
    for cdata in soup.findAll(string=lambda text: isinstance(text, CData)):
        cdata.extract()


def remove_blacklist(soup):
    """Remove all blacklisted elements."""
    for element_name in elements_to_delete():
        for element in soup.find_all(element_name):
            element.decompose()


def unwrap_elements(soup):
    """Flatten all elements where we are only interested in their contents."""
    # We do not need to unwrap from the "bottom up" as all we are doing is replacing elements with their contents so
    # we will still find child elements after their parent has been unwrapped.
    for element_name in elements_to_replace_with_contents():
        for element in soup.find_all(element_name):
            element.unwrap()


def process_special_elements(soup):
    """Flatten special elements while processing their contents."""
    for element_name in special_elements():
        for element in soup.find_all(element_name):
            if element.name == 'q':
                element.string = '"{0}"'.format(element.string)
            if element.name == 'sub':
                element.string = '_{0}'.format(element.string)
            if element.name == 'sup':
                element.string = '^{0}'.format(element.string)
            element.unwrap()


def remove_empty_strings(soup):
    """Remove any strings which contain only whitespace. Without this,
    consecutive linebreaks may not be identified correctly."""
    for element in soup.find_all(string=True):
        if not normalise_text(str(element)):
            element.extract()


def identify_linebreaks(soup):
    """Identify linebreaks."""
    # Iterate through the <br> elements in the tree
    for element in soup.find_all('br'):
        # When the next element is not another <br> count how long the chain is
        if (element.next_sibling is None) or (element.next_sibling.name != 'br'):
            br_element_chain = [element]
            while (br_element_chain[-1].previous_sibling is not None) and (br_element_chain[-1].previous_sibling.name == 'br'):
                br_element_chain.append(br_element_chain[-1].previous_sibling)

            # If there's only one <br> then we strip it out
            if len(br_element_chain) == 1:
                br_element_chain[0].decompose()
            # If there are multiple <br>s then replace them with BREAK_INDICATOR
            else:
                br_element_chain[0].replace_with(BREAK_INDICATOR)
                for inner_element in br_element_chain[1:]:
                    inner_element.decompose()

    # Iterate through the tree, replacing <hr> with BREAK_INDICATOR
    for element in soup.find_all('hr'):
        # This check is needed since we're modifying the list while iterating through it
        if element.name == 'hr':
            element.replace_with(BREAK_INDICATOR)


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
            # Join with no spaces if this is a smart quotation mark
            if str(element.previous_sibling)[-1] in ['“', '‘'] or str(element)[0] in ['”', '’']:
                text = "".join([str(element.previous_sibling), str(element)])
            else:
                text = " ".join([str(element.previous_sibling), str(element)])
            element.previous_sibling.replace_with(text)
            element.extract()


def split_strings_on_linebreaks(soup):
    """Split strings on linebreak markers. If the parent is a <p> tag then close-parent reopen-parent."""
    # Iterate through the tree, splitting elements which contain BREAK_INDICATOR
    # Use a list rather than the generator, since we are altering the tree as we traverse it
    for element in list(soup.find_all(string=True)):
        if BREAK_INDICATOR in element:
            # Split the text into two or more fragments (there maybe be multiple BREAK_INDICATORs in the string)
            text_fragments = [s.strip() for s in str(element).split(BREAK_INDICATOR)]

            # Get the parent element
            parent_element = element.parent

            # If the parent is a paragraph then we want to close and reopen by creating a new tag
            if parent_element.name == "p":
                # Iterate in reverse order as we are repeatedly adding new elements directly after the original one
                for text_fragment in text_fragments[:0:-1]:
                    new_p_element = soup.new_tag("p")
                    new_p_element.string = text_fragment
                    parent_element.insert_after(new_p_element)
                parent_element.string.replace_with(text_fragments[0])
            # Otherwise we want to simply include all the text fragments as independent NavigableStrings (that will be wrapped later)
            else:
                # Iterate in reverse order as we are repeatedly adding new elements directly after the original one
                for text_fragment in text_fragments[:0:-1]:
                    element.insert_after(soup.new_string(text_fragment))
                element.string.replace_with(text_fragments[0])


def wrap_bare_text(soup):
    """Wrap any remaining bare text in <p> tags."""
    # Iterate over all strings in the tree
    for element in soup.find_all(string=True):
        # If this is the only child of a whitelisted block then do nothing
        if element.parent.name in block_level_whitelist() and len(element.parent.contents) == 1:
            pass
        # ... otherwise wrap them in <p> tags
        else:
            p_element = soup.new_tag("p")
            p_element.string = element
            element.replace_with(p_element)


def strip_attributes(soup):
    """Strip class and style attributes."""
    for element in soup.find_all():
        element.attrs.pop("class", None)
        element.attrs.pop("style", None)


def recursively_prune(soup):
    """Recursively prune out any elements which have no children."""
    def single_replace():
        n_removed = 0
        for element in soup.find_all(lambda elem: len(list(elem.children)) == 0):
            element.decompose()
            n_removed += 1
        return n_removed
    # Repeatedly apply single_replace() until no elements are being removed
    while single_replace():
        pass


def process_unknown_elements(soup):
    """Replace any unknown elements with their contents."""
    for element in soup.find_all():
        if element.name not in known_elements():
            element.unwrap()


def parse_to_tree(html):
    """Turn input HTML into a cleaned parsed tree."""
    # Insert space into non-spaced comments so that html5lib can interpret them correctly
    html = html.replace("<!---->", "<!-- -->")

    # Convert the HTML into a Soup parse tree
    soup = BeautifulSoup(html, "html5lib")

    # Remove comments and DOCTYPE strings
    remove_metadata(soup)

    # Handle CDATA
    process_cdata(soup)

    # Remove blacklisted elements
    remove_blacklist(soup)

    # Flatten elements where we want to keep the text but drop the containing tag
    unwrap_elements(soup)

    # Process elements with special innerText handling
    process_special_elements(soup)

    # Process unknown elements
    process_unknown_elements(soup)

    # Remove empty string elements
    remove_empty_strings(soup)

    # Replace <br> and <hr> elements with break indicator
    identify_linebreaks(soup)

    # Normalise all strings, removing whitespace and fixing unicode issues.
    # Must happen AFTER identifying linebreaks and BEFORE applying converting these linebreaks to text blocks.
    normalise_strings(soup)

    # Consolidate text, joining any consecutive NavigableStrings together
    # Must happen AFTER identifying linebreaks and BEFORE applying converting these linebreaks to text blocks.
    consolidate_text(soup)

    # Convert the linebreak placeholders to text blocks. This must happen AFTER we do any consolidation of raw text as
    # otherwise we risk wrapping text that would not display as separate visual paragraphs in the original page with
    # block level elements that mean they will display as separate visual paragraphs in the simplified page.
    split_strings_on_linebreaks(soup)

    # Wrap any remaining bare text in a suitable block level element
    # Must happen AFTER identifying linebreaks and BEFORE applying converting these linebreaks to text blocks.
    wrap_bare_text(soup)

    # Recursively replace any elements which contain 0 or 1 children
    recursively_prune(soup)

    # Strip tag attributes
    strip_attributes(soup)

    # Finally ensure that the whole tree is wrapped in a div
    # Strip out enclosing elements that cannot live inside a div
    while soup.contents and (soup.contents[0].name in ["html", "body"]):
        soup.contents[0].unwrap()
    # If the outermost tag is a single div then return it
    if len(soup.contents) == 1 and soup.contents[0].name == "div":
        return soup
    # ... otherwise wrap in a div and return that
    root = soup.new_tag("div")
    root.append(soup)
    return root
