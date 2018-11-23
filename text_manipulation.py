"""Common text manipulation functions."""
import unicodedata
import regex

def normalise_unicode(text):
    """Normalise unicode such that things that are visually equivalent map to the same unicode string where possible."""
    normal_form = "NFKC"
    text = unicodedata.normalize(normal_form, text)
    return text


def normalise_whitespace(text):
    """Replace runs of whitespace characters with a single space as this is what happens when HTML text is displayed."""
    text = regex.sub(r"\s+", " ", text)
    # Remove leading and trailing whitespace
    text = text.strip()
    return text


def normalise_text(text):
    """Normalise unicode and whitespace."""
    # Normalise unicode first to try and standardise whitespace characters as much as possible before normalising them
    text = normalise_unicode(text)
    text = normalise_whitespace(text)
    return text

def simplify_html(text):
    """Simplify HTML by stripping whitespace."""
    # Normalise unicode first to try and standardise whitespace characters as much as possible before normalising them
    text = normalise_text(text)
    text = text.replace(" <", "<").replace("> ", ">")
    return text
