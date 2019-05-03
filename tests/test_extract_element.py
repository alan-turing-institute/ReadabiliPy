from collections import defaultdict
from ..readabilipy.extractors.extract_element import extract_element
from ..readabilipy.extractors.extract_element import get_element_candidates


def test_get_element_candidates():

    xpaths = [
        ('//h1[@class="entry-title"]//text()', 4),
        ('//h1[@itemprop="headline"]//text()', 3),
        ('//h1[@class="post__title"]//text()', 2),
    ]

    html = """
            <h1 class="entry-title">Title 1</h>
            <p></p>
            <h1 itemprop="headline">Title 2</h>
            <p></p>
            <h1 class="post__title">Title 2</h>
    """

    expected_output_1 = defaultdict(int)
    expected_output_1['Title 1'] = 4
    expected_output_1['Title 2'] = 5

    expected_output_2 = defaultdict(int)
    expected_output_2['Title 1'] = 4
    expected_output_2['Title 2'] = 3

    assert get_element_candidates(html, xpaths, score_lower_limit=0) == expected_output_1
    assert get_element_candidates(html, xpaths, score_lower_limit=3) == expected_output_2


def test_extract_element():

    xpaths = [
        ('//h1[@class="entry-title"]//text()', 4),
        ('//h1[@itemprop="headline"]//text()', 3),
        ('//h1[@class="post__title"]//text()', -1),
    ]

    html = """
            <h1 class="entry-title">Title 1</h>
            <p></p>
            <h1 itemprop="headline">Title 2</h>
            <p></p>
            <h1 class="post__title">Title 2</h>
    """

    html_2 = """
            <h1 class="post__title">Title 2</h>
    """

    expected_output_1 = defaultdict(int)
    expected_output_1['Title 1'] = 4
    expected_output_1['Title 2'] = 3

    expected_output_2 = defaultdict(int)
    expected_output_2['Title 2'] = -1

    expected_output_3 = defaultdict(int)
    expected_output_3['Title 1'] = 7
    expected_output_3['Title 2'] = 3

    assert extract_element(html, xpaths) == expected_output_1
    assert extract_element(html_2, xpaths) == expected_output_2
    assert extract_element(html, xpaths, process_dict_fn=process_dict) == expected_output_3


def process_dict(d):
    d['Title 1'] = 7
    return d
