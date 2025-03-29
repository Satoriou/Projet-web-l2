import sqlite3
import json
from werkzeug.security import generate_password_hash

DBFILENAME = 'site.sqlite'

def db_run(query, args=(), db_name=DBFILENAME):
  with sqlite3.connect(db_name) as conn:
    cur = conn.execute(query, args)
    conn.commit()

def load(db_name=DBFILENAME):
    db_run('DROP TABLE IF EXISTS user')

    db_run('CREATE TABLE user (id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,password_hash TEXT NOT NULL)')

    
load()

