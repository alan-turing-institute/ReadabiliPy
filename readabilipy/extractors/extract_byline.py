from .extract_element import extract_element


def extract_byline(html):
    """Return the article byline from the article HTML"""

    # List of xpaths for HTML tags that could contain a byline
    # Tuple scores reflect confidence in these xpaths and the preference used for extraction
    xpaths = [
        ('//meta[@name="author"]/@content', 3),
        ('//meta[@name="parsely-author"]/@content', 1),
        ('//meta[@itemprop="author"]/@content', 3),
        ('//meta[@property="article:author"]/@content', 1),
        ('//meta[@property="author"]/@content', 2),
        ('//*[contains(@itemprop, "author")]//span[@itemprop="name"]/text()', 1),
        ('//a[@class="post__byline-name-hyphenated"]/text()', 1),
        ('//aside[@class="post-author"]/a[@rel="author"]/text()', 1),
        ('//div[@class="article-heading-author-name"]//a[@rel="author"]/text()', 1),
        ('//div[@class="article-byline"]/span[contains(@itemprop, "author")]//span[@itemprop="name"]/text()', 1),
        ('//div[@class="article-author"]/span[contains(@class, "article-author")]/a/text()', 1),
        ('//div[@class="author-byline"]/span/span/a/text()', 1),
        ('//div[@class="author-text"]/a[@class="bold author-name"]/text()', 1),
        ('//div[@class="byline"]/a/text()', 1),
        ('//div[@class="text"]/article/descendant::*/text()', 1),
        ('//div[@class="founders-cond f6 lh-none"]/text()', 1),
        ('//div[@class="vcard author"]//a/text()', 1),
        ('//div[@class="subarticle"]/p//strong/text()', 1),
        ('//div[contains(@class, "author-info")]/span[contains(@class, "author--name")]/text()', 1),
        ('//div[contains(@class, "author-byline")]/span[@class="author-name"]//a/text()', 1),
        ('//div[contains(@class, "wire-byline")]/span/text()', 1),
        ('//div[contains(@class, "author-list")]/span/text()', 1),
        ('//div[contains(@class, "author-name")]/a/text()', 1),
        ('//input[@name="tpContentAuthor"]/@value', 1),
        ('//span[@class="author"]/text()', 1),
        ('//span[@class="author vcard"]/span[contains(@class, "coauthors")]/a[@rel="author"]/text()', 1),
        ('//span[@class="author vcard"]/a/text()', 2),
        ('//span[@class="author vcard" and @itemprop="name"]/a/text()', 1),
        ('//span[@class="author vcard"]//text()', 1),
        ('//span[@class="author vcard"]/span/a/text()', 1),
        ('//span[@class="author"]/descendant::*/text()', 1),
        ('//span[@class="author-name vcard fn author"]/a/text()', 2),
        ('//span[@class="entry-meta-author author vcard"]//a/text()', 1),
        ('//span[@class="fl-post-author"]/a/text()', 1),
        ('//span[@class="post__byline__author"]//a/text()', 1),
        ('//span[contains(@class, "author-card__details__name")]/text()', 1),
        ('//span[contains(@itemprop, "author")]', 1),
        ('//span[contains(@class, "author vcard"  )]/span/text()', 1),
        ('//span[@itemprop="name"]/text()', 1),
        ('//span[@itemprop="name"]/a/text()', 1),
        ('//span[@itemprop="author"]/meta[@itemprop="name"]/@content', 3),
        ('//span[@itemprop="author"]/a/span[@itemprop="name"]/text()', 1),
        ('//span[@itemprop="author"]/span[@itemprop="name"]/text()', 1),
        ('//p[@itemprop="author"]/text()', 1),
        ('//p[@class="entry-byline"]/a/text()', 1),
        ('substring-before(substring-after(//script[contains(text(), "tq.byline")], "tq.byline = ''"), "'';")', 1),
        ('substring-after(//div[@id="sto_graphs"]/p[last()]/text(), "- ")', 1),
        ('substring-after(substring-before(//*[comment()[contains(., "By")]]/comment(), "-"), "By ")', 1),
        ('substring-before(//div[@class="author"]/text(), "|")', 1),
        ('substring-after(//div[@class="container"]/div[@class="row"]/div[@class="col-md-8"]/p[contains(text(), "Submitted")]/text(), "by ")', 1)
    ]

    author_names = extract_element(html, xpaths, return_all_unique=True)

    for name in author_names:
        if len(name.split()) > 3: #  Names shouldn't have more than 3 words
            author_names.remove(name)

    byline_string = ", ".join(author_names)

    return byline_string
