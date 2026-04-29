from flask import request
import re
import regex as regex_lib
import sys
from re import compile as regex_compile
from re import search as regex_search


def compile_request_pattern():
    pattern = request.args["pattern"]
    return re.compile(pattern)


def search_with_request_pattern(body):
    query = request.args.get("q", "")
    return re.search(query, body)


def fstring_pattern_from_form(body):
    term = request.form["term"]
    pattern = f".*({term})+.*"
    return re.findall(pattern, body)


def imported_regex_alias(body):
    pattern = input("regex: ")
    return regex_search(pattern, body)


def argv_regex_compile():
    return regex_compile(sys.argv[1])


def third_party_regex_module(body):
    pattern = request.json["pattern"]
    return regex_lib.compile(pattern).search(body)


def pandas_string_regex(series):
    pattern = request.args["filter"]
    return series.str.contains(pattern)
