import json
import os
from ReadabiliPy import readability


def check_extract_article(test_filename, expected_filename):
    test_data_dir = "data"
    # Read HTML test file
    test_filepath = os.path.join(os.path.dirname(__file__), test_data_dir, test_filename)
    with open(test_filepath) as h:
        html = h.read()

    # Extract simplified article HTML
    article_json = readability.parse(html)

    # Get expected simplified article HTML
    expected_filepath = os.path.join(os.path.dirname(__file__), test_data_dir, expected_filename)
    with open(expected_filepath) as h:
        expected_article_json = json.loads(h.read())

    # Test full JSON matches (checks for unexpected fields in either actual or expected JSON)
    assert article_json == expected_article_json


def test_extract_article_full_page():
    check_extract_article(
        "addictinginfo.com-1_full_page.html",
        "addictinginfo.com-1_simple_article_from_full_page.json"
    )


def test_extract_article_full_article():
    check_extract_article(
        "addictinginfo.com-1_full_article.html",
        "addictinginfo.com-1_simple_article_from_full_article.json"
    )
