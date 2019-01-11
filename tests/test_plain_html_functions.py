"""Tests for plain_html functions."""
from bs4 import BeautifulSoup
from ..readabilipy import plain_html

def test_remove_metadata():
    html = """
        <!DOCTYPE html>
        <html>
        <head></head>
        <body>
        <!-- Comment here -->
        </body>
        </html>
    """
    soup = BeautifulSoup(html, "html5lib")
    plain_html.remove_metadata(soup)
    assert "<!-- Comment here -->" not in str(soup)


def test_remove_blacklist():
    html = """
        <html>
        <body>
            <button type="button">Click Me!</button>
            <p>Hello</p>
        <body>
        </html>
    """
    soup = BeautifulSoup(html, "html5lib")
    plain_html.remove_blacklist(soup)
    assert "button" not in str(soup)
