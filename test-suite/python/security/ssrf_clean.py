from urllib.parse import urlparse
from urllib.request import urlopen

import httpx
import requests
from flask import request

ALLOWED_HOSTS = {"api.example.com", "images.example.com"}


def is_allowed_url(target: str | None) -> bool:
    if not target:
        return False
    parsed = urlparse(target)
    return parsed.scheme == "https" and parsed.hostname in ALLOWED_HOSTS


def validate_outbound_url(target: str | None) -> str:
    if not is_allowed_url(target):
        raise ValueError("untrusted outbound target")
    return target


def validate_fetch_url(target: str | None) -> str:
    return validate_outbound_url(target)


def flask_proxy():
    target = request.args.get("url")
    if not is_allowed_url(target):
        raise ValueError("blocked")
    return requests.get(target, timeout=3).text


def helper_proxy():
    target = validate_outbound_url(request.args.get("url"))
    return httpx.get(target, timeout=3).text


async def async_helper_proxy():
    target = validate_outbound_url(request.args.get("image"))
    async with httpx.AsyncClient(timeout=3) as client:
        return await client.get(target)


def event_proxy(event):
    return urlopen(validate_fetch_url(event["queryStringParameters"]["feed"])).read()


def constant_url_fetch():
    return requests.get("https://api.example.com/status", timeout=3).json()
