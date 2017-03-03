from models.sql import Database

class User():
    def __init__(self,username, password):
        self.username = username
        self.password = password

    @classmethod
    def addUser(cls,username,password):
        Database.query('INSERT OR IGNORE INTO USERS (username,password) VALUES (?,?)',[username,password])


    @classmethod
    def listUsers(cls):
        user_list = []
        users = Database.query('SELECT * FROM USERS')
        for user in users:
            user_list.append(cls(user[1],user[2]))

        return user_list
