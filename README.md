# ReadabiliPy

[![Coverage Status](https://coveralls.io/repos/github/alan-turing-institute/ReadabiliPy/badge.svg?branch=master)](https://coveralls.io/github/alan-turing-institute/ReadabiliPy?branch=master)

`ReadabiliPy` contains a Python wrapper for Mozilla's [Readability.js](https://github.com/mozilla/readability) Node.js package, as well as article extraction routines written in pure Python.

This package augments the output of `Readability.js` to also return a list of plain text representations of article paragraphs.

`ReadabiliPy` comes with a handy command line application: ``readabilipy``.

## Installation

To use the `Readability.js` wrapper you need to have a working [Node.js](https://nodejs.org/en/download/) installation of version 14 or higher.
Make sure to install Node.js before installing this package, as this ensures Readability.js will be installed.
If you only want to use the Python-based article extraction, you **do not need** to install Node.js.

`ReadabiliPy` can be installed simply from PyPI:

```
$ pip install readabilipy
```

Note that to update to a new version of `Readability.js` you can simply reinstall `ReadabiliPy`.

## Usage

`ReadabiliPy` can be used either as a command line application or as a Python library.

### Command line application

The ``readabilipy`` command line application can be used to extract an article from an HTML source file.

For example, if you have the article saved as ``input.html`` in the current directory then you can run:

```
$ readabilipy -i ./input.html -o article.json
```

The extracted article can then be found in the ``article.json`` file. By default ReadabiliPy will use the Readability.js functionality to extract the article, provided this is available. If instead you'd like to use the Python-based extraction, run:

```
$ readabilipy -p -i ./input.html -o article.json
```

The complete help text of the command line application is as follows:

```
$ readabilipy -h
usage: readabilipy [-h] -i INPUT_FILE -o OUTPUT_FILE [-c] [-n] [-p] [-V]

Extract article data from a HTML file using either Mozilla's Readability.js
package or a simplified python-only alternative.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        Path to input file containing HTML.
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        Path to file to output the article data to as JSON.
  -c, --content-digests
                        Add a 'data-content-digest' attribute containing a
                        SHA256-based digest of the element's contents to each
                        HTML element in the plain_content output.
  -n, --node-indexes    Add a 'data-node-index' attribute containing a
                        hierarchical representation of the element's position
                        in the HTML structure each HTML element in the
                        plain_content output.
  -p, --use-python-parser
                        Use the pure-python 'plain_html' parser included in
                        this project rather than Mozilla's Readability.js.
  -V, --version         Show version and exit
```

## Library

ReadabiliPy can also be used as a Python package.
The main routine is called ``simple_json_from_html_string`` and expects the HTML article as a string.
Here is an example of extracting an article after downloading the page using [requests](https://requests.readthedocs.io/en/master/):

```python
>>> import requests
>>> from readabilipy import simple_json_from_html_string
>>> req = requests.get('https://en.wikipedia.org/wiki/Readability')
>>> article = simple_json_from_html_string(req.text, use_readability=True)
```

Note that you need to use the flag ``use_readability=True`` to use Readability.js, otherwise the Python-based extraction is used.

The ``simple_json_from_html_string`` function returns a dictionary with the following fields:

 - `title`: The article title
 - `byline`: Author information
 - `content`: A simplified HTML representation of the article, with all article text contained in paragraph elements.
 - `plain_content`: A "plain" version of the simplified `Readability.js` article HTML present in the `content` field. This attempts to retain only the plain text content of the article, while preserving the HTML structure.
 - `plain_text`: A list containing plain text representations of each paragraph (`<p>`) or list (`<ol>` or `<ul>`) present in the simplified `Readability.js` article HTML in the `content` field. Each paragraph or list is represented as a single string. List strings look like `"* item 1, * item 2, * item 3,"` for both ordered and unordered lists (note the trailing `,`).

Note further that:

- All fields are guaranteed to be present. If individual fields are missing from the output of `Readability.js`, the value of these fields will be `None`. If no article data is returned by `Readability.js`, the value of all fields will be `None`.
- All text in the `plain_content` and `plain_text` fields is encoded as unicode normalised using the "NFKC" normal form. This normal form is used to try and ensure as much as possible that things that appear visually the same are encoded with the same unicode representation (the K part) and characters are represented as a single composite character where possible (the C part).
- An optional `content_digests` flag can be passed to the Python wrapper. When this is set to `True`, each HTML element in the `plain_content` field has a `data-content-digest` attribute, which holds the SHA-256 hash of its plain text content. For "leaf" nodes (containing only plain text in the output), this is the SHA-256 hash of their plain text content. For nodes containing other nodes, this is the SHA-256 hash of the concatenated SHA-256 hashes of their child nodes.
- An optional `node_indexes` flag can be passed to the Python wrapper. When this is set to `True`, each HTML element in the `plain_content` field has a `data-node-indexes` attribute, which holds a hierarchical index describing the location of element within the `plain_content` HTML structure.
- An optional `use_readability` flag can be passed to the Python wrapper. When this is set to `True`, Mozilla's `Readability.js` will be used as the parser. If it is set to `False` then the pure-python parser in `plain_html.py` will be used instead.

The second top-level function exported by ReadabiliPy is ``simple_tree_from_html_string``. This returns a cleaned, parsed HTML tree of the article as a [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) object.

## Notes

License: MIT License, see the `LICENSE` file.

Copyright (c) 2018, The Alan Turing Institute

If you encounter any issues or have any suggestions for improvement, please open an issue [on Github](https://github.com/alan-turing-institute/ReadabiliPy).
You're helping to make this project better for everyone!
