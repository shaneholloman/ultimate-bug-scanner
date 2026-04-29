from aiohttp import ClientSession
from urllib.request import urlopen
from urllib3 import PoolManager

import aiohttp
import httpx
import requests
import urllib3
from requests import get as requests_get


def requests_direct():
    return requests.get("https://api.example.com/data").json()


def requests_alias():
    return requests_get("https://api.example.com/data").json()


def requests_session():
    session = requests.Session()
    return session.post("https://api.example.com/update", json={"ok": True})


def httpx_direct():
    return httpx.post("https://api.example.com/update", json={"ok": True})


def httpx_client():
    client = httpx.Client()
    return client.get("https://api.example.com/data")


async def aiohttp_session():
    async with aiohttp.ClientSession() as session:
        return await session.get("https://api.example.com/data")


async def aiohttp_direct_import():
    async with ClientSession() as session:
        return await session.post("https://api.example.com/update")


def urllib_urlopen():
    return urlopen("https://api.example.com/feed").read()


def urllib3_pool():
    pool = PoolManager()
    return pool.request("GET", "https://api.example.com/data")


def urllib3_module_pool():
    pool = urllib3.PoolManager()
    return pool.urlopen("GET", "https://api.example.com/data")
