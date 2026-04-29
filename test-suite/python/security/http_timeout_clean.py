from aiohttp import ClientSession, ClientTimeout
from urllib.request import urlopen
from urllib3 import PoolManager

import aiohttp
import httpx
import requests
import urllib3
from requests import get as requests_get


def requests_direct():
    return requests.get("https://api.example.com/data", timeout=3).json()


def requests_alias():
    return requests_get("https://api.example.com/data", timeout=(2, 10)).json()


def requests_session():
    session = requests.Session()
    return session.post("https://api.example.com/update", json={"ok": True}, timeout=5)


def httpx_direct():
    return httpx.post("https://api.example.com/update", json={"ok": True}, timeout=5)


def httpx_client():
    client = httpx.Client(timeout=5)
    return client.get("https://api.example.com/data")


async def aiohttp_session():
    timeout = aiohttp.ClientTimeout(total=5)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        return await session.get("https://api.example.com/data")


async def aiohttp_direct_import():
    async with ClientSession(timeout=ClientTimeout(total=5)) as session:
        return await session.post("https://api.example.com/update")


def urllib_urlopen():
    return urlopen("https://api.example.com/feed", timeout=5).read()


def urllib3_pool():
    pool = PoolManager(timeout=3.0)
    return pool.request("GET", "https://api.example.com/data")


def urllib3_module_pool():
    pool = urllib3.PoolManager(timeout=urllib3.Timeout(connect=2.0, read=5.0))
    return pool.urlopen("GET", "https://api.example.com/data")
