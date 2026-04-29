import ssl
import httpx
import aiohttp
import urllib3
import requests
from httpx import AsyncClient
from aiohttp import TCPConnector
from urllib3 import PoolManager
from ssl import CERT_NONE, _create_unverified_context


httpx.get("https://api.example.com", verify=False)
httpx.Client(verify=False)

requests_session = requests.Session()
requests_session.verify = False

async_client = AsyncClient(verify=False)
connector = aiohttp.TCPConnector(ssl=False)
session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False))

pool = urllib3.PoolManager(cert_reqs="CERT_NONE")
proxy = PoolManager(cert_reqs=CERT_NONE, assert_hostname=False)

context = ssl._create_unverified_context()
another_context = _create_unverified_context()
ssl._create_default_https_context = ssl._create_unverified_context
context.verify_mode = ssl.CERT_NONE
context.check_hostname = False

async def fetch(session):
    return await session.get("https://api.example.com", ssl=False)


def make_connector():
    return TCPConnector(ssl=False)
