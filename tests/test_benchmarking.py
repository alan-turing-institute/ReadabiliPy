import os
from ..readabilipy.json_parser import parse_to_json
from ..readabilipy.extractors.extract_title import extract_title
from ..readabilipy.extractors.extract_date import extract_date

test_filepath = os.path.join(os.path.dirname(__file__), "data", "benchmarkinghuge.html")
with open(test_filepath) as h:
    html = h.read()

def test_benchmark_parse_to_json(benchmark):

    benchmark(parse_to_json, html=html)

def test_benchmark_extract_title(benchmark):

    benchmark(extract_title, html=html)

def test_benchmark_extract_date(benchmark):

    benchmark(extract_date, html=html)
