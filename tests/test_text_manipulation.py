from ReadabiliPy.text_manipulation import normalise_unicode, normalise_whitespace, normalise_text, simplify_html, strip_control_characters

def test_unicode_normalisation():
    nfd_form = "Ame\u0301lie"
    nfc_form = "Amélie"
    assert normalise_unicode(nfd_form) == normalise_unicode(nfc_form)


def test_all_whitespace_is_normalised_to_empty_string():
    tab_space_new_line_tab_space = "\t \n\t \f \r\n"
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


def test_strip_control_characters_non_printing_characters():
    unnormalised_string = "A string with non-printing characters in​c\u200Bluded\ufeff"
    assert strip_control_characters(unnormalised_string) == "A string with non-printing characters included"
    assert normalise_text(unnormalised_string) == "A string with non-printing characters included"

def test_strip_control_characters_cr():
    unnormalised_string = "A string with new lines\rin​c\u200Bluded\ufeff"
    assert strip_control_characters(unnormalised_string) == "A string with new lines\rincluded"
    assert normalise_text(unnormalised_string) == "A string with new lines included"

def test_strip_control_characters_lf():
    unnormalised_string = "A string with new lines\ninc\u200Bluded\ufeff"
    assert strip_control_characters(unnormalised_string) == "A string with new lines\nincluded"
    assert normalise_text(unnormalised_string) == "A string with new lines included"

def test_strip_control_characters_cr_lf():
    unnormalised_string = "A string with new lines\r\nin​c\u200Bluded\ufeff"
    assert strip_control_characters(unnormalised_string) == "A string with new lines\r\nincluded"
    assert normalise_text(unnormalised_string) == "A string with new lines included"

def test_strip_control_characters_ff():
    unnormalised_string = "A string with form feed\fin​c\u200Bluded\ufeff"
    assert strip_control_characters(unnormalised_string) == "A string with form feed\fincluded"
    assert normalise_text(unnormalised_string) == "A string with form feed included"

def test_strip_control_characters_tab():
    unnormalised_string = "A string with tabs\tin​c\u200Bluded\ufeff"
    assert strip_control_characters(unnormalised_string) == "A string with tabs\tincluded"
    assert normalise_text(unnormalised_string) == "A string with tabs included"
