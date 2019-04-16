from .extract_element import extract_element
import re
from dateutil import parser


def extract_date(html):
    """Return the article date from the article HTML"""

    # List of xpaths for HTML tags that could contain a date
    # Tuple scores reflect confidence in these xpaths and the preference used for extraction
    xpaths = [
        ('//meta[@property="article:published_time"]/@content', 24),  # Unlike with title, makes sense to have extremely high confidence in popular date tags
        ('//meta[@property="article:published"]/@content', 20),
        ('//meta[@name="Last-Modified"]/@content', 1),
        ('//meta[@name="dcterms.created"]/@content', 1),
        ('//meta[@name="published"]/@content', 5),
        ('//meta[@name="published_time_telegram"]/@content', 1),
        ('//meta[@property="og:article:published_time"]/@content', 1),
        ('//meta[@property="og:pubdate"]/@content', 1),
        ('//meta[contains(concat(" ", normalize-space(@property), " "), " article:published_time ")]/@content', 1),
        ('//meta[@itemprop="datePublished"]/@content', 2),
        ('//time[contains(@class, "entry-date")]/@datetime', 3),
        ('//time[@class="post-entry-time"]/@datetime', 1),
        ('//time[@itemprop="datePublished"]/@datetime', 3),
        ('//time[@class="post-date updated"]/@datetime', 1),
        ('//time[@class="post__date"]/@datetime', 1),
        ('//time/@datetime', 1),
        ('//time[@class="post__date"]/@content', 1),
        ('//time/text()', 1),
        ('//div[@class="article-heading-author-name"]//time[@class="timeagofunction"]/@datetime', 1),
        ('//div[@class="keyvals"]/@data-content_published_date', 1),
        ('//div[@class="article-byline"]/time[@class="visually-hidden"]/text()', 1),
        ('//div/time/@datetime', 1),
        ('//div[@class="subarticle"]/p/text()', -1),
        ('//div[@class="text"]/p/text()', -1),
        ('//div[@class="publish-date"]/text()', 1),
        ('//footer[@class="byline"]/time/@datetime', 1),
        ('//span[@class="timestamp "]/text()', 1),
        ('//span[@class="article-element__meta-item"]/text()', 1),
        ('//span[@class="date published time"]/@title', 1),
        ('//span[@class="updated"]/text()', 1),
        ('//span[@class="entry-date"]/text()', 1),
        ('//p[@itemprop="datePublished"]/text()', 1),
        ('//p[@class="entry-byline"]//time[@class="entry-date"]/@datetime', 1),
        ('//article[contains(@id, "post")]//time[@class="entry-date published"]/@datetime', 25),
        ('substring-after(//*[comment()[contains(., "By")]]/comment(), "-")', 1),
        ('substring-after(//p[@class="text-muted"]/text(), ",")', 1)
    ]

    # Get the date
    date_string = extract_element(html, xpaths)
    if date_string:
        for bad_string in ["Published", "posted to", " | Politics", "|"]:
            date_string = date_string.replace(bad_string, "")
        try:
            return parser.parse(date_string, ignoretz=True).isoformat()
        except Exception:
            return None
    return None
