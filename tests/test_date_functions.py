from ..readabilipy.extractors.extract_date import extract_date
from ..readabilipy.extractors.extract_date import ensure_iso_date_format


def test_extract_date():
    htmls_with_expected = [
        ("""<h1>No dates here</h1>""", None),
        ("""<meta property="article:published_time" content="2018-10-09T01:03:32" />""", "2018-10-09T01:03:32"),
        ("""<meta property="article:modified_time" content="2018-12-13T21:02:01+00:00" />""", "2018-12-13T21:02:01"),
        ("""<meta property="article:published" content="2019-01-30T09:39:20-0500" />""", "2019-01-30T09:39:20"),
        ("""<meta property="og:updated_time" content="2019-01-30T09:39:21-0500" />""", "2019-01-30T09:39:21"),
        ("""<meta itemprop="dateModified" content="2019-01-30T09:39:22-0500" />""", "2019-01-30T09:39:22"),
        ("""<meta itemprop="datePublished" content="2019-01-30T09:39:23-0500" />""", "2019-01-30T09:39:23"),
        ("""<time datetime="2019-01-30T09:39:24-0500" />""", "2019-01-30T09:39:24"),
    ]

    for html, expected_output in htmls_with_expected:
        output = extract_date(html)
        assert output == expected_output


def test_ensure_iso_date_format_timezone_keep():
    datetime_string = '2014-10-24T17:32:46+12:00'
    iso_string = ensure_iso_date_format(datetime_string, ignoretz=False)
    expected_iso_string = '2014-10-24T17:32:46+12:00'

    assert iso_string == expected_iso_string


def test_ensure_iso_date_format_timezone_drop():
    datetime_string = '2014-10-24T17:32:46+12:00'
    iso_string = ensure_iso_date_format(datetime_string)
    expected_iso_string = '2014-10-24T17:32:46'

    assert iso_string == expected_iso_string


def test_ensure_iso_date_format_no_tz():
    datetime_string = '2014-10-24T17:32:46'
    iso_string = ensure_iso_date_format(datetime_string)
    expected_iso_string = '2014-10-24T17:32:46'

    assert iso_string == expected_iso_string


def test_ensure_iso_date_format_000Z_format():
    datetime_string = '2019-02-15T15:54:50.000Z'
    iso_string = ensure_iso_date_format(datetime_string)
    expected_iso_string = '2019-02-15T15:54:50'

    assert iso_string == expected_iso_string


def test_ensure_iso_date_format_hh_colon_mmZ_format():
    datetime_string = '2019-02-18T17:52:10Z'
    iso_string = ensure_iso_date_format(datetime_string)
    expected_iso_string = '2019-02-18T17:52:10'

    assert iso_string == expected_iso_string
    

def test_ensure_iso_date_format_non_iso_string():
    htmls_with_expected = [
        ("""Hello world""", None),
        ("""10/10/2019""", None),
    ]

    for html, expected_output in htmls_with_expected:
        output = ensure_iso_date_format(html)
        assert output == expected_output
