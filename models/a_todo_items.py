from main import db

class TodoItemsSQL(db.Model):
    __tablename__ = 'todo_items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    priority = db.Column(db.String(120))
    create_date = db.Column(db.DateTime)
    todo_list_id = db.Column(db.Integer)
    due_to = db.Column(db.DateTime)
    done = db.Column(db.Integer)

    def __init__(self, name, priority,create_date,todo_list_id,due_to,done):
        self.name = name
        self.priority = priority
        self.create_date = create_date
        self.todo_list_id = todo_list_id
        self.due_to = due_to
        self.done = done

    def __repr__(self):
        return 'TodoItems Name: {} Parent id {} Done : {}'.format(self.name,self.todo_list_id,self.done)