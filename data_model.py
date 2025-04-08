import sqlite3
import math
from werkzeug.security import generate_password_hash, check_password_hash

DBFILENAME = 'site.sqlite'

# Utility functions
def db_fetch(query, args=(), all=False, db_name=DBFILENAME):
  with sqlite3.connect(db_name) as conn:
    # to allow access to columns by name in res
    conn.row_factory = sqlite3.Row 
    cur = conn.execute(query, args)
    # convert to a python dictionary for convenience
    if all:
      res = cur.fetchall()
      if res:
        res = [dict(e) for e in res]
      else:
        res = []
    else:
      res = cur.fetchone()
      if res:
        res = dict(res)
  return res
        

def db_insert(query, args=(), db_name=DBFILENAME):
  with sqlite3.connect(db_name) as conn:
    cur = conn.execute(query, args)
    conn.commit()
    return cur.lastrowid


def db_run(query, args=(), db_name=DBFILENAME):
  with sqlite3.connect(db_name) as conn:
    cur = conn.execute(query, args)
    conn.commit()


def db_update(query, args=(), db_name=DBFILENAME):
  with sqlite3.connect(db_name) as conn:
    cur = conn.execute(query, args)
    conn.commit()
    return cur.rowcount


def login(name, password):
    user = db_fetch('SELECT * FROM users WHERE name = ?', (name,))
    if user and check_password_hash(user['password_hash'], password):
        return user['name']
    return -1


def new_user(name, password):
    password_hash = generate_password_hash(password)
    user_name = db_insert('INSERT INTO users (name, password_hash) VALUES (?, ?)', (name, password_hash))
    return user_name


def new_note(title, content,owner):
    note_id = db_insert('INSERT INTO notes (title, content, owner_name) VALUES (?, ?, ?)', (title, content, owner))
    return note_id

def add_friend(user, friend):
    if db_fetch('SELECT * FROM friends WHERE (user_name = ? AND friend_name = ?) OR (friend_name = ? AND user_name = ?)' , (user,friend,)) == None:
        friends_id = db_insert('INSERT INTO friends (user_name, friend_name) VALUES (?, ?)', (user, friend))
    return friends_id

def list_friends(user):
    return db_fetch('SELECT * FROM friends WHERE user_name = ? OR friend_name = ?', (user,user, ), True)

def list_groups(user):
    return db_fetch('SELECT * FROM memgroup WHERE member_name = ?', (user,))

def user_exist(name):
    user = db_fetch('SELECT * FROM users WHERE name = ?', (name,))
    return user!= None


def list_notes(name):
    return db_fetch('SELECT * FROM notes WHERE owner_name = ?', (name, ), True)

def note(note_id):
    return db_fetch('SELECT * FROM notes WHERE id = ?', (note_id,))
    
    
    
    