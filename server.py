from flask import Flask, session, Response, request, redirect, url_for, render_template
from functools import wraps
import data_model as model
import os
app = Flask(__name__)


app.secret_key = os.urandom(24)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        user_id = model.login(name, password)
        if user_id != -1:
            session['user_id'] = user_id
            session['user_name'] = name
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    return redirect(url_for('home'))

@app.route('/new_user', methods=['GET', 'POST'])
def new_user():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        user_id = model.new_user(name, password)
        session['user_id'] = user_id
        session['user_name'] = name
        return redirect(url_for('home'))
    return render_template('new_user.html')


@app.route('/profil', methods=['GET', 'POST'])
@login_required
def profil():
    return render_template('profil.html')

@app.route('/add_note', methods=['POST'])
@login_required
def add_note():
    note_title = request.form['noteTitle']
    note_content = request.form['noteContent']

    return render_template('index.html')


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