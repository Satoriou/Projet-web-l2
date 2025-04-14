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

#permet de se connecter au site
def login(name, password):
    user = db_fetch('SELECT * FROM users WHERE name = ?', (name,))
    if user and check_password_hash(user['password_hash'], password):
        return user['name']
    return -1

#ajouter un uilisateur
def new_user(name, password):
    password_hash = generate_password_hash(password)
    user_name = db_insert('INSERT INTO users (name, password_hash) VALUES (?, ?)', (name, password_hash))
    return user_name

#créer une note
def new_note(title, content,owner):
    note_id = db_insert('INSERT INTO notes (title, content, owner_name) VALUES (?, ?, ?)', (title, content, owner))
    return note_id

#ajoute un ami à l'utilisateur
def add_friend(user, friend):
    friends_id = None
    if (db_fetch('SELECT * FROM friends WHERE (user_name = ? AND friend_name = ?) OR (friend_name = ? AND user_name = ?)' , (user,friend,user,friend,)) == None):
        friends_id = db_insert('INSERT INTO friends (user_name, friend_name) VALUES (?, ?)', (user, friend))
    return friends_id

#renvoi la liste d'amis de l'utilisateur
def list_friends(user):
    return db_fetch('SELECT * FROM friends WHERE user_name = ? OR friend_name = ?', (user,user, ), True)

#renvoi la liste des groupes dans lesquels est l'utilisateur
def list_groups(user):
    return db_fetch('SELECT * FROM memgroup JOIN groups ON memgroup.group_id=groups.id WHERE member_name = ?', (user,), True)

#vérifier si l'utilisateur associé au nom existe
def user_exist(name):
    user = db_fetch('SELECT * FROM users WHERE name = ?', (name,))
    return user!= None

#renvoi la liste des notes d'un utilisateur
def list_notes(name):
    return db_fetch('SELECT * FROM notes WHERE owner_name = ?', (name, ), True)

#renvoi les données d'une note
def note(note_id):
    return db_fetch('SELECT * FROM notes WHERE id = ?', (note_id,))

#renvoi les données d'un groupe
def group(group_id):
    return db_fetch('SELECT * FROM groups WHERE id = ?', (group_id,))

#lister les notes d'un groupe
def notes_group(group_id):
    return db_fetch('SELECT * FROM notegroup JOIN notes ON notes.id=notegroup.note_id WHERE group_id = ?', (group_id,), True)

#ajouter une note à un groupe
def add_note_group(group_id, note_id):
    return db_insert('INSERT INTO notegroup (group_id, note_id) VALUES (?, ?)', (group_id, note_id))

#ajouter un membre à un groupe
def add_member_group(group_id, member_name):
    return db_insert('INSERT INTO memgroup (group_id, member_name) VALUES (?, ?)', (group_id, member_name))

#créer un groupe
def create_groupe(group_name, owner_name):
    return db_insert('INSERT INTO groups (name, owner_name) VALUES (?, ?)', (group_name, owner_name))
    
#lister les membres d'un groupe  
def list_memgroup(group_id):
    return db_fetch('SELECT * FROM memgroup WHERE group_id = ?', (group_id,), True)

#supprimer une note
def withdraw_note(note_id):
    db_run('DELETE FROM notes WHERE id = ?', (note_id,))
    db_run('DELETE FROM notegroup WHERE note_id = ?', (note_id,))

#supprimer un note d'un groupe
def withdraw_note_group(group_id,note_id):
    db_run('DELETE FROM notegroup WHERE note_id = ? AND group_id = ?', (note_id, group_id,))

#supprimer un groupe
def withdraw_group(group_id):
    db_run('DELETE FROM notegroup WHERE group_id = ?', (group_id,))
    db_run('DELETE FROM memgroup WHERE group_id = ?', (group_id,))
    db_run('DELETE FROM groups WHERE id = ?', (group_id,))
    
#enlever un membre d'un groupe
def withdraw_mem_goup(group_id, mem_name):
    db_run('DELETE FROM memgroup WHERE member_name = ? AND group_id = ?', (mem_name, group_id,))
    
#quitter un groupe
def leftgroup(group_id, mem_name):
    db_run('DELETE FROM memgroup WHERE member_name = ? AND group_id = ?', (mem_name, group_id,))
    
    db_run('DELETE FROM notegroup WHERE group_id = ? IN (SELECT group_id FROM notegroup JOIN notes ON notegroup.note_id=notes.id WHERE notes.owner_name= ?)',(group_id,mem_name,))
    
# supprimer un ami
def withdraw_friend(friend_name, user_name):
    db_run('DELETE FROM friends WHERE (user_name = ? AND friend_name = ?) OR (friend_name = ? AND user_name = ?)', (friend_name, user_name,friend_name, user_name,))

#supprimer un utilisateur
def delete_user(user_name):
    db_run('DELETE FROM friends WHERE user_name= ? OR friend_name = ?', (user_name,user_name,))
    liste_notes = list_notes(user_name)
    liste_groupes = list_groups(user_name)
    
    for groupe in liste_groupes:
        withdraw_mem_goup(groupe['id'], user_name)
        
        for note in liste_notes:
            withdraw_note_group(groupe['id'], note['id'])
            withdraw_note(note['id'])
    db_run('DELETE FROM users WHERE name = ?', (user_name,))









