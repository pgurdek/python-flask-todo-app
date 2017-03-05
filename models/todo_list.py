from models.sql import Database
from models.user import User


class TodoList():
    def __init__(self, name, id=None):
        self.name = name
        self.id = id

    @classmethod
    def listOfTodo(cls, user):
        listOfTodo = []
        sqlQuery = "SELECT todo_lists.id,name FROM todo_lists LEFT JOIN users ON users.id = user_id WHERE username=?"
        dbListOfTodo = Database.query(sqlQuery, [user.username])
        for todo in dbListOfTodo:
            listOfTodo.append(TodoList(todo[1], todo[0]))

        return listOfTodo

    @classmethod
    def addToDoList(cls, todoListName, user):
        sqlQuery = "INSERT INTO todo_lists (name,user_id) VALUES (?,?)"
        userID = user.getID()
        Database.query(sqlQuery, [todoListName, userID])

    @classmethod
    def removeToDoList(cls, todoListName, user):
        sqlQuery = "DELETE FROM todo_lists WHERE user_id=? AND id=?"
        userID = user.getID()
        Database.query(sqlQuery, [userID, todoListName])
