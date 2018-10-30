from bs4 import BeautifulSoup
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
            article_json["plain_content"] = extract_paragraphs_as_plain_text(readability_json["content"])

    return article_json


def extract_paragraphs_as_plain_text(paragraph_html):
    # Load article as DOM
    soup = BeautifulSoup(paragraph_html, 'html.parser')
    # Select all paragraphs
    paragraphs = soup.find_all('p')
    # Extract text for each paragraph
    paragraphs = [p.get_text() for p in paragraphs]
    # Normalise unicode such that things that are visually equivalent map tot he same unicode string where possible
    normal_form = "NFKC"
    paragraphs = [unicodedata.normalize(normal_form, p) for p in paragraphs]
    # Strip leading and trailing whitespace
    paragraphs = [p.strip() for p in paragraphs]
    # Drop empty paragraphs
    paragraphs = list(filter(None, paragraphs))
    return paragraphs
