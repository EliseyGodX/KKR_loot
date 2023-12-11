import sqlite3
from logger import logger
from Project import *

P = 'DB.db.{}'


class DB:
    global P

    def __init__(self, project: str, fields: tuple) -> None:
        self.project = project
        self.fields = fields
        
        try:
            self.db = sqlite3.connect(f'DB/dbs/{self.project}.db')
            self.cursor = self.db.cursor()
            logger.debug(f'---{P.formate(project)} initialization---')

        except Exception as exc:
            logger.critical(f'{P} CRITICAL ERROR IN db_initialization: \n{exc}')
            exit()


