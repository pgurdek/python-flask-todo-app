from models.alchemy_model import db


class TodoList(db.Model):
    __tablename__ = 'todo_lists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    user_id = db.Column(db.Integer)

    def __init__(self, id, name, user_id):
        self.id = id
        self.name = name
        self.user_id = user_id

    def __repr__(self):
        return 'ID: {} Name :{} User_id :{} '.format(self.id, self.name, self.user_id)

    def delete(self):
        """
        Delete project from db
        :return:
        """
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def listOfTodo(cls, user):
        """
        List all projects of user
        :param user:
        :return:
        """
        todos = cls.query.filter_by(user_id=user.id)
        return todos

    @classmethod
    def addToDoList(cls, todoListName, user):
        """
        Add to new project
        :param todoListName:
        :param user:
        :return:
        """
        db.session.flush()
        db.session.add(cls(None, todoListName, user.id))
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        """
        Get project by id
        :param id:
        :return:
        """
        return cls.query.filter(cls.id == id).first()
