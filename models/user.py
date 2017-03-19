from models.alchemy_model import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(120))

    # def __init__(self, id, username, password):
    #     self.id = id
    #     self.username = username
    #     self.password = password

    def __repr__(self):
        return 'Username {}'.format(self.username)

    def add_user(self):
        """
        Add user to database
        :return:
        """
        db.session.flush()
        db.session.add(self)
        db.session.commit()


    @classmethod
    def userList(cls):
        """
        List all users
        :return:
        """
        users = cls.query.all()
        return users
    @classmethod
    def getID(cls,id):
        """
        Get user by id
        :param id:
        :return:
        """
        return db.session.query(User).get(id)
