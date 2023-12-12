import sqlite3
from logger import logger
import Project

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



    def item(self, id_: int, lang: str, addon: Project) -> tuple:
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

        return result
        
