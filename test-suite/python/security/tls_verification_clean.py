import ssl
import httpx
import aiohttp
import urllib3
import requests
from aiohttp import TCPConnector
from urllib3 import PoolManager


httpx.get("https://api.example.com", verify=True, timeout=3)
httpx.Client(verify="/etc/ssl/certs/ca-bundle.crt", timeout=3)

requests_session = requests.Session()
requests_session.verify = True

connector = aiohttp.TCPConnector(ssl=True)
session = aiohttp.ClientSession(connector=connector, timeout=aiohttp.ClientTimeout(total=5))

pool = urllib3.PoolManager(cert_reqs="CERT_REQUIRED", timeout=urllib3.Timeout(connect=2, read=5))
proxy = PoolManager(cert_reqs=ssl.CERT_REQUIRED, assert_hostname=True, timeout=3)

context = ssl.create_default_context()
ssl._create_default_https_context = ssl.create_default_context
context.verify_mode = ssl.CERT_REQUIRED
context.check_hostname = True

async def fetch(session):
    return await session.get("https://api.example.com", ssl=True, timeout=5)


def make_connector():
    return TCPConnector(ssl=True)
