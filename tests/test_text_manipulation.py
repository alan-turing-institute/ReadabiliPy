from ReadabiliPy.text_manipulation import normalise_unicode, normalise_whitespace, normalise_text, simplify_html, strip_control_characters

def test_unicode_normalisation():
    nfd_form = "Ame\u0301lie"
    nfc_form = "Amélie"
    assert normalise_unicode(nfd_form) == normalise_unicode(nfc_form)


def test_all_whitespace_is_normalised_to_empty_string():
    tab_space_new_line_tab_space = "\t \n\t "
    assert normalise_whitespace(tab_space_new_line_tab_space) == ""


def test_text_normalisation():
    unnormalised_string = "Ame\u0301lie   Poulain"
    assert normalise_text(unnormalised_string) == "Amélie Poulain"


def test_simplify_html():
    formatted_string = """
    <html>
        <body>
            <p>Some text here</p>
        </body>
    </html>
    """
    assert simplify_html(formatted_string) == "<html><body><p>Some text here</p></body></html>"


def test_strip_control_characters():
    unnormalised_string = "A string with non-printing characters and tabs	in​cluded﻿"
    assert strip_control_characters(unnormalised_string) == "A string with non-printing characters and tabs	included"
    assert normalise_text(unnormalised_string) == "A string with non-printing characters and tabs included"
