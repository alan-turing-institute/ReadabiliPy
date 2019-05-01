from ..readabilipy.extractors.extract_date import extract_date
from ..readabilipy.extractors.extract_date import standardise_datetime_format


def test_extract_date():
    htmls_with_expected = [
        ("""<meta name="Last-Modified" content="2018-12-21 06:30:21" />""", "2018-12-21T06:30:21"),
        ("""<p itemprop="datePublished">12/21/2018</p>""", "2018-12-21T00:00:00"),
        ("""<h1>No dates here</h1>""", None),
        ("""<meta property="article:published_time" content="2018-10-09T01:03:32" />""", "2018-10-09T01:03:32"),
        ("""<meta property="article:published_time" content="2018-12-13T21:02:01+00:00" />""", "2018-12-13T21:02:01"),
        ("""<meta property="article:published_time" content="2019-01-30 09:39:19 -0500" />""", "2019-01-30T09:39:19"),
        ("""<div class="publish-date"> Published 11:32 AM EST Feb 19, 2019 </div>""", "2019-02-19T11:32:00"),
        ("""<meta name="published_time_telegram" content="2019-01-25T15:16:00+00:00" />""", "2019-01-25T15:16:00"),
        ("""<p class="text-muted">Posted Friday, October 19, 2018</p>""", "2018-10-19T00:00:00"),
        ("""<div class="text"><p>2019-01-25T15:16:00+00:00</p></div>""", "2019-01-25T15:16:00"),
        ("""<span class="timestamp " data-localize-time data-epoch-time="1545342875000" data-time-zone="-0800" data-time-format="%A %B %d, %Y">Thursday December 20, 2018</span>""", "2018-12-20T00:00:00"),
        ("""<time style="text-transform:uppercase">8:16 AM 01/31/2019 | Politics</time>""", "2019-01-31T08:16:00"),
        ("""<span class="article-element__meta-item">Jun 01 2017 posted to <a href="/d/politics" title="Politics" class="article-element__meta-link">Politics</a></span>""", "2017-06-01T00:00:00"),
        ("""
            <div class="article-byline">By
                <span itemprop="author creator" itemtype="http://schema.org/Person" itemid="/by/michael-gryboski">
                    <a class="reporter" href="/by/michael-gryboski">
                        <span itemprop="name">Michael Gryboski</span>
                    </a>
                </span>
                , Christian Post Reporter
                <time class="visually-hidden"> | Monday, January 28, 2019</time>
            </div>
        """,
            "2019-01-28T00:00:00"),
        ("""<html><!-- By  - 08/01/10 --></html>""", "2010-01-08T00:00:00"),
    ]

    for html, expected_output in htmls_with_expected:
        output = extract_date(html)
        assert output == expected_output


def test_standardise_datetime_format():
    dates_with_expected = [
        ("2019-01-30 09:39:19 -0500", "2019-01-30T09:39:19"),
        ("2018-12-13T21:02:01+05:00", "2018-12-13T21:02:01"),
        ("Posted Friday, October 19, 2018", "2018-10-19T00:00:00"),
        (" Published 11:32 AM EST Feb 19, 2019", "2019-02-19T11:32:00"),
        ("Jun 01 2017 posted to Politics", "2017-06-01T00:00:00"),
        ("8:16 AM 01/31/2019 | Politics", "2019-01-31T08:16:00"),
    ]

    for date, expected_output in dates_with_expected:
        output = standardise_datetime_format(date)
        assert output == expected_output


def test_extract_datetime_iso8601_keep_timezone_keep():
    datetime_string = '2014-10-24T17:32:46+12:00'
    iso_string = standardise_datetime_format(datetime_string, ignoretz=False)
    expected_iso_string = '2014-10-24T17:32:46+12:00'

    assert iso_string == expected_iso_string


def test_extract_datetime_iso8601_drop_timezone():
    datetime_string = '2014-10-24T17:32:46+12:00'
    iso_string = standardise_datetime_format(datetime_string)
    expected_iso_string = '2014-10-24T17:32:46'

    assert iso_string == expected_iso_string


def test_extract_datetime_uk_format_without_timezone():
    datetime_string = '01/03/05'
    format_string = 'DD/MM/YY'
    iso_string = standardise_datetime_format(datetime_string, format=format_string)
    expected_iso_string = '2005-03-01T00:00:00'

    assert iso_string == expected_iso_string


def test_extract_datetime_us_format_without_timezone():
    datetime_string = '03/01/05'
    format_string = 'MM/DD/YY'
    iso_string = standardise_datetime_format(datetime_string)
    expected_iso_string = '2005-03-01T00:00:00'

    assert iso_string == expected_iso_string


def test_extract_datetime_byline_mmddyy_with_mmddyy_format():
    datetime_string = 'CHQ Staff | 10/17/18'
    format_string = 'MM/DD/YY'
    iso_string = standardise_datetime_format(datetime_string)
    expected_iso_string = '2018-10-17T00:00:00'

    assert iso_string == expected_iso_string


def test_extract_datetime_byline_mmddyyyy_with_mmddyy_format():
    datetime_string = 'CHQ Staff | 10/17/2018'
    format_string = 'MM/DD/YY'
    iso_string = standardise_datetime_format(datetime_string)
    expected_iso_string = '2018-10-17T00:00:00'

    assert iso_string == expected_iso_string


def test_extract_datetime_byline_mdyy_with_mdyy_format():
    datetime_string = 'CHQ Staff | 1/7/18'
    format_string = 'M/D/YY'
    iso_string = standardise_datetime_format(datetime_string)
    expected_iso_string = '2018-01-07T00:00:00'

    assert iso_string == expected_iso_string


def test_extract_datetime_byline_0m0dyy_with_mdyy_format():
    datetime_string = 'CHQ Staff | 01/07/18'
    format_string = 'M/D/YY'
    iso_string = standardise_datetime_format(datetime_string)
    expected_iso_string = '2018-01-07T00:00:00'

    assert iso_string == expected_iso_string


def test_extract_datetime_byline_mmddyy_with_mdyy_format():
    datetime_string = 'CHQ Staff | 12/17/18'
    format_string = 'M/D/YY'
    iso_string = standardise_datetime_format(datetime_string)
    expected_iso_string = '2018-12-17T00:00:00'

    assert iso_string == expected_iso_string
