from ReadabiliPy import readability
from pytest import mark


def check_html_fragment(test_fragment, expected_in_output):
    """Check that expected output is present when parsing a test HTML fragment."""
    article_json = readability.parse(test_fragment)
    assert(expected_in_output in article_json["plain_content"])


def check_whitelisted_html_fragment(test_fragment):
    check_html_fragment(test_fragment, test_fragment)


@mark.parametrize("element", ["article", "aside", "blockquote", "caption", "colgroup",
                                     "col", "div", "dl", "dt", "dd", "figure", "figcaption",
                                     "footer", "h1", "h2", "h3", "h4", "h5", "h6", "header",
                                     "li", "main", "ol", "p", "pre", "section", "table",
                                     "tbody", "thead", "tfoot", "tr", "td", "th", "ul"])
def test_whitelist_single_element(element):
    check_whitelisted_html_fragment('<{0}>Lorem ipsum dolor sit amet</{0}>'.format(element))
 