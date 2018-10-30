from bs4 import BeautifulSoup
from bs4.element import Comment, NavigableString
import hashlib
import json
import os
from subprocess import check_call
import tempfile
import unicodedata


def parse(html):
    temp_dir = tempfile.gettempdir()
    # Write input HTML to temporary file so it is available to the node.js script
    html_path = os.path.join(temp_dir, "full.html");
    with open(html_path, 'w') as f:
        f.write(html)

    # Call Mozilla's Readability.js Readability.parse() function via node, writing output to a temporary file
    article_json_path = os.path.join(temp_dir, "article.json");
    parse_script_path = os.path.join(os.path.dirname(__file__), "ExtractArticle.js")
    check_call(["node", parse_script_path, "-i", html_path, "-o", article_json_path])

    # Read output of call to Readability.parse() from JSON file and return as Python dictionary
    with open(article_json_path) as f:
        readability_json = json.loads(f.read())

    # Only keep the subset of Readability.js fields we are using (and therefore testing for accuracy of extraction)
    # TODO: Add tests for additional fields and include them when we look at packaging this wrapper up for PyPI
    # Initialise output article to include all fields with null values
    article_json = {
        "title": None,
        "byline": None,
        "content": None,
        "plain_content": None
    }
    # Populate article fields from readability fields where present
    if readability_json:
        if "title" in readability_json and readability_json["title"] is not "":
            article_json["title"] = readability_json["title"]
        if "byline" in readability_json and readability_json["byline"] is not "":
            article_json["byline"] = readability_json["byline"]
        if "content" in readability_json and readability_json["content"] is not "":
            article_json["content"] = readability_json["content"]
            article_json["plain_content"] = plain_content(readability_json["content"])

    return article_json


def plain_content(readability_content):
    # Load article as DOM
    soup = BeautifulSoup(readability_content, 'html.parser')
    # Make all elements plain
    plain_elements = [plain_element(content) for content in soup.contents]
    # Replace article contents with plain elements
    soup.contents = plain_elements

    return str(soup)


def plain_element(element):
    # For lists, we make each item plain text
    leaf_nodes = ['p', 'li']
    leaf_types = [NavigableString, Comment]
    if element.name in leaf_nodes:
        # For leaf node elements, extract the text content, discarding any HTML tags
        # 1. Get element contents as text
        plain_text = element.get_text()
        # 2. Normalise the extracted text string to a canonical representation
        plain_text = normalise_text(plain_text)
        # 3. Drop element if plain_text is empty
        if plain_text == "":
            element = None
        else:
            # 4. Update element content to be plain text
            element.string = plain_text
            # Set ID of element to SHA-256 hash of plain content
            element['id'] = hashlib.sha256(element.string.encode('utf-8')).hexdigest()
    elif type(element) in leaf_types:
        plain_text = element.string
        plain_text = normalise_text(plain_text)
        if plain_text == "":
            element = None
        else:
            element.string = plain_text
    else:
        # If not a leaf node or leaf type call recursively on child nodes, replacing
        element.contents = [plain_element(content) for content in element.contents]
        content_hash = hashlib.sha256()
        for content in element.contents:
            if content and type(content) not in leaf_types:
                content_hash.update(content["id"].encode('utf-8'))
        element["id"] = content_hash.hexdigest()
    return element


def normalise_text(text):
    # Normalise the unicode representation
    normal_form = "NFKC"
    text = unicodedata.normalize(normal_form, text)
    # Strip leading and training whitespace again (ensures things like non-breaking whitespaces are removed)
    text = text.strip()
    return text
