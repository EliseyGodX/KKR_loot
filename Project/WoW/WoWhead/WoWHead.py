import requests
import xml.etree.ElementTree as ET
from logger import logger

P = 'db.WoW.WoWHead.{}'


class WoWHead:

    def __init__(self, addon: str, test: list) -> None:
        self.efficiency = True  # for test
        self.addon = addon

        try:  # chek for WoWHead
            if parse_xml(id_=test[0], lang='eng',
                            efficiency=self.efficiency,
                            addon=self.addon)[2] == 'Hearthstone': 
                logger.debug(f'---{P.format(self.addon)} initialization---')
            
            else:  # if WoWHead is broken
                self.efficiency = False
                logger.error(f'{P.format(self.addon)} efficiency != True')

        except Exception as exc:  # for unexpected error
            self.efficiency = False
            logger.error(f'{P.format(self.addon)} CRITICAL ERROR IN initialization: \n{exc}')


    
    @logger.catch
    def parse(self, id_, lang) -> tuple:
        return parse_xml(id_=id_, lang=lang, 
                         efficiency=self.efficiency,
                         addon=self.addon)






@logger.catch
def parse_xml(id_: int, lang: str, efficiency: bool, addon: str) -> tuple | None:
    if efficiency is not True: return
    if lang == 'eng': lang = ''
    
    url = f"https://www.wowhead.com/{addon}/{lang}/item={id_}&xml"
    response = requests.get(url)
    xml_data = response.content

    tree = ET.ElementTree(ET.fromstring(xml_data))

    if tree.find(".//error") is not None: return  # for bad id
    
    name = tree.find(".//name").text.strip()
    ilvl = tree.find(".//level").text.strip()
    try: slot = tree.find(".//inventorySlot").text.strip()
    except: slot = 'None'
    if lang == '': lang = 'eng'

    return (id_, lang, name.lower(), ilvl, slot)
