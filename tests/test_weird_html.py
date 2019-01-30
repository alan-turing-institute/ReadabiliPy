"""Tests for weird HTML input."""
from pytest import mark
from .checks import check_exact_html_output
from ..readabilipy import text_manipulation


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


# Test whitespace around tags
@mark.parametrize('terminal_punctuation', text_manipulation.terminal_punctuation_marks)
def test_ensure_correct_punctuation_joining(terminal_punctuation):
    """Do not join with ' ' if the following character is a punctuation mark."""
    check_exact_html_output("""
        <div>
            <p>
                Some text <a href="example.com">like this</a>{0} with punctuation.
            </p>
        </div>""".format(terminal_punctuation),
        """<div><p>Some text like this{0} with punctuation.</p></div>""".format(terminal_punctuation))


@mark.parametrize('matched_pair', text_manipulation.matched_punctuation_marks)
def test_ensure_correct_bracket_quote_joining(matched_pair):
    """Do not join with ' ' if the following character is a punctuation mark."""
    check_exact_html_output("""
        <div>
            <p>
                Some text {0}<a href="example.com">like this</a>{1} with punctuation.
            </p>
        </div>""".format(*matched_pair),
        """<div><p>Some text {0}like this{1} with punctuation.</p></div>""".format(*matched_pair))


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
