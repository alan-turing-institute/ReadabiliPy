from .extract_element import extract_element


def extract_title(html):
    """Return the article title from the article HTML"""

    # List of dictionaries for HTML tags that could contain a title
    extraction_paths = [
        {
            "paths": [["meta"]],
            "attrs": [{"property": "og:title"}, {"itemprop": "headline"}, {"name": "fb_title"}, {"name": "sailthru.author"}, {"name": "dcterms.title"}, {"name": "title"}],
            "element": "content"
        },
        {
            "paths": [["header", "h1"]],  # two-level HTML tag (header/h1)
            "attrs": [None],  # note: attributes are for the bottom level tag in path (h1 here), where None, any element matching the path will be extracted
            "element": "text"
        },
        {
            "paths": [["h1"], ["h2"]],  # multiple top level HTML tags
            "attrs": [{"class": "title"}, {"class": "entry-title"}, {"itemprop": "headline"}, {"class": "post__byline-name-hyphenated"}],
            "element": "text"
        }

    ]

    return extract_element(html, extraction_paths)
