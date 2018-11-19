from ReadabiliPy import readability
from pytest import mark


def check_blacklisted_html_fragment(test_fragment):
    """Check that no output is present when parsing HTML fragment."""
    article_json = readability.parse(test_fragment)
    print(article_json)
    assert(article_json["plain_content"] is None)


@mark.parametrize("element", ["button", "datalist", "fieldset", "form",
                              "input", "label", "legend", "meter", "optgroup",
                              "option", "output", "progress", "select",
                              "textarea", "area", "img", "map", "picture",
                              "source", "audio", "track", "video", "embed",
                              "math", "object", "param", "svg", "details",
                              "dialog", "summary", "canvas", "noscript",
                              "script", "template", "data", "link", "time",
                              "style", "nav", "br", "hr"]) 
def test_html_blacklist_element(element):
    check_blacklisted_html_fragment('<{0}>Lorem ipsum dolor sit amet</{0}>'.format(element))
