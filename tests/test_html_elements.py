from ReadabiliPy import readability
from pytest import mark

def check_html_output(test_fragment, expected_output = None):
    """Check that expected output is present when parsing HTML fragment."""
    article_json = readability.parse(test_fragment)
    if expected_output is None:
        expected_output = test_fragment
    # Check that each line of expected output is present
    print(article_json["plain_content"])
    for line in expected_output.split("\n"):
        assert(line.strip() in article_json["plain_content"])

def check_html_has_no_output(test_fragment):
    """Check that no output is present when parsing HTML fragment."""
    article_json = readability.parse(test_fragment)
    print(article_json["plain_content"])
    assert(article_json["plain_content"] is None)


# =============================
# All whitelisted HTML elements
# =============================
def test_html_whitelist_article():
    """An article is a self-contained composition in a document."""
    check_html_output("""
        <article>
        <header>
            <h2>Lorem ipsum dolor sit amet</h2>
            <p>Consectetur adipiscing elit</p>
        </header>
        <p>Vestibulum leo nulla, imperdiet a pellentesque a, ultrices aliquam massa</p>
        </article>
    """)


# def test_html_whitelist_aside():
#     """An aside is a tangentially related section, sometimes used for pull-quotes."""
#     check_html_output("""
#         <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean libero neque, ullamcorper quis tristique.</p>
#         <aside>
#             <p>Aenean libero neque</p>
#         </aside>    
#         <p>Pellentesque non sapien nec arcu facilisis gravida.</p>
#     """)


def test_html_whitelist_blockquote():
    """The blockquote element represents content that is quoted from another source."""
    check_html_output("""
        <p>He began his list of "lessons" with the following:</p>
        <blockquote>
            One should never assume that his side of the issue will be recognized, let alone that it will be conceded to
            have merits.
        </blockquote>
        <p>He continued with a number of similar points, ending with:</p>
        <blockquote>
            Finally, one should be prepared for the threat of breakdown in negotiations at any given moment and not be
            cowed by the possibility.
        </blockquote>
        <p>We shall now discuss these points...</p>
    """)


def test_html_whitelist_caption():
    """The caption element represents the title of the table that is its parent."""
    check_html_output("""
        <p>The caption provides context to the table.</p>
        <table>
            <caption>
                Table 1. This table shows the possible results of flipping two coins.
            </caption>
            <tbody>
                <tr>
                    <th></th>
                    <th>H</th>
                    <th>T</th>
                </tr>
                <tr>
                    <th>H</th>
                    <td>HH</td>
                    <td>TH</td>
                </tr>
                <tr>
                    <th>T</th>
                    <td>HT</td>
                    <td>TT</td>
                </tr>
            </tbody>
        </table>
    """)


def test_html_whitelist_colgroup():
    """The colgroup element groups one or more col elements inside its parent table."""
    check_html_output("""
        <table>
        <colgroup>
            <col span="2" style="background-color:red"/>
            <col style="background-color:yellow"/>
        </colgroup>
        <tr>
            <th>ISBN</th>
            <th>Title</th>
            <th>Price</th>
        </tr>
        </table>
    """,
    """
        <colgroup>
            <col span="2"/>
            <col/>
        </colgroup>
    """
    )

def test_html_whitelist_col():
    """The colgroup element groups one or more col elements inside its parent table."""
    check_html_output("""
        <table>
        <colgroup>
            <col span="2" style="background-color:red"/>
            <col style="background-color:yellow"/>
        </colgroup>
        <tr>
            <th>ISBN</th>
            <th>Title</th>
            <th>Price</th>
        </tr>
        </table>
    """,
    """
        <col span="2"/>
        <col/>
    """
    )

def test_html_whitelist_div():
    """The div element has no special meaning."""
    check_html_output("""
        <p>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean libero neque, ullamcorper quis tristique id,
            pretium dapibus turpis. 
        </p>
        <div lang="en-GB">
        <p>Here is an example of using div for stylistic reasons.</p>
        <p>It marks several paragraphs which are in a different language from the rest of the text.</p>
        </div>
        <p>Pellentesque non sapien nec arcu facilisis gravida.</p>
    """)


def test_html_whitelist_dl():
    """The dl element is a description list, within which dt is a term and dd is the description."""
    check_html_output("""
        <dl>
            <dt>Term 1</dt>
            <dd>Description 1</dd>
            <dt>Term 2</dt>
            <dd>Description 2</dd>
        </dl>
    """)


def test_html_whitelist_dd():
    """The dl element is a description list, within which dt is a term and dd is the description."""
    check_html_output("""
        <dl>
            <dt>Term 1</dt>
            <dd>Description 1</dd>
        </dl>
    """,
    "<dd>Description 1</dd>")


def test_html_whitelist_dt():
    """The dl element is a description list, within which dt is a term and dd is the description."""
    check_html_output("""
        <dl>
            <dt>Term 1</dt>
            <dd>Description 1</dd>
        </dl>
    """,
    "<dt>Term 1</dt>")


def test_html_whitelist_figure():
    """The figure element represents some self-contained flow content."""
    check_html_output("""
        <p>In <a href="#figref">this figure</a> we see some code.</p>
        <figure id="figref">
            <figcaption>Listing 1. Code description.</figcaption>
            <pre>
                <code>Some formatted code lives here</code>
            </pre>
        </figure>
        <p>Further details are given in this paragraph.</p>
    """,
    """
        <figure id="figref">
    """)


def test_html_whitelist_figcaption():
    """The figcaption element represents the caption of its parent figure."""
    check_html_output("""
        <p>In <a href="#figref">this figure</a> we see some code.</p>
        <figure id="figref">
            <figcaption>Listing 1. Code description.</figcaption>
            <pre>
                <code>Some formatted code lives here</code>
            </pre>
        </figure>
        <p>Further details are given in this paragraph.</p>
    """,
    """
        <figcaption>Listing 1. Code description.</figcaption>
    """)


# def test_html_whitelist_footer():
#     """The footer element represents a footer for its nearest ancestor section."""
#     check_html_output("""
#         <p>
#             A dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna
#             aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
#             consequat.
#         </p>
#         <footer>Text about author and date</footer>
#     """)


# def test_html_whitelist_h1():
#     """The h1 element is often used for titles."""
#     check_html_output("""
#         <h1>Title here</h1>
#         <p>Some text following.</p>
#     """)


def test_html_whitelist_h2_h3_h4_h5_h6():
    """hN elements represent headings for their sections in ranked order."""
    check_html_output("""
        <h2>Second level</h2>
        <h3>Third level</h3>
        <h2>Also second-level</h2>
        <h3>Third level</h3>
        <h4>Fourth level</h4>
        <h5>Fifth level</h5>
        <h6>Bottom level</h6>
        <h4>Also fourth-level</h4>
        <h5>Also fifth level</h5>
    """)


def test_html_whitelist_header():
    """The header element represents introductory content for its nearest ancestor section."""
    check_html_output("""
        <header>
            <p>Byline might live here for example.</p>
        </header>
        <p>
            A dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna
            aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
            consequat.
        </p>
    """)


def test_html_whitelist_li():
    """The li element defines an item in a list."""
    check_html_output("""
        <ul>
            <li>Item 1</li>
            <li>Item 2</li>
        </ul>
    """,
    """
        <li>Item 1</li>
        <li>Item 2</li>
    """)


def test_html_whitelist_main():
    """The main element contains content that is unique to the document in question."""
    check_html_output("""
       <header>The header</header>
       <main>
            <p>A paragraph</p>
            <p>And another one</p>
        </main>
        <footer>The footer</footer>
    """,
    """
       <main>
            <p>A paragraph</p>
            <p>And another one</p>
        </main>
    """)

def test_html_whitelist_ol():
    """The ol element defines an unordered list."""
    check_html_output("""
        <ol>
            <li>Item 1</li>
            <li>Item 2</li>
        </ol>
    """)

def test_html_whitelist_p():
    """The p element defines a paragraph."""
    check_html_output("""
        <p>Nulla venenatis nulla porta, vestibulum felis ac, faucibus urna.</p>
        <p>Praesent imperdiet nec justo at blandit. Morbi ultrices urna in elementum viverra. Proin condimentum lacus interdum lorem blandit vulputate.</p>
    """)

def test_html_whitelist_pre():
    """The pre element represents a block of preformatted text."""
    check_html_output("""
        <pre>
            Some preformatted   text lives  here
        </pre>
    """)    
    

def test_html_whitelist_section():
    """The section element represents a generic section of a document or application."""
    check_html_output("""
        <section class="chapter">
            <h3 class="chaptertitle">My First Chapter</h3>
            <p>This is the first of my chapters. It doesn’t say much.</p>
            <p>But it has two paragraphs!</p>
        </section>
    """,
    """    
        <section>
            <h3>My First Chapter</h3>
            <p>This is the first of my chapters. It doesn’t say much.</p>
            <p>But it has two paragraphs!</p>
        </section>
    """)    
    

# def test_html_whitelist_table():
#     """The table element represents data with more than one dimension."""
#     check_html_output("""
#         <table>
#         <tr>
#             <td>Table contents</td>
#         </tr>
#         </table>
#     """, 
#     "<table><tr><td>Content</td></tr></table>")


# def test_html_whitelist_tbody():
#     """The tbody element represents a block of rows inside its parent table."""
#     check_html_output("""
#         <table>
#         <tbody>
#             <td>Table body content</td>
#         </tbody>
#         </table>
#     """, 
#     "<tbody><td>Content</td></tbody>")


def test_html_whitelist_thead():
    """The thead element represents a block of rows that form the header of its parent table."""
    check_html_output("""
        <table>
        <thead>
            <tr>
                <th>Header</th>
            </tr>
        </thead>
        </table>
    """,
    "<thead><tr><th>Header</th></tr></thead>")


def test_html_whitelist_tfoot():
    """The tfoot element represents a block of rows that form the column summaries of its parent table."""
    check_html_output("""
        <table>
        <tfoot>
            <tr>
                <td>Sum of column</td>
            </tr>
        </tfoot>
        </table>
    """,
    "<tfoot><tr><td>Sum of column</td></tr></tfoot>")


# def test_html_whitelist_tr():
#     """The tr element represents a row in a table."""
#     check_html_output("""
#         <table>
#         <tr>
#             <td>Content</td>
#         </tr>
#         </table>
#     """,
#     "<tr><td>Content</td></tr>")


# def test_html_whitelist_td():
#     """The td element represents a cell in a table."""
#     check_html_output("""
#         <table>
#         <tr>
#             <td>Cell content</td>
#         </tr>
#         </table>
#     """,
#     "<td>Cell content</td>")


def test_html_whitelist_th():
    """The th element represents a header cell in a table."""
    check_html_output("""
        <table>
        <tr>
            <th>Header text</th>
        </tr>
        </table>
    """,
    "<th>Header text</th>")


def test_html_whitelist_ul():
    """The ul element defines an unordered list."""
    check_html_output("""
        <ul>
            <li>Item 1</li>
            <li>Item 2</li>
        </ul>
    """)


# =============================
# All blacklisted HTML elements
# =============================
# @mark.parametrize("element", ["button", "datalist", "fieldset", "form",
#                               "input", "label", "legend", "meter", "optgroup",
#                               "option", "output", "progress", "select",
#                               "textarea", "area", "img", "map", "picture",
#                               "source", "audio", "track", "video", "embed",
#                               "math", "object", "param", "svg", "details",
#                               "dialog", "summary", "canvas", "noscript",
#                               "script", "template", "data", "link", "time",
#                               "style", "nav", "br", "hr"]) 
@mark.parametrize("element", ["button", "fieldset", "form"])
def test_html_blacklist_element(element):
    check_html_has_no_output('<{0}>Lorem ipsum dolor sit amet</{0}>'.format(element))


def test_html_blacklist_datalist():
    """The datalist element represents a set of option elements."""
    check_html_has_no_output("""
        <datalist id=sexes>
            <option value="Female">
            <option value="Male">
        </datalist>
    """)


def test_html_blacklist_fieldset():
    """The fieldset element represents a set of form controls."""
    check_html_has_no_output("""
        <fieldset id=sexes>
            <option value="Female">
            <option value="Male">
        </fieldset>
    """)

# =========================
# All special HTML elements
# =========================
# def test_html_special_q():
#     """An article is a self-contained composition in a document."""
#     check_html_output("""
#         <p>Some text <q>this bit is quoted</q> and now back to normal</p>
#     """,
#     '<p>Some text "this bit is quoted" and now back to normal</p>')
