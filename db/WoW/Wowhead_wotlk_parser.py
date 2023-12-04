import requests
import xml.etree.ElementTree as ET
from loguru import logger

logger.add('log/debug_db.log', format='{time} || {level} || {message}', rotation='2 MB')
logger.debug(f'esfsderfgsderfg')

def parse_xml(id_: int) -> str:
    url = f"https://www.wowhead.com/wotlk/ru/item={id_}&xml"
    response = requests.get(url)
    xml_data = response.content

    tree = ET.ElementTree(ET.fromstring(xml_data))

    name = tree.find(".//name").text.strip()
    ilvl = tree.find(".//level").text.strip()
    slot = tree.find(".//inventorySlot").text.strip()
