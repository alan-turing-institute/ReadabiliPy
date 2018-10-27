# ReadabiliPy

A Node and filesystem dependent Python wrapper for Mozilla's [Readability.js](https://github.com/mozilla/readability) Node.js package.

This package also augments the output of Readability.js to also return a list of plain text representations of article paragraphs.

## Package contents
- `Readability.js` folder
  - `Readability.js`: Taken unaltered from commit [3be1aaa  ](https://github.com/mozilla/readability/tree/3be1aaa01c078c25b67ed8dfd1c9aa8f9963490b) of Mozilla's [Readability.js](https://github.com/mozilla/readability) Node.js package.
- `ExtractArticle.js`: A Node.js script that reads a file containing a HTML snippet (does not have to be a full document), parses it using [jsdom](https://github.com/jsdom/jsdom), attempts to extract an article using `Readability.parse()` and writes the output to a JSON file.
  - Usage: `node ExtractArticle.js - i <input_file> -o <output_file>`


## Installation
1. [Install Node.js](https://nodejs.org/en/download/)
2. Install the node part of this package by running `npm install`.