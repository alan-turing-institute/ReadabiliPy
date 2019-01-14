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
    elements = [plain_element(element, False, False) for element in soup.contents]
    assert elements == ["<div><p>Text</p><!----></div>"]