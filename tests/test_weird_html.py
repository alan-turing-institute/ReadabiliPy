"""Tests for weird HTML input."""
from .checks import check_exact_html_output


def test_non_printing_control_characters():
    """Non-printing characters should be removed."""
    check_exact_html_output("""
        <div>
            <p>First paragraph.</p>
            <p><span>﻿</span></p>
            <p>Last paragraph.</p>
        </div>
    """, """
        <div>
            <p>First paragraph.</p>
            <p>Last paragraph.</p>
        </div>
    """)


def test_iframe_containing_tags():
    """At present we blacklist iframes completely"""
    check_exact_html_output("""
        <div>
            <iframe><span>text</span></iframe>
        </div>
        """, "<div></div>")


def test_iframe_with_source():
    """At present we blacklist iframes, but may want to extract the links in future."""
    check_exact_html_output(
        """<div><iframe src="https://www.youtube.com/embed/BgB5E91lD6s" width="640" height="355" frameborder="0" allowfullscreen="allowfullscreen"></iframe></div>""",
        "<div></div>"
    )


# Test comments inside tags
def test_comments_inside_tags():
    """Ensure that comments inside tags are removed."""
    check_exact_html_output(
        "<p>Some <!-- --> text <!-- with a comment --> here<!--or here-->.<!----></p>",
        "<div><p>Some text here.</p></div>"
    )


# Test tags inside words
def test_tags_inside_words():
    """Ensure that words with tags inside them are kept together when the tags are stripped."""
    check_exact_html_output(
        """a<a href="http://example.com">i</a>sle""",
        "<div><p>aisle</p></div>"
    )

# Test splitting for unclosed tags inside paragraphs
def test_paragraph_splitting_with_unclosed_tags():
    """Ensure that paragraphs with unclosed tags inside them split correctly."""
    check_exact_html_output(
        """
        <p>
            <meta charset="utf-8">First paragraph.
            <br><br>
            Second paragraph.
        </p>""",
        "<div><p>First paragraph.</p><p>Second paragraph.</p></div>"
    )
