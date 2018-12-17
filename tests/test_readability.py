"""Test readability.py on sample articles"""
import json
import os
from ReadabiliPy import readability, text_manipulation

# ===== TEST END TO END ARTICLE EXTRACTION =====


def check_extract_article(test_filename, expected_filename, content_digests=False, node_indexes=False):
    test_data_dir = "data"
    # Read HTML test file
    test_filepath = os.path.join(os.path.dirname(
        __file__), test_data_dir, test_filename)
    with open(test_filepath) as h:
        html = h.read()

    # Extract simplified article HTML
    article_json = readability.parse(html, content_digests, node_indexes)
    print(article_json)

    # Get expected simplified article HTML
    expected_filepath = os.path.join(os.path.dirname(__file__),
                                     test_data_dir, expected_filename)
    with open(expected_filepath) as h:
        expected_article_json = json.loads(h.read())

    # Test full JSON matches (checks for unexpected fields in either actual or expected JSON)
    assert article_json == expected_article_json


def check_exact_html_output(test_fragment, expected_output=None):
    """Check that expected output is present when parsing HTML fragment."""
    if expected_output is None:
        expected_output = test_fragment
    article_json = readability.parse(test_fragment)
    content = str(article_json["plain_content"])
    # Check that expected output is present after simplifying the HTML
    normalised_output = text_manipulation.simplify_html(expected_output)
    normalised_content = text_manipulation.simplify_html(content)
    assert normalised_output == normalised_content


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


def test_extract_article_non_article():
    check_extract_article(
        "non_article_full_page.html",
        "non_article_full_page.json"
    )


def test_extract_article_unicode_normalisation():
    check_extract_article(
        "conservativehq.com-1_full_page.html",
        "conservativehq.com-1_simple_article_from_full_page.json"
    )


def test_extract_article_list_items():
    check_extract_article(
        "list_items_full_page.html",
        "list_items_simple_article_from_full_page.json"
    )


def test_extract_article_headers_and_non_paragraph_blockquote_text():
    check_extract_article(
        "davidwolfe.com-1_full_page.html",
        "davidwolfe.com-1_simple_article_from_full_page.json"
    )


def test_extract_article_list_items_content_digests():
    check_extract_article(
        "list_items_full_page.html",
        "list_items_simple_article_from_full_page_content_digests.json",
        content_digests=True
    )


def test_extract_article_list_items_node_indexes():
    check_extract_article(
        "list_items_full_page.html",
        "list_items_simple_article_from_full_page_node_indexes.json",
        node_indexes=True
    )


def test_extract_article_full_page_content_digest():
    check_extract_article(
        "addictinginfo.com-1_full_page.html",
        "addictinginfo.com-1_simple_article_from_full_page_content_digest.json",
        content_digests=True
    )


def test_extract_article_full_page_node_indexes():
    check_extract_article(
        "addictinginfo.com-1_full_page.html",
        "addictinginfo.com-1_simple_article_from_full_page_node_indexes.json",
        node_indexes=True
    )


def test_extract_article_full_page_content_digest_node_indexes():
    check_extract_article(
        "addictinginfo.com-1_full_page.html",
        "addictinginfo.com-1_simple_article_from_full_page_content_digest_node_indexes.json",
        content_digests=True,
        node_indexes=True
    )


# ==== TEST PLAIN TEXT EXTRACTION =====
def check_extract_paragraphs_as_plain_text(test_filename, expected_filename):
    test_data_dir = "data"
    # Read readable article test file
    test_filepath = os.path.join(os.path.dirname(__file__),
                                 test_data_dir, test_filename)
    with open(test_filepath) as h:
        article = json.loads(h.read())

    # Extract plain text paragraphs
    paragraphs = readability.extract_text_blocks_as_plain_text(
        article["plain_content"])

    # Get expected plain text paragraphs
    expected_filepath = os.path.join(os.path.dirname(__file__),
                                     test_data_dir, expected_filename)
    with open(expected_filepath) as h:
        expected_paragraphs = json.loads(h.read())

    # Test
    print(paragraphs)
    assert paragraphs == expected_paragraphs


def test_extract_paragraphs_as_plain_text():
    check_extract_paragraphs_as_plain_text(
        "addictinginfo.com-1_simple_article_from_full_article.json",
        "addictinginfo.com-1_plain_text_paragraphs_from_simple_article.json"
    )


def test_extract_paragraphs_as_plain_text_node_indexes():
    check_extract_paragraphs_as_plain_text(
        "list_items_simple_article_from_full_page_node_indexes.json",
        "list_items_plain_text_paragraph_node_indexes.json"
    )


# Test correct wrapping
def test_ensure_correct_div_wrapping():
    """Do not wrap in a <div> if this is already a <div>."""
    check_exact_html_output("""
        <div>
            <p>
                Some example text here.
            </p>
        </div>""",
    """<div><p>Some example text here.</p></div>""")

