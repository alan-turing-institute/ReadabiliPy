# ReadabiliPy

A Node and filesystem dependent Python wrapper for Mozilla's [Readability.js](https://github.com/mozilla/readability) Node.js package.

This package also augments the output of Readability.js to also return a list of plain text representations of article paragraphs.

## Package contents
- `Readability.js` folder
  - `Readability.js`: Taken unaltered from commit [3be1aaa  ](https://github.com/mozilla/readability/tree/3be1aaa01c078c25b67ed8dfd1c9aa8f9963490b) of Mozilla's [Readability.js](https://github.com/mozilla/readability) Node.js package.
- `ExtractArticle.js`: A Node.js script that reads a file containing a HTML snippet (does not have to be a full document), parses it using [jsdom](https://github.com/jsdom/jsdom), attempts to extract an article using `Readability.parse()` and writes the output to a JSON file.
  - Usage: `node ExtractArticle.js - i <input_file> -o <output_file>`
- A `readability.py` file containing the wrapper function `extract_article()`.
  - Usage:
  ```python
  from ReadabiliPy import readability

  article = readability.extract_article(html_string)
  ```
  - The function returns a dictionary with the following fields:
    - `title`: The article title
    - `byline`: Author information
    - `content`: A simplified HTML representation of the article, with all article text contained in paragraph elements.
    - `plain_content`: A list containing a plain text representation of each paragraph in the simplified article.
    - All fields are guaranteed to be present. If individual fields are missing from the output of Readability.js, the value of these fields will be `None`. If no article data is returned by Readability.js, the value of all fields will be `None`.

## Installation
1. [Install Node.js](https://nodejs.org/en/download/)
2. Install the node part of this package by running `npm install`.
3. Install the requirements for the Python part of this package by running `pip install -r requirements.txt`.

## Testing
1. Install `pytest` by running `pip install pytest`
