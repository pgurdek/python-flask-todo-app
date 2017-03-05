from flask import Flask, render_template, request, redirect, url_for, session, flash, g
import os
import datetime
from models.sql import Database
from models.user import User
from functools import wraps
from models.todo import Todo
from models.todo_list import TodoList

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.user = None


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


# login required decorator
def Permission(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session['todoIdRequest'] in app.user.avaiablelists:
            return f(*args, **kwargs)
        else:
            flash('Wrong Persmission try again')
            return redirect(url_for('index'))

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


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    userLogged = app.user
    todoObjectList = TodoList.listOfTodo(userLogged)
    if not todoObjectList:
        todoObjectList = ['You have not any ToDoList, Create New Please']
    if request.method == "POST":
        if request.form['actionListToDo'] == "Add New List":
            if request.form['todoName'] != None and request.form['todoName'] != '':
                TodoList.addToDoList(request.form['todoName'], userLogged)
                return redirect(url_for('index'))
        elif request.form['actionListToDo'] == "Delete":
            TodoList.removeToDoList(request.form['todoListID'], userLogged)
            return redirect(url_for('index'))
    return render_template('index.html', user=userLogged, todoObjectList=todoObjectList)


@app.route("/login", methods=["GET", "POST"])
@logged_already
def login():
    error = None
    users = User.userList()
    if request.method == "POST":
        for user in users:
            if request.form['username'] == user.username and request.form['password'] == user.password:
                session['logged_in'] = True
                app.user = user
                app.user.avaiableLists()
                return redirect(url_for('index'))
            else:
                error = "Invalid Credentials. Please Try Again "

    return render_template("login.html", error=error)


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    if request.method == "POST":
        if request.form['logout'] == "1":
            session.pop('logged_in', None)
            app.user = None
            flash('You are logged out, Have Fun')
            return redirect(url_for('login'))

    return render_template('logout.html')


@app.route('/todo_items', methods=["GET", "POST"])
# @app.route('/todo_items?todoList=<int:getID>',methods=["GET", "POST"])
@login_required
def todo_items(getID=None):
    """ Shows list of todo items stored in the database."""
    list_id = request.args.get('todoList')
    if request.method == 'GET':
        list_id = request.args.get('todoList')
        session['todoIdRequest'] = list_id
        tasksObjectList = Todo.get_all(list_id)
        return render_template('todo_items.html', tasksObjectList=tasksObjectList, list_id=list_id)

    elif request.method == "POST":

        if request.form['action'] == "Toggle":
            reqeustID = request.form['taskID']
            taskObject = Todo.get_by_id(reqeustID)
            taskObject.toggle()
            return redirect(url_for('todo_items', todoList=list_id))
        elif request.form['action'] == "Save":
            reqeustID = request.form['taskID']
            taskObject = Todo.get_by_id(reqeustID)
            if request.form['editTask']:
                taskObject.name = request.form['editTask']
                taskObject.save()
            return redirect(url_for('todo_items', todoList=list_id))
        elif request.form['action'] == "Delete":
            reqeustID = request.form['taskID']
            taskObject = Todo.get_by_id(reqeustID)
            taskObject.name = request.form['editTask']
            taskObject.delete()
            return redirect(url_for('todo_items', todoList=list_id))
        elif request.form['action'] == "Add New Task":
            # if request.form('taskName') is not None and request.form('taskName') != '':
            name = request.form['taskName']
            print(name)
            priority = request.form['taskPriority']
            currentDate = datetime.datetime.today().strftime('%Y-%m-%d')
            dueTo = request.form['taskDueTo']
            print(dueTo)
            newTask = Todo(1, name, False, priority, currentDate, dueTo)
            newTask.addTask(list_id)
            return redirect(url_for('todo_items', todoList=list_id))
            # if request.form['taskName'] != None and request.form['taskName'] != '':
            #     TodoList.addToDoList(request.form['todoName'],userLogged)
            #     return redirect(url_for('index'))
    return render_template('todo_items.html')


# @app.route("/add", methods=['GET', 'POST'])
# def add():
#     """ Creates new todo item
#     If the method was GET it should show new item form.
#     If the method was POST it shold create and save new todo item.
#     """
#     return "Add todo"
#
#
# @app.route("/remove/<todo_id>")
# def remove(todo_id):
#     """ Removes todo item with selected id from the database """
#     return "Remove " + todo_id
#
#
# @app.route("/edit/<todo_id>", methods=['GET', 'POST'])
# def edit(todo_id):
#     """ Edits todo item with selected id in the database
#     If the method was GET it should show todo item form.
#     If the method was POST it shold update todo item in database.
#     """
#     return "Edit " + todo_id
#
#
# @app.route("/toggle/<todo_id>")
# def toggle(todo_id):
#     """ Toggles the state of todo item """
#     return "Toggle " + todo_id


if __name__ == "__main__":
    app.run(debug=True)
