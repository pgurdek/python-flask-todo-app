from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
from models.sql import Database
from models.user import User
from functools import wraps
from models.todo import Todo

app = Flask(__name__)
app.secret_key = os.urandom(24)


# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first')
            return redirect(url_for('login'))
    return wrap

def logged_already(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            flash('You are already logged, please logout first')
            return redirect(url_for('logout'))
        else:
            flash('You need to login first')
            return f(*args, **kwargs)
    return wrap

@app.route("/")
@login_required
def index():
    return render_template('index.html')


@app.route("/login", methods=["GET", "POST"])
@logged_already
def login():
    error = None
    users = User.listUsers()
    if request.method == "POST":
        for user in users:
            if request.form['username'] == user.username and request.form['password'] == user.password:
                session['logged_in'] = True
                return redirect(url_for('index'))
            else:
                error = "Invalid Credentials. Please Try Again "

    return render_template("login.html", error=error)


@app.route("/logout",methods=["GET", "POST"])
@login_required
def logout():
    if request.method == "POST":
        if request.form['logout'] == "1":
            session.pop('logged_in', None)
            flash('You are logged out, Have Fun')
            redirect(url_for('login'))

    return render_template('logout.html')


@app.route('/todo_list')
@login_required
def todo_list():
    """ Shows list of todo items stored in the database."""


# @app.route("/")
# def list():
#     """ Shows list of todo items stored in the database.
#     """
#     return "Hello World!"


@app.route("/add", methods=['GET', 'POST'])
def add():
    """ Creates new todo item
    If the method was GET it should show new item form.
    If the method was POST it shold create and save new todo item.
    """
    return "Add todo"


@app.route("/remove/<todo_id>")
def remove(todo_id):
    """ Removes todo item with selected id from the database """
    return "Remove " + todo_id


@app.route("/edit/<todo_id>", methods=['GET', 'POST'])
def edit(todo_id):
    """ Edits todo item with selected id in the database
    If the method was GET it should show todo item form.
    If the method was POST it shold update todo item in database.
    """
    return "Edit " + todo_id


@app.route("/toggle/<todo_id>")
def toggle(todo_id):
    """ Toggles the state of todo item """
    return "Toggle " + todo_id


if __name__ == "__main__":
    app.run(debug=True)
