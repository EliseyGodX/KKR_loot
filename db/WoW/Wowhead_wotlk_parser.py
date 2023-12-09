import requests
import xml.etree.ElementTree as ET
from logger import logger

P = 'db.WoW.Wowhead_wotlk_parser'

efficiency = True


@logger.catch
def wowhead_wotlk_parser_initialization():
    global efficiency
    try:
        if parse_xml(6948, 'eng')[0] == 'Hearthstone':
            logger.debug(f'---{P} initialization---')
        else: 
            efficiency = False
            logger.error(f'{P} efficiency (WoWHead) != True')

    except Exception as exc:
        efficiency = False
        logger.error(f'{P} CRITICAL ERROR IN initialization: \n{exc}')



@logger.catch
def parse_xml(id_: int, lang: str) -> tuple | str:
    if efficiency is not True: 
        return ('WoWHead is broken', 'WoWHead is broken', 'WoWHead is broken')
    if lang == 'eng': lang = ''
    
    url = f"https://www.wowhead.com/wotlk/{lang}/item={id_}&xml"
    response = requests.get(url)
    xml_data = response.content

    tree = ET.ElementTree(ET.fromstring(xml_data))

    name = tree.find(".//name").text.strip()
    ilvl = tree.find(".//level").text.strip()
    try: slot = tree.find(".//inventorySlot").text.strip()
    except: slot = None

    return (name, ilvl, slot)