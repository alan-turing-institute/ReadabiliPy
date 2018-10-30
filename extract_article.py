import argparse
import json
import readability


def main():
    parser = argparse.ArgumentParser(
        description="Extract article data from a HTML file using Mozilla's Readability.js package.")
    parser.add_argument('-i', '--input-file',
                        help='Path to input file containing HTML.')
    parser.add_argument('-o', '--output-file',
                        help='Path to file to output the article data to as JSON.')

    args = parser.parse_args()

    with open(args.input_file) as h:
        html = h.read()

    article = readability.parse(html)

    with open(args.output_file, "w") as j:
        json.dump(article, j, ensure_ascii=False)


if __name__ == '__main__':
    main()