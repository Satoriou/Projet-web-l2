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
    user = db_fetch('SELECT * FROM user WHERE name = ?', (name,))
    if user and check_password_hash(user['password_hash'], password):
        return user['id']
    return -1


def new_user(name, password):
    password_hash = generate_password_hash(password)
    user_id = db_insert('INSERT INTO user (name, password_hash) VALUES (?, ?)', (name, password_hash))
    return user_id
