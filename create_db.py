import sqlite3
import json
from werkzeug.security import generate_password_hash

DBFILENAME = 'site.sqlite'

def db_run(query, args=(), db_name=DBFILENAME):
  with sqlite3.connect(db_name) as conn:
    cur = conn.execute(query, args)
    conn.commit()

def load(db_name=DBFILENAME):
    db_run('DROP TABLE IF EXISTS users')
    db_run('DROP TABLE IF EXISTS notes')
    db_run('DROP TABLE IF EXISTS groups')
    db_run('DROP TABLE IF EXISTS memgroup')
    db_run('DROP TABLE IF EXISTS notegroup')

    db_run('CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,password_hash TEXT NOT NULL)')
    
    db_run('CREATE TABLE notes (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, content TEXT NOT NULL, owner_id INTEGER NOT NULL,CONSTRAINT pk_owner_id FOREIGN KEY (owner_id) REFERENCES users(id))')
        
    db_run('CREATE TABLE groups (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, owner_id INTEGER NOT NULL, CONSTRAINT pk_owner_id FOREIGN KEY (owner_id) REFERENCES users(id))')
        
    db_run('CREATE TABLE memgroup (group_id INTEGER NOT NULL, member_id INTEGER NOT NULL, CONSTRAINT pk_member_id FOREIGN KEY (member_id) REFERENCES users(id),CONSTRAINT pk_group_id FOREIGN KEY (group_id) REFERENCES groups(id))')
        
    db_run('CREATE TABLE notegroup (group_id INTEGER NOT NULL, note_id INTEGER NOT NULL, CONSTRAINT pk_group_id FOREIGN KEY (group_id) REFERENCES groups(id), CONSTRAINT pk_note_id FOREIGN KEY (note_id) REFERENCES notes(id))')

    
load()

