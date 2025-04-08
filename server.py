from flask import Flask, session, Response, request, redirect, url_for, render_template
from functools import wraps
import data_model as model
import os
app = Flask(__name__)


app.secret_key = os.urandom(24)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_name' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

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

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_name', None)
    return redirect(url_for('home'))

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


@app.route('/profil', methods=['GET', 'POST'])
@login_required
def profil():
    return render_template('profil.html')



@app.route('/social')
@login_required
def social():
    friends = model.list_friends(session['user_name'])
    groups = model.list_groups(session['user_name'])
    return render_template('social.html', friends=friends, groups=groups)



@app.route('/add_friend', methods=('POST',))
@login_required
def add_friend():
    friend_name = request.form['friend_name']
    if model.user_exist(friend_name):
        model.add_friend(session['user_name'], friend_name)
    return redirect(url_for('social'))


@app.route('/display_note/<int:id>')
def afficher_note(id):
    note = model.note(id)
    return render_template('displayNote.html', note=note)


@app.route('/Mes-notes')
@login_required
def notes():
    notes = model.list_notes(session['user_name'])
    return render_template('notes.html', notes=notes)



@app.route('/add_note', methods=['POST'])
@login_required
def add_note():
    note_title = request.form['noteTitle']
    note_content = request.form['noteContent']
    model.new_note(note_title, note_content, session['user_name'])
    
    return redirect(url_for('notes'))


@app.route('/take_note')
@login_required
def take_note():
    return render_template('takeNote.html')


@app.get('/')
@login_required
def home():
  return render_template('index.html')


if __name__ == "__main__":
    app.run()