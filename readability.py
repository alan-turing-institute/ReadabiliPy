from bs4 import BeautifulSoup
import json
import os
from subprocess import check_call
import tempfile


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
        readability_json= json.loads(f.read())

    # Only keep the subset of Readability.js fields we are using (and therefore testing for accuracy of extraction)
    # TODO: Add tests for additional fields and include them when we look at packaging this wrapper up for PyPI
    article_json = dict()
    article_json["title"] = readability_json["title"]
    article_json["byline"] = readability_json["byline"]
    article_json["content"] = readability_json["content"]

    return article_json

