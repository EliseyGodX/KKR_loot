import sqlite3
from logger import logger
import Project
from fuzzywuzzy import process

P = 'DB.db.{}'


class DB:
    global P

    def __init__(self, project: str, addon: str, 
                 fields: tuple, _projects = []) -> None:
        self.project = project
        self.addon = addon
        self.fields = fields

        try:
            self.db = sqlite3.connect(f'DB/dbs/{self.project}.db')
            self.cursor = self.db.cursor()
            logger.debug(f'---{P.format(self.project)} initialization---')
            _projects.append(self.project) 

        except Exception as exc:
            logger.critical(
                f'{P.format(self.project)} CRITICAL ERROR IN db_initialization: \n{exc}')
            exit()



    def item_by_id(self, id_: int, lang: str, addon: Project) -> tuple:
        self.cursor.execute(f'''SELECT * FROM {self.addon} 
                            WHERE id = (?) AND lang = ?''', (id_, lang, ))
        result = self.cursor.fetchone()
        
        if result is None:
            result = addon.parse(id_=id_, lang=lang)
            if result is not None:
                self.cursor.execute(
                    f'''INSERT INTO {self.addon} ({', '.join(self.fields)}) 
                    VALUES ({', '.join(['?' for _ in self.fields])})''', result)
                self.db.commit()
                logger.debug(f'{P.format(self.project)} new item ({lang}) - {id_}')

        return result
    


    def item_by_name(self, name: str, items: str) -> tuple:
        item = process.extractOne(name, items)
        return self.cursor.execute(f'''SELECT * FROM {self.addon} 
                                   WHERE name = (?)''', (item[0],)).fetchall()
        


    def new_item(self, id_: int, lang: str, addon: Project) -> None:
        if self.cursor.execute(f'''SELECT * FROM {self.addon} 
                            WHERE id = (?) AND lang = ?''', 
                            (id_, lang, )).fetchall() is None:
            self.cursor.execute(
                    f'''INSERT INTO {self.addon} ({', '.join(self.fields)}) 
                    VALUES ({', '.join(['?' for _ in self.fields])})''', 
                    addon.parse(id_=id_, lang=lang))
            self.db.commit()
            
        
