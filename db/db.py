import sqlite3

def db_initialization() -> None:
    global db, cursor
    db = sqlite3.connect('db/items.db')
    cursor = db.cursor()


