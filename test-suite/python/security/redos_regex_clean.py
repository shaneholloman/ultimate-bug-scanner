from flask import request
import re


def fixed_pattern_search(body):
    return re.search(r"^[a-z0-9_-]{1,64}$", body)


def escaped_request_literal(body):
    term = request.args["term"]
    pattern = rf"^{re.escape(term)}$"
    return re.search(pattern, body)


def escaped_compile():
    needle = request.args.get("needle", "")
    return re.compile(re.escape(needle))


def allowlisted_pattern(name, body):
    patterns = {
        "slug": r"^[a-z0-9-]{1,80}$",
        "uuid": r"^[0-9a-f-]{36}$",
    }
    pattern = patterns.get(name)
    if pattern is None:
        raise ValueError("unsupported pattern")
    return re.fullmatch(pattern, body)


def pandas_literal_contains(series):
    needle = request.args["needle"]
    return series.str.contains(needle, regex=False)
