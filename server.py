from flask import Flask, session, Response, request, redirect, url_for, render_template
from functools import wraps
import data_model as model
import os
app = Flask(__name__)


app.secret_key = os.urandom(24)

#permet de sécuriser l'accès aux pages du site
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_name' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

#permet de se connecter
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        user_name = model.login(name, password)
        if user_name != -1:
            session['user_name'] = user_name
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

#permet de se déconnecter
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_name', None)
    return redirect(url_for('home'))

#permet de créer un nouveau compte
@app.route('/new_user', methods=['GET', 'POST'])
def new_user():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        if model.user_exist(name):
            return render_template('new_user.html', error="Invalid credentials")
        user_name = model.new_user(name, password)
        session['user_name'] = name
        return redirect(url_for('home'))
    return render_template('new_user.html')

#renvoie vers la page du profil
@app.route('/profil', methods=['GET', 'POST'])
@login_required
def profil():
    return render_template('profil.html')


#renvoie vers la page des groupes et des amis
@app.route('/social')
@login_required
def social():
    friends = model.list_friends(session['user_name'])
    groups = model.list_groups(session['user_name'])
    return render_template('social.html', friends=friends, groups=groups)


#permet à l'utilisateur d'ajouter un ami
@app.route('/add_friend', methods=('POST',))
@login_required
def add_friend():
    friend_name = request.form['friend_name']
    if model.user_exist(friend_name) and friend_name != session['user_name']:
        model.add_friend(session['user_name'], friend_name)
    return redirect(url_for('social'))

#permet à l'utilisateur de supprimer un ami
@app.route('/supprimer-ami/<string:friend_name>', methods=['GET'])
@login_required
def supprimerAmi(friend_name):
    
    model.withdraw_friend(friend_name, session['user_name'])
    
    return redirect(url_for('social'))

#permet à l'utilisateur de créer un groupe
@app.route('/create_group', methods=('POST',))
@login_required
def creer_groupe():
    group_name = request.form['nom_groupe']
    groupe = model.create_groupe(group_name,session['user_name'])
    model.add_member_group(groupe, session['user_name'])
    
    return redirect(url_for('social'))
    
#renvoie la page pour afficher un groupe
@app.route('/group/<int:group_id>')
@login_required
def afficher_groupe(group_id):
    
    group = model.group(group_id)
    notes_group = model.notes_group(group_id)
    
    user_notes = model.list_notes(session['user_name'])
    user_firends = model.list_friends(session['user_name'])
    memgroup = model.list_memgroup(group_id)
    
    return render_template('group.html', group=group, notes=notes_group, user_notes=user_notes, user_firends=user_firends, memgroup=memgroup)

#permet d'ajouter un note à un groupe
@app.route('/ajouter-note-groupe/<int:groupe_id>', methods=['POST'])
@login_required
def ajouterNoteGroupe(groupe_id):
    note_id = request.form['note_id']
    
    liste_note_group = []
    notes_group =  model.notes_group(groupe_id)
    for note in notes_group:
        liste_note_group.append(str(note['id']))
    if(note_id not in liste_note_group):
        model.add_note_group(groupe_id, note_id)
    
    return redirect(url_for('afficher_groupe', group_id=groupe_id))

#permet à l'admin d'un groupe ou au propiétaire d'une note de la supprimer du groupe
@app.route('/supprimer-note-group/<int:group_id>/<int:note_id>', methods=['GET'])
@login_required
def retirerNoteGroupe(group_id,note_id):
    
    model.withdraw_note_group(group_id,note_id)
    
    return redirect(url_for('afficher_groupe', group_id=group_id))

#permet à l'admin d'un groupe de supprimer celui-ci
@app.route('/supprimer-groupe/<int:group_id>', methods=['GET'])
@login_required
def supprimerGroupe(group_id):
    
    model.withdraw_group(group_id)
    
    return redirect(url_for('social'))

#permet à l'admin d'un groupe de supprimer un membre
@app.route('/supprimer-mem-group/<int:group_id>/<string:mem_name>', methods=['GET'])
@login_required
def supprimerMemGroup(group_id, mem_name):
    
    model.withdraw_mem_goup(group_id, mem_name)
    
    return redirect(url_for('afficher_groupe', group_id=group_id))

#permet de quitter un groupe
@app.route('/quitter-groupe/<int:group_id>', methods=['GET'])
@login_required
def quitterGroupe(group_id):
    
    model.leftgroup(group_id, session['user_name'])
    
    return redirect(url_for('social'))


#permet d'ajoute un ami de l'utilisateur à un groupe dont il fait partis
@app.route('/ajouter-ami-groupe/<int:groupe_id>', methods=['POST'])
@login_required
def ajouter_ami_groupe(groupe_id):
    friend_name = request.form['friend_name']
    
    
    members_group =  model.list_memgroup(groupe_id)
    list_name_members = []
    
    for member in members_group:
        list_name_members.append(str(member['member_name']))
        
    if(friend_name not in list_name_members):
        model.add_member_group(groupe_id, friend_name)

    return redirect(url_for('afficher_groupe', group_id=groupe_id))

#afficher une note dans le context d'un groupe
@app.route('/display_note_group/<int:group_id>/<int:note_id>')
@login_required
def afficher_note_group(group_id,note_id):
    note = model.note(note_id)
    
    return render_template('notes-group.html', note=note, group=model.group(group_id))

#affiche une note
@app.route('/display_note/<int:id>')
@login_required
def afficher_note(id):
    note = model.note(id)
    return render_template('displayNote.html', note=note)

#renvoie vers la page d'affichage des notes
@app.route('/Mes-notes')
@login_required
def notes():
    notes = model.list_notes(session['user_name'])
    return render_template('notes.html', notes=notes)


#permet d'ajouter une note
@app.route('/add_note', methods=['POST'])
@login_required
def add_note():
    note_title = request.form['noteTitle']
    note_content = request.form['noteContent']
    model.new_note(note_title, note_content, session['user_name'])
    
    return redirect(url_for('notes'))

#permet de supprimer une note
@app.route('/withdraw_note/<int:note_id>', methods=['GET'])
@login_required
def withdraw_note(note_id):
    model.withdraw_note(note_id)
    
    return redirect(url_for('notes'))

#renvoie vers la page de prise de note
@app.route('/take_note')
@login_required
def take_note():
    return render_template('takeNote.html')

#permet de supprimer un compte
@app.route('/delete-user', methods=['GET'])
@login_required
def delete_user():
    model.delete_user(session['user_name'])
    logout()
    return redirect(url_for('home'))


#renvoie à la page d'accueil
@app.get('/')
@login_required
def home():
  return render_template('index.html')


if __name__ == "__main__":
    app.run()