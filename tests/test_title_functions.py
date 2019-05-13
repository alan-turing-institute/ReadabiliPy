from ..readabilipy.extractors.extract_title import extract_title
from ..readabilipy.extractors.extract_title import combine_similar_titles


def test_extract_title():
    htmls_with_expected = [
        ("""
            <html>
            <head>
                <meta name="fb_title" content="Example title" />
            </head>
            <body>
                <p>Hello world</p>
            <body>
            </html>
        """, "Example title"),
        ("""
            <html>
            <head>
            </head>
            <body>
                <h2 class="title">Silly title</h2>
                <h1 class="title">Bad title</h1>
                <header><h1>Example title</h1></header>
                <p>Hello world</p>
            <body>
            </html>
        """, "Example title"),
        ("""
            <html>
            <head>
            </head>
            <body>
                <h2 itemprop="headline">Example title</h2>
                <header><h1>Incorrect title</h1></header>
                <p>Hello world</p>
            <body>
            </html>
        """, "Example title"),
        ("""
            <h1 class="entry-title">
                <a href="http://addictinginfo.com/2018/10/15/trump-denies-charitable-donation-he-promised-if-elizabeth-warren-releases-dna-results-and-its-on-video/"
                    title="Permalink to Trump Denies Charitable Donation He Promised If Elizabeth Warren Releases DNA Results And It&#8217;s On Video"
                    rel="bookmark">Trump Denies Charitable Donation He Promised If Elizabeth Warren Releases DNA Results And
                    It&#8217;s On Video</a>
            </h1>
        """, "Trump Denies Charitable Donation He Promised If Elizabeth Warren Releases DNA Results And It’s On Video"),
        ("""
            <meta property="og:title" content="Trump Denies Charitable Donation He Promised If Elizabeth Warren Releases DNA Results And It&#8217;s On Video" />
        """, "Trump Denies Charitable Donation He Promised If Elizabeth Warren Releases DNA Results And It’s On Video"),
        ("""<head><title>Test title</title></head>""", "Test title"),
        ("""<head><title><p>Test title</p></title></head>""", "Test title")
    ]

    for html, expected_output in htmls_with_expected:
        output = extract_title(html)
        assert output == expected_output


def test_title_shortening():

    htmls_with_expected = [
        ("""
            <h1 class="entry-title">Pamela Geller in Breitbart News: Dueling Billboards from CAIR, AFDI in Times Square</h1>
            <meta property="og:title" content="Pamela Geller in Breitbart News: Dueling Billboards from CAIR, AFDI in Times Square - Geller Report" />
        """, "Pamela Geller in Breitbart News: Dueling Billboards from CAIR, AFDI in Times Square"),
    ]

    for html, expected_output in htmls_with_expected:
        output = extract_title(html)
        assert output == expected_output


def test_combine_similar_titles():

    extracted_strings = {}
    extracted_strings['title 1'] = {'score': 1, 'xpaths': ['a']}
    extracted_strings['Title 1'] = {'score': 1, 'xpaths': ['b']}
    extracted_strings['Title 1 - Extended'] = {'score': 1, 'xpaths': ['c']}

    expected_output = {}
    expected_output['title 1'] = {'score': 1, 'xpaths': ['a']}
    expected_output['Title 1'] = {'score': 3, 'xpaths': ['a', 'b', 'c']}
    expected_output['Title 1 - Extended'] = {'score': 1, 'xpaths': ['c']}

    assert combine_similar_titles(extracted_strings) == expected_output
