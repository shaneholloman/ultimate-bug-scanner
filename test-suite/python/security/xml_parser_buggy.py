import xml.etree.ElementTree as ET
from xml.dom import minidom
from xml.sax import parseString
from lxml import etree
from lxml.etree import XMLParser, fromstring


class Upload:
    def read(self):
        return b"<root/>"


class Request:
    data = b"<!DOCTYPE root [<!ENTITY xxe SYSTEM 'file:///etc/passwd'>]><root>&xxe;</root>"
    body = b"<root/>"
    files = {"xml": Upload()}

    def get_data(self):
        return self.data


request = Request()

payload = request.get_data()
ET.fromstring(payload)
ET.XML(request.body)
minidom.parseString(request.data)
parseString(request.files["xml"].read())

dangerous_parser = etree.XMLParser(
    resolve_entities=True,
    load_dtd=True,
    no_network=False,
    huge_tree=True,
)
etree.fromstring(request.data, parser=dangerous_parser)
fromstring(request.data, parser=XMLParser(resolve_entities=True))
