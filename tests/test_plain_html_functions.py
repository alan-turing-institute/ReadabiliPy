"""Tests for plain_html functions."""
from bs4 import BeautifulSoup
from ..readabilipy import plain_html, text_manipulation


def test_remove_metadata():
    html = """
        <!DOCTYPE html>
        <html>
        <head></head>
        <body>
        <!-- Comment here -->
        </body>
        </html>
    """
    soup = BeautifulSoup(html, "html5lib")
    plain_html.remove_metadata(soup)
    assert "<!-- Comment here -->" not in str(soup)


def test_remove_blacklist():
    html = """
        <html>
        <body>
            <button type="button">Click Me!</button>
            <p>Hello</p>
        <body>
        </html>
    """
    soup = BeautifulSoup(html, "html5lib")
    plain_html.remove_blacklist(soup)
    assert "button" not in str(soup)


def test_remove_cdata():
    """Test all possible methods of CData inclusion. Note that in the final
    example the '//' prefixes have no effect (since we are not in a <script>)
    tag and so we expect that the first will be displayed (tested in Chrome and
    Safari)."""
    html = """
        <div>
            <p>Some text <![CDATA[Text inside two tags]]></p>
            <![CDATA[Text inside one tag]]>
        </div>
        <![CDATA[Text outside tags]]>
        <script type="text/javascript">
            //<![CDATA[
            document.write("<");
            //]]>
        </script>
        //<![CDATA[
            invalid CDATA block
        //]]>
    """.strip()
    parsed_html = str(plain_html.parse_to_tree(html))
    expected_output = "<div><div><p>Some text</p></div><p>//</p></div>"
    assert text_manipulation.simplify_html(parsed_html) == expected_output


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
                <h2 class="title">Example title</h2>
                <p>Hello world</p>
            <body>
            </html>
        """
    ]
    addicting_info_htmls = [
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
        """
    ]
    expected_output = "Example title"
    for html in htmls:
        output = plain_html.extract_title(html)
        assert output == expected_output
    expected_output = "Trump Denies Charitable Donation He Promised If Elizabeth Warren Releases DNA Results And It’s On Video"
    for html in addicting_info_htmls:
        output = plain_html.extract_title(html)
        assert output == expected_output

def test_extract_date():
    htmls = [
        """
            <meta name="Last-Modified" content="2018-12-21T06:30:21" />
        """,
        """
            <time>2018-12-21T06:30:22</time>
            <time datetime="2018-12-21T06:30:21"></time>
        """
    ]
    expected_output = "2018-12-21T06:30:21"
    for html in htmls:
        output = plain_html.extract_date(html)
        assert output == expected_output
