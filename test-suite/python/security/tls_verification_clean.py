import ssl
import httpx
import aiohttp
import urllib3
import requests
from aiohttp import TCPConnector
from urllib3 import PoolManager


httpx.get("https://api.example.com", verify=True)
httpx.Client(verify="/etc/ssl/certs/ca-bundle.crt")

requests_session = requests.Session()
requests_session.verify = True

connector = aiohttp.TCPConnector(ssl=True)
session = aiohttp.ClientSession(connector=connector)

pool = urllib3.PoolManager(cert_reqs="CERT_REQUIRED")
proxy = PoolManager(cert_reqs=ssl.CERT_REQUIRED, assert_hostname=True)

context = ssl.create_default_context()
ssl._create_default_https_context = ssl.create_default_context
context.verify_mode = ssl.CERT_REQUIRED
context.check_hostname = True

async def fetch(session):
    return await session.get("https://api.example.com", ssl=True)


def make_connector():
    return TCPConnector(ssl=True)
