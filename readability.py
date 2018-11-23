from bs4 import BeautifulSoup
from bs4.element import Comment, NavigableString
import hashlib
import json
import os
from subprocess import check_call
import tempfile
import unicodedata
from .plain_html import parse_to_tree


def parse(html, content_digests=False, node_indexes=False, use_readability=False):
    if use_readability:
        temp_dir = tempfile.gettempdir()
        # Write input HTML to temporary file so it is available to the node.js script
        html_path = os.path.join(temp_dir, "full.html")
        with open(html_path, 'w') as f:
            f.write(html)

        # Call Mozilla's Readability.js Readability.parse() function via node, writing output to a temporary file
        article_json_path = os.path.join(temp_dir, "article.json")
        parse_script_path = os.path.join(os.path.dirname(__file__), "ExtractArticle.js")
        check_call(["node", parse_script_path, "-i", html_path, "-o", article_json_path])

        # Read output of call to Readability.parse() from JSON file and return as Python dictionary
        with open(article_json_path) as f:
            input_json = json.loads(f.read())

    else:
        input_json = {
            "content": str(parse_to_tree(html))
        }
    
    # Only keep the subset of Readability.js fields we are using (and therefore testing for accuracy of extraction)
    # TODO: Add tests for additional fields and include them when we look at packaging this wrapper up for PyPI
    # Initialise output article to include all fields with null values
    article_json = {
        "title": None,
        "byline": None,
        "content": None,
        "plain_content": None,
        "plain_text": None
    }
    # Populate article fields from readability fields where present
    if input_json:
        if "title" in input_json and input_json["title"] is not "":
            article_json["title"] = input_json["title"]
        if "byline" in input_json and input_json["byline"] is not "":
            article_json["byline"] = input_json["byline"]
        if "content" in input_json and input_json["content"] is not "":
            article_json["content"] = input_json["content"]
            article_json["plain_content"] = \
                plain_content(article_json["content"], content_digests, node_indexes)
            article_json["plain_text"] = \
                extract_paragraphs_as_plain_text(article_json["plain_content"])

    return article_json


def extract_paragraphs_as_plain_text(paragraph_html):
    # Load article as DOM
    soup = BeautifulSoup(paragraph_html, 'html.parser')
    # Select all unordered lists
    lists = soup.find_all(['ul', 'ol'])
    # Prefix text in all list items with "* " and make lists paragraphs
    for l in lists:
        plain_items = "".join(list(filter(None, [plain_text_leaf_node(li)["text"] for li in l.find_all('li')])))
        l.string = plain_items
        l.name = "p"
    # Select all paragraphs
    paragraphs = soup.find_all('p')
    paragraphs = [plain_text_leaf_node(p) for p in paragraphs]
    # Drop empty paragraphs
    paragraphs = list(filter(lambda p: p["text"] is not None, paragraphs))
    return paragraphs


def plain_text_leaf_node(element):
    # Extract all text, stripped of any child HTML elements
    plain_text = element.get_text()
    # Normalise unicode such that things that are visually equivalent map to the same
    # unicode string where possible
    normal_form = "NFKC"
    plain_text = unicodedata.normalize(normal_form, plain_text)
    plain_text = plain_text.strip()
    if plain_text != "" and element.name == "li":
        plain_text = "* {}, ".format(plain_text)
    if plain_text == "":
        plain_text = None
    if "data-node-index" in element.attrs:
        plain = {"node_index": element["data-node-index"], "text": plain_text}
    else:
        plain = {"text": plain_text}
    return plain


def plain_content(readability_content, content_digests, node_indexes):
    # Load article as DOM
    soup = BeautifulSoup(readability_content, 'html.parser')
    # Make all elements plain
    elements = plain_elements(soup.contents, content_digests, node_indexes)
    if node_indexes:
        # Add node index attributes to nodes
        elements = [add_node_indexes(element) for element in elements]
    # Replace article contents with plain elements
    soup.contents = elements
    return str(soup)


def plain_elements(elements, content_digests, node_indexes):
    # Get plain content versions of all elements
    elements = [plain_element(element, content_digests, node_indexes) for element in elements]
    if content_digests:
        # Add content digest attrbiute to nodes
        elements = [add_content_digest(element) for element in elements]
    return elements


def plain_element(element, content_digests, node_indexes):
    # For lists, we make each item plain text
    if element.name in leaf_nodes():
        # For leaf node elements, extract the text content, discarding any HTML tags
        # 1. Get element contents as text
        plain_text = element.get_text()
        # 2. Normalise the extracted text string to a canonical representation
        plain_text = normalise_text(plain_text)
        # 3. Update element content to be plain text
        element.string = plain_text
    elif type(element) in leaf_types():
        plain_text = element.string
        plain_text = normalise_text(plain_text)
        element = type(element)(plain_text)
    else:
        # If not a leaf node or leaf type call recursively on child nodes, replacing
        element.contents = plain_elements(element.contents, content_digests, node_indexes)
    return element


def leaf_nodes():
    return ['p', 'li']


def leaf_types ():
    return [NavigableString, Comment]


def add_node_indexes(element, node_index="0"):
    if type(element) in leaf_types():
        # Can't add attributes to leaf string types
        return element
    else:
        # Add index to current element
        element["data-node-index"] = node_index
        # Add index to child elements
        local_idx = 0
        for child in element.contents:
            # Can't add attributes to leaf string types
            if type(child) not in leaf_types():
                local_idx = local_idx + 1
                child_index = "{stem}.{local}".format(stem=node_index, local=local_idx)
                add_node_indexes(child, node_index=child_index)
    return element


def add_content_digest(element):
    if type(element) not in leaf_types():
        element["data-content-digest"] = content_digest(element)
    return element


def content_digest(element):
    if type(element) in leaf_types():
        # Hash
        trimmed_string = element.string.strip()
        if trimmed_string == "":
            digest = ""
        else:
            digest = hashlib.sha256(trimmed_string.encode('utf-8')).hexdigest()
    else:
        contents = element.contents
        num_contents = len(contents)
        if num_contents == 0:
            # No hash when no child elements exist
            digest = ""
        elif num_contents == 1:
            # If single child, use digest of child
            digest = content_digest(contents[0])
        else:
            # Build content digest from the "non-empty" digests of child nodes
            digest = hashlib.sha256()
            child_digests = list(filter(lambda x: x != "", [content_digest(content) for content in contents]))
            [digest.update(child.encode('utf-8')) for child in child_digests]
            digest = digest.hexdigest()
    return digest


def normalise_text(text):
    # Normalise the unicode representation
    normal_form = "NFKC"
    text = unicodedata.normalize(normal_form, text)
    # Strip leading and training whitespace again (ensures things like non-breaking whitespaces are removed)
    text = text.strip()
    return text
