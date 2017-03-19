from models.alchemy_model import db


class Todo(db.Model):
    """ Class representing todo item."""
    __tablename__ = 'todo_items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    priority = db.Column(db.String(120))
    create_date = db.Column(db.String)
    todo_list_id = db.Column(db.Integer)
    due_to = db.Column(db.String)
    done = db.Column(db.Integer)
    archived = db.Column(db.Integer)

    def __init__(self, id,name, priority,create_date,todo_list_id,due_to,done,archived=0):
        self.id = id
        self.name = name
        self.priority = priority
        self.create_date = create_date
        self.todo_list_id = todo_list_id
        self.due_to = due_to
        self.done = done
        self.archived = archived

    def __repr__(self):
        return 'TodoItems Name: {} Parent id {} Done : {}'.format(self.name,self.todo_list_id,self.done)



    def toggle(self):
        """ Toggles item's state """
        if self.done == 0:
            self.done = 1
        else: self.done = 0

    def save(self):
        """ Saves/updates todo item in database """
        db.session.flush()
        db.session.add(self)
        db.session.commit()


    def delete(self):
        """ Archives todo item from the database """
        self.archived = 1
        self.save()

    @classmethod
    def get_all(cls, todoListID):
        """ Retrieves all Todos form database and returns them as list.
        Returns:
            list(Todo): list of all todos
        """
        todo_object_list = cls.query.filter_by(archived=0).filter(cls.todo_list_id==todoListID).order_by(cls.due_to).all()
        return todo_object_list

    @classmethod
    def get_by_date(cls, date_from, date_to,todoListID):
        """
        Get all todos between dates
        :param date_from:
        :param date_to:
        :return:
        """
        if not date_from:
            date_from = '1900-01-01'
        if not date_to:
            date_to = '2220-01-01'
        todo_list  = cls.query.filter_by(archived=0).filter(cls.todo_list_id==todoListID,cls.due_to.between(date_from, date_to)).order_by(cls.due_to).all()
        return todo_list

    @classmethod
    def get_by_id(cls, id):
        """ Retrieves todo item with given id from database.
        Args:
            id(int): item id
        Returns:
            Todo: Todo object with a given id
        """
        todo_object = db.session.query(Todo).get(id)
        return todo_object

