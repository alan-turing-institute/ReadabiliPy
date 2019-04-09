from ..readabilipy.extractors.extract_title import extract_title
from ..readabilipy.extractors.extract_date import extract_date


def test_extract_title():
    htmls = [
        """
            <html>
            <head>
                <meta name="fb_title" content="Example title" />
            </head>
            <body>
                <p>Hello world</p>
            <body>
            </html>
        """,
        """
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
        """,
        """
            <html>
            <head>
            </head>
            <body>
                <h2 itemprop="headline">Example title</h2>
                <header><h1>Incorrect title</h1></header>
                <p>Hello world</p>
            <body>
            </html>
        """,
        """
            <h1 class="entry-title">
                <a href="http://addictinginfo.com/2018/10/15/trump-denies-charitable-donation-he-promised-if-elizabeth-warren-releases-dna-results-and-its-on-video/"
                    title="Permalink to Trump Denies Charitable Donation He Promised If Elizabeth Warren Releases DNA Results And It&#8217;s On Video"
                    rel="bookmark">Trump Denies Charitable Donation He Promised If Elizabeth Warren Releases DNA Results And
                    It&#8217;s On Video</a>
            </h1>
        """,
        """
            <meta property="og:title" content="Trump Denies Charitable Donation He Promised If Elizabeth Warren Releases DNA Results And It&#8217;s On Video" />
        """,
        """
            <h1 class="entry-title">Pamela Geller in Breitbart News: Dueling Billboards from CAIR, AFDI in Times Square</h1>
            <meta property="og:title" content="Pamela Geller in Breitbart News: Dueling Billboards from CAIR, AFDI in Times Square - Geller Report" />
        """
    ]
    expected_outputs = ["Example title"] * 3
    expected_outputs.extend(["Trump Denies Charitable Donation He Promised If Elizabeth Warren Releases DNA Results And It’s On Video"] * 2)
    expected_outputs.append("Pamela Geller in Breitbart News: Dueling Billboards from CAIR, AFDI in Times Square")
    for html, expected_output in zip(htmls, expected_outputs):
        output = extract_title(html)
        assert output == expected_output


def test_extract_date():
    htmls = [
        """
            <meta name="Last-Modified" content="2018-12-21 06:30:21" />
        """,
        """
            <p itemprop="datePublished">12/21/2018</p>
        """,
        """
            <h1>No dates here</h1>
        """,
        """
            <meta property="article:published_time" content="2018-10-09T01:03:32" />
        """,
        """
            <meta property="article:published_time" content="2018-12-13T21:02:01+00:00" />
        """,
        """
            <meta property="article:published_time" content="2019-01-30 09:39:19 -0500" />
        """,
        """
            <div class="publish-date"> Published 11:32 AM EST Feb 19, 2019 </div>
        """,
        """
            <meta name="published_time_telegram" content="2019-01-25T15:16:00+00:00" />
        """
    ]
    expected_outputs = ["2018-12-21T06:30:21", "2018-12-21T00:00:00", None, "2018-10-09T01:03:32", "2018-12-13T21:02:01", "2019-01-30T09:39:19", "2019-02-19T11:32:00", "2019-01-25T15:16:00"]
    for html, expected_output in zip(htmls, expected_outputs):
        output = extract_date(html)
        assert output == expected_output
