from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import datetime
from models.user import User
from models.todo_list import TodoList
from models.todo import Todo
from functools import wraps
from models.alchemy_model import db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db.app = app
db.init_app(app)
app.secret_key = os.urandom(24)
app.user = None




# login required decorator
def login_required(f):
    """
    Check if user is in session
    :param f:
    :return:
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first')
            return redirect(url_for('login'))

    return wrap




def logged_already(f):
    """
    Redicret user to logout page
    :param f:
    :return:
    """
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
    """
    Show all projects of current user
    Add project to current user
    Remove project to current user
    :return:
    """
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
            project = TodoList.get_by_id(request.form['todoListID'])
            project.delete()

    return render_template('index.html', user=userLogged, todoObjectList=todoObjectList)


@app.route("/login", methods=["GET", "POST"])
@logged_already
def login():
    """
    Login to TODO app
    :return:
    """
    error = None
    users = User.userList()
    if request.method == "POST":
        for user in users:

            if request.form['username'] == user.username and request.form['password'] == user.password:
                session['logged_in'] = True
                app.user = user
                return redirect(url_for('index'))
            else:
                error = "Invalid Credentials. Please Try Again "

    return render_template("login.html", error=error)


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    """
    Log out from current session
    :return:
    """
    if request.method == "POST":
        if request.form['logout'] == "1":
            session.pop('logged_in', None)
            app.user = None
            flash('You are logged out, Have Fun')
            return redirect(url_for('login'))

    return render_template('logout.html')


@app.route('/todo_items', methods=["GET", "POST"])
@login_required
def todo_items(getID=None):
    """
    Show all todos of current project
    Add todos to current project
    Remove todo from current project
    :return:
    """
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
            taskObject.save()
            return redirect(url_for('todo_items', todoList=list_id))
        elif request.form['action'] == "Save":
            reqeustID = request.form['taskID']
            taskObject = Todo.get_by_id(reqeustID)
            taskObject.name = request.form['editTask']
            taskObject.due_to = request.form['editDate']
            taskObject.save()
            return redirect(url_for('todo_items', todoList=list_id))
        elif request.form['action'] == "Delete":
            reqeustID = request.form['taskID']
            taskObject = Todo.get_by_id(reqeustID)
            taskObject.delete()
            return redirect(url_for('todo_items', todoList=list_id))
        elif request.form['action'] == "Add New Task":
            name = request.form['taskName']
            dueTo = request.form['taskDueTo']
            priority = request.form['taskPriority']
            currentDate = datetime.datetime.today().strftime('%Y-%m-%d')


            newTask = Todo(None, name, priority, currentDate,list_id,dueTo,0)
            newTask.save()
            return redirect(url_for('todo_items', todoList=list_id))

        elif request.form['action'] == "Filter":
            d_from = str(request.form.get('d_from'))
            d_to = str(request.form.get('d_to'))
            sortedTodos = Todo.get_by_date(d_from, d_to,list_id)
            return render_template('todo_items.html', tasksObjectList=sortedTodos, list_id=list_id)

    return render_template('todo_items.html')

@app.context_processor
def override_url_for():
    """Overrides url_for with additional values on end (cache prevent)"""
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    """Add on end to static files a int value(time)  """
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)



if __name__ == "__main__":
    app.run(debug=True)
