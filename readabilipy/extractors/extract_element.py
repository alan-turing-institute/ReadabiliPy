from bs4 import BeautifulSoup
import re
from ..text_manipulation import normalise_whitespace


def extract_element(html, extraction_paths):
    """Return the relevant element (title, date or byline) from article HTML"""

    # Convert the HTML into a Soup parse tree
    soup = BeautifulSoup(html, "html5lib")

    element = None
    for tag_dict in extraction_paths:

        # Overwrite the element var if not already found
        if element is None:

            for path in tag_dict["paths"]:

                if element is None:

                    for attr_set in tag_dict["attrs"]:

                        if len(path) > 1:
                            # Call find() for each element in the soup from path
                            # Only for the lowest level element do we filter by attribute
                            soup_tag = soup.find(path[0])
                            i = 1
                            soup_tags = []
                            for level in path[1:]:
                                i += 1
                                if soup_tag:
                                    if i == len(path):
                                        soup_tags.append(soup_tag.find(path, attr_set))
                                    else:
                                        soup_tags.append(soup_tag.find(path))
                        else:
                            soup_tags = soup.find_all(path[0], attr_set)

                        # Handle the element being text in the HTML or an attr (e.g. content)
                        # If soup_tag was not found, element does not get set
                        goToNextTag = True
                        for soup_tag in soup_tags:
                            if goToNextTag:
                                if tag_dict["element"] == "text":
                                    if soup_tag and soup_tag.text:
                                        element = soup_tag.text
                                        goToNextTag = False
                                else:
                                    if soup_tag and soup_tag.has_attr(tag_dict["element"]):
                                        element = soup_tag[tag_dict["element"]]
                                        goToNextTag = False

    # Remove unwanted whitespace from the element
    if element:
        element = normalise_whitespace(element)

    return element
