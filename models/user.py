class User():
    def __init__(self, username, password):
        self.username = username
        self.password = password

    @classmethod
    def addUser(cls,username,password):
        return cls(username,password)

