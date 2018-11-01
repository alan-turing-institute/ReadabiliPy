import json
import os
import subprocess
from ReadabiliPy import readability
import tempfile


def check_extract_article(test_filename, expected_filename, content_digests=False, node_indexes=False):
    test_data_dir = "data"
    # Read HTML test file
    test_filepath = os.path.join(os.path.dirname(__file__), test_data_dir, test_filename)
    with open(test_filepath) as h:
        html = h.read()

    # Extract simplified article HTML
    article_json = readability.parse(html, content_digests, node_indexes)

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

# def test_extract_article_full_page_content_digest():
#     check_extract_article(
#         "addictinginfo.com-1_full_page.html",
#         "addictinginfo.com-1_simple_article_from_full_page.json",
#         content_digests=True
#     )


def check_extract_paragraphs_as_plain_text(test_filename, expected_filename):
    test_data_dir = "data"
    # Read readable article test file
    test_filepath = os.path.join(os.path.dirname(__file__), test_data_dir, test_filename)
    with open(test_filepath) as h:
        article = json.loads(h.read())

    # Extract plain text paragraphs
    paragraphs = readability.extract_paragraphs_as_plain_text(article["content"])

    # Get expected plain text paragraphs
    expected_filepath = os.path.join(os.path.dirname(__file__), test_data_dir, expected_filename)
    with open(expected_filepath) as h:
        expected_paragraphs = json.loads(h.read())

    # Test
    assert paragraphs == expected_paragraphs


def test_extract_paragraphs_as_plain_text():
    check_extract_paragraphs_as_plain_text(
        "addictinginfo.com-1_simple_article_from_full_article.json",
        "addictinginfo.com-1_plain_text_paragraphs_from_simple_article.json"
    )


def validate_extract_article_command_line_script(test_html_filepath, expected_article_json_filepath,
                                                 content_digest=False, node_indexes=False):
    # Set output file path to temp file
    temp_dir = tempfile.gettempdir()
    article_json_filepath = os.path.join(temp_dir, "article.json")
    # Call extract article command line script
    script_path = os.path.join(os.path.dirname(__file__), "..", "extract_article.py")
    subprocess.check_call(["python", script_path, "-i", test_html_filepath, "-o", article_json_filepath])

    # Call extract article command line script
    script_path = os.path.join(os.path.dirname(__file__), "..", "extract_article.py")
    cmd = ["python", script_path, "-i", test_html_filepath, "-o", article_json_filepath]
    # Only add optional commandline argument if provided. This way we casn test the default behaviour works for
    # optional arguments when they are not provided
    if content_digest:
        cmd = cmd + ["-c"]
    if node_indexes:
        cmd = cmd + ["-n"]
    # Call command line script
    subprocess.check_call(cmd)

    # Test
    with open(article_json_filepath) as actual, open(expected_article_json_filepath) as expected:
        actual_article = json.loads(actual.read())
        expected_article = json.loads(expected.read())
        assert actual_article == expected_article


def test_extract_article_command_line_script():
    # Set input file path to test HTML file
    test_data_dir = "data"
    test_html_filename = "addictinginfo.com-1_full_page.html"
    test_html_filepath = os.path.join(os.path.dirname(__file__), test_data_dir, test_html_filename)
    # Set path for expected article JSON file
    expected_article_json_filename = "addictinginfo.com-1_simple_article_from_full_page.json"
    expected_article_json_filepath = os.path.join(os.path.dirname(__file__), test_data_dir,
                                                  expected_article_json_filename)

    # Test
    validate_extract_article_command_line_script(test_html_filepath, expected_article_json_filepath)


def test_extract_article_command_line_script_content_digest():
    # Set input file path to test HTML file
    test_data_dir = "data"
    test_html_filename = "list_items_full_page.html"
    test_html_filepath = os.path.join(os.path.dirname(__file__), test_data_dir, test_html_filename)
    # Set path for expected article JSON file
    expected_article_json_filename = "list_items_simple_article_from_full_page_content_digests.json"
    expected_article_json_filepath = os.path.join(os.path.dirname(__file__), test_data_dir,
                                                  expected_article_json_filename)

    # Test
    validate_extract_article_command_line_script(test_html_filepath, expected_article_json_filepath,
                                                 content_digest=True)


def test_extract_article_command_line_script_node_indexes():
    # Set input file path to test HTML file
    test_data_dir = "data"
    test_html_filename = "list_items_full_page.html"
    test_html_filepath = os.path.join(os.path.dirname(__file__), test_data_dir, test_html_filename)
    # Set path for expected article JSON file
    expected_article_json_filename = "list_items_simple_article_from_full_page_node_indexes.json"
    expected_article_json_filepath = os.path.join(os.path.dirname(__file__), test_data_dir,
                                                  expected_article_json_filename)

    # Test
    validate_extract_article_command_line_script(test_html_filepath, expected_article_json_filepath,
                                                 node_indexes=True)

