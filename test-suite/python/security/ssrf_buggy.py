from urllib.request import urlopen

import aiohttp
import httpx
import requests
from flask import request
from requests import Session as RequestsSession


def flask_proxy():
    target = request.args.get("url")
    return requests.get(target, timeout=3).text


def django_callback(request):
    return httpx.get(request.GET["callback"], timeout=3).text


async def starlette_preview(request):
    target = request.query_params.get("image")
    async with aiohttp.ClientSession() as session:
        return await session.get(target)


def urllib_proxy():
    return urlopen(request.values.get("feed")).read()


def aliased_requests_session(request):
    target = request.GET.get("next_hop")
    client = RequestsSession()
    return client.get(target, timeout=3).content
