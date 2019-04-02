from .extract_element import extract_element


def extract_byline(html):
    """Return the article byline from the article HTML"""

    # List of xpaths for HTML tags that could contain a byline
    # Tuple scores reflect confidence in these xpaths and the preference used for extraction
    xpaths = [
        ('//meta[@name="author"]/@content', 1),
        ('substring-before(substring-after(//script[contains(text(), "tq.byline")], "tq.byline = ''"), "'';")', 1)
    ]

    return extract_element(html, xpaths)
