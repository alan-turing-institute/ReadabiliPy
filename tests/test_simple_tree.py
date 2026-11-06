"""Tests for simple_tree functions."""
from unittest import mock

import pytest
from bs4 import BeautifulSoup
from bs4.element import Tag

from readabilipy import simple_json_from_html_string, simple_tree_from_html_string
from readabilipy.simplifiers import strip_html_whitespace


EMPTY_HTML = [
    pytest.param("", id="empty"),
    pytest.param(" \n\t ", id="whitespace"),
    pytest.param("<!-- comment --><!---->", id="comments"),
    pytest.param("<!DOCTYPE html>", id="doctype"),
    pytest.param("<html></html>", id="empty-html"),
    pytest.param(
        "<script>ignored()</script><style>body { color: red; }</style>"
        "<form>Ignored form text</form>", id="blacklisted"
    ),
    pytest.param("<div><section><p> </p></section></div>", id="nested-empty"),
    pytest.param("""
        <!doctype html>
        <html lang="en">
          <head>
            <meta charset="UTF-8" />
            <script type="module" crossorigin src="/blog/assets/app.js"></script>
          </head>
          <body class="min-h-screen w-full bg-white antialiased">
            <div id="root"></div>
          </body>
        </html>
    """, id="issue-123-spa"),
]


@pytest.mark.parametrize("html", EMPTY_HTML)
def test_empty_tree(html):
    tree = simple_tree_from_html_string(html)
    assert isinstance(tree, Tag)
    assert tree.name == "div"
    assert tree.contents == []
    assert str(tree) == "<div></div>"


@pytest.mark.parametrize("html", EMPTY_HTML)
@pytest.mark.parametrize("content_digests", [False, True])
@pytest.mark.parametrize("node_indexes", [False, True])
@pytest.mark.parametrize("use_readability", [False, True])
def test_empty_tree_json(html, content_digests, node_indexes, use_readability):
    with mock.patch("readabilipy.simple_json.have_node", return_value=False) as have_node:
        article = simple_json_from_html_string(
            html, content_digests=content_digests, node_indexes=node_indexes,
            use_readability=use_readability
        )
    if use_readability:
        have_node.assert_called_once_with()
    else:
        have_node.assert_not_called()
    attributes = ''
    if content_digests:
        attributes += ' data-content-digest=""'
    if node_indexes:
        attributes += ' data-node-index="0"'
    assert article == {
        "title": None,
        "byline": None,
        "date": None,
        "content": "<div></div>",
        "plain_content": f"<div{attributes}></div>",
        "plain_text": [],
    }


@pytest.mark.parametrize("html, expected, tree_type, texts", [
    ("<p>First</p>", "<div><p>First</p></div>", Tag, ["First"]),
    ("<div><p>First</p></div>", "<div><p>First</p></div>", BeautifulSoup, ["First"]),
    ("<p>First</p><p>Second</p>", "<div><p>First</p><p>Second</p></div>",
     Tag, ["First", "Second"]),
])
def test_nonempty_tree(html, expected, tree_type, texts):
    tree = simple_tree_from_html_string(html)
    assert isinstance(tree, tree_type)
    assert tree.name == ("[document]" if tree_type is BeautifulSoup else "div")
    assert str(tree) == expected
    article = simple_json_from_html_string(html)
    assert article["content"] == expected
    assert article["plain_content"] == expected
    assert article["plain_text"] == [{"text": text} for text in texts]


def test_remove_cdata():
    """Test all possible methods of CData inclusion. Note that in the final
    example the '//' prefixes have no effect (since we are not in a <script>)
    tag and so we expect that the first will be displayed (tested in Chrome and
    Safari)."""
    html = """
        <div>
            <p>Some text <![CDATA[Text inside two tags]]></p>
            <![CDATA[Text inside one tag]]>
        </div>
        <![CDATA[Text outside tags]]>
        <script type="text/javascript">
            //<![CDATA[
            document.write("<");
            //]]>
        </script>
        //<![CDATA[
            invalid CDATA block
        //]]>
    """.strip()
    parsed_html = str(simple_tree_from_html_string(html))
    expected_output = "<div><div><p>Some text</p></div><p>//</p></div>"
    assert strip_html_whitespace(parsed_html) == expected_output
