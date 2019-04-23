from .extract_element import extract_element
from itertools import permutations


def extract_title(html):
    """Return the article title from the article HTML"""

    # List of xpaths for HTML tags that could contain a title
    # Tuple scores reflect confidence in these xpaths and the preference used for extraction
    xpaths = [
        ('//meta[@property="og:title"]/@content', 6),
        ('//meta[contains(@itemprop, "headline")]/@content', 2),
        ('//meta[@name="fb_title"]/@content', 1),
        ('//meta[@name="sailthru.title"]/@content', 1),
        ('//meta[@name="dcterms.title"]/@content', 1),
        ('//meta[@name="title"]/@content', 1),
        ('//header[@class="entry-header"]/h1[@class="entry-title"]//text()', 1),
        ('//header/h1//text()', 1),
        ('//h1[@class="title"]//text()', 1),
        ('//h1[@class="entry-title"]//text()', 3),
        ('//h1[@itemprop="headline"]//text()', 2),
        ('//h1[@class="post__title"]//text()', 1),
        ('//h2[@itemprop="headline"]//text()', 2),
        ('//div[@class="postarea"]/h2/a//text()', 1)
    ]

    return extract_element(html, xpaths, process_dict_fn=combine_similar_titles)


def combine_similar_titles(extracted_strings):
    """Take a dictionary with titles and scores and combine scores for titles where one is just a longer version the other, taking the shorter as key"""

    # Iterate through each possible pair of title keys, including both permutations of each pair
    for title_pair in permutations(extracted_strings, 2):
        if title_pair[0] in title_pair[1]:
            extracted_strings[title_pair[0]] += extracted_strings[title_pair[1]]  # combine scores
    return extracted_strings
