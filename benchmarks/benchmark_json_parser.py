from ..readabilipy.json_parser import parse_to_json


def benchmark_parse_to_json():

    html = 

    return timeit.timeit('parse_to_json(html)', number = 5, setup='from __main__ import parse_to_json')
