from models.sql import Database


class User():
    def __init__(self, username, password, avaiablelists=None):
        self.username = username
        self.password = password
        self.avaiablelists = avaiablelists

    @classmethod
    def addUser(cls, username, password):
        Database.query('INSERT OR IGNORE INTO USERS (username,password) VALUES (?,?)', [username, password])

    @classmethod
    def userList(cls):
        user_list = []
        users = Database.query('SELECT * FROM USERS')
        for user in users:
            user_list.append(cls(user[1], user[2]))

        return user_list

    def getID(self):
        query = "SELECT id FROM users WHERE username=?"
        return Database.query(query, [self.username, ])[0][0]

    def avaiableLists(self):
        avaiableList = []
        query = "SELECT todo_lists.id FROM todo_lists LEFT JOIN users ON user_id = users.id WHERE username=?"
        for item in  Database.query(query, [self.username, ]):
            avaiableList.append(item[0])
        self.avaiablelists = avaiableList
        print('Lista Dostepna', self.avaiablelists)