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
    check_exact_html_output("""
        <div>
            <iframe src="https://www.youtube.com/embed/BgB5E91lD6s" width="640" height="355" frameborder="0" allowfullscreen="allowfullscreen"></iframe>
        </div>
    """, "<div></div>")