from bs4 import BeautifulSoup
from ..text_manipulation import normalise_whitespace


def extract_element(html, extraction_paths):
    """Return the relevant element (title, date or byline) from article HTML"""

    # Convert the HTML into a Soup parse tree
    soup = BeautifulSoup(html, "html5lib")

    elements = []
    for tag_dict in extraction_paths:

        for path in tag_dict["paths"]:

            for attr_set in tag_dict["attrs"]:

                if len(path) == 2:
                    # Call find_all() for each element in the soup from path
                    # Only for the lowest level element do we filter by attribute
                    soup_tags_level_one = soup.find_all(path[0])
                    soup_tags = []
                    for soup_tag in soup_tags_level_one:
                        soup_tags = soup_tags + soup_tag.find_all(path[1], attr_set)

                else:
                    soup_tags = soup.find_all(path[0], attr_set)

                # Handle the element being text in the HTML or an attr (e.g. content)
                for soup_tag in soup_tags:
                    if tag_dict["element"] == "text":
                        if soup_tag and soup_tag.text:
                            elements.append(normalise_whitespace(soup_tag.text))
                    else:
                        if soup_tag and soup_tag.has_attr(tag_dict["element"]):
                            elements.append(normalise_whitespace(soup_tag[tag_dict["element"]]))

    if len(elements) == 0:
        return None  # Return None when no extraction path elements in the HTML
    else:
        # Returns the most common element, but returns the first in the list by default when equally common
        if len(elements) == len(set(elements)):  # if all elements unique
            return elements[0]
        else:
            return max(set(elements), key=elements.count)
