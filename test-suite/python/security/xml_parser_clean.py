from defusedxml import ElementTree as DET
from defusedxml.ElementTree import fromstring
from lxml import etree


class Request:
    data = b"<root/>"


request = Request()

trusted_xml = b"<root><name>example</name></root>"
safe_parser = etree.XMLParser(
    resolve_entities=False,
    load_dtd=False,
    no_network=True,
)

DET.fromstring(request.data)
fromstring(request.data)
etree.fromstring(trusted_xml, parser=safe_parser)
