import sqlite3
from logger import logger
from db import WoW

P = 'db.db'

@logger.catch
def db_initialization() -> None:
    global db, cursor
    try:
        db = sqlite3.connect('db/items.db')
        cursor = db.cursor()

        logger.debug(f'---{P} initialization---')
    except Exception as exc:
        logger.critical(f'{P} CRITICAL ERROR IN db_initialization: \n{exc}')
        exit()

