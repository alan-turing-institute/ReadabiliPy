# from .checks import check_extract_article
from bs4 import BeautifulSoup
from ..readabilipy.json_parser import plain_element


def test_plain_element_with_comments():
    """Contents of comments should be stripped but the comment itself should be kept."""
    html = """
        <div>
            <p>Text</p>
            <!-- comment -->
        </div>
    """.strip()
    soup = BeautifulSoup(html, 'html.parser')
    elements = [str(plain_element(element, False, False)) for element in soup.contents]
    assert elements == ["<div><p>Text</p><!----></div>"]


def test_content_digest_on_filled_and_empty_elements():
    """Filled strings should get a digest but empty strings should not."""
    html = """
        <div>
            <p>Text</p>
            <p></p>
        </div>
    """.strip()
    soup = BeautifulSoup(html, 'html.parser')
    elements = [str(plain_element(element, True, True)) for element in soup.contents]
    assert elements == ['<div><p data-content-digest="71988c4d8e0803ba4519f0b2864c1331c14a1890bf8694e251379177bfedb5c3">Text</p><p data-content-digest=""></p></div>']