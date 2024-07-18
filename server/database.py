import sqlite3
from flask import g

DATABASE = 'forex_data.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS forex_data
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         from_currency TEXT,
                         to_currency TEXT,
                         period TEXT,
                         date TEXT,
                         open REAL,
                         high REAL,
                         low REAL,
                         close REAL,
                         volume INTEGER)''')