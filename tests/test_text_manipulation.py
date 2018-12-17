from ReadabiliPy.text_manipulation import normalise_text

def test_all_whitespace_is_normalised_to_empty_string():
    tab_space_tab_space = "\t \t "
    assert normalise_text(tab_space_tab_space) == ""
