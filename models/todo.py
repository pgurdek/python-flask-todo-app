from models.sql import Database


class Todo:
    """ Class representing todo item."""

    def __init__(self, id, name, done=False, priority=1, create_date="", due_to=""):
        self.id = id
        self.name = name
        self.done = done
        self.priority = priority
        self.create_date = create_date
        self.due_to = due_to


    def addTask(self,list_id):
        sqlQuery = "INSERT INTO todo_items(name,done,priority,create_date,due_to,todo_list_id) VALUES (?,?,?,?,?,?)"
        param = [self.name, self.done, self.priority, self.create_date, self.due_to,list_id]
        Database.query(sqlQuery,param)

    def toggle(self):
        """ Toggles item's state """
        sqlQuery = "UPDATE todo_items SET done=? WHERE id=?"
        toggle = not self.done
        Database.query(sqlQuery, [toggle, self.id])

    def save(self):
        """ Saves/updates todo item in database """
        sqlQuery = "UPDATE todo_items SET name=? WHERE id=?"
        Database.query(sqlQuery, [self.name, self.id])

    def delete(self):
        """ Removes todo item from the database """
        sqlQuery = "DELETE FROM todo_items WHERE  id=?"
        Database.query(sqlQuery, [self.id])

    @classmethod
    def get_all(cls, todoListID):
        """ Retrieves all Todos form database and returns them as list.
        Returns:
            list(Todo): list of all todos
        """
        sqlQuery = "SELECT id,name,done,priority,create_date,due_to FROM todo_items WHERE todo_list_id=?"
        allTasks = Database.query(sqlQuery, [todoListID, ])
        taskObjectList = []
        if allTasks:
            for task in allTasks:
                taskObjectList.append(Todo(task[0], task[1], [task[2]]))

        return taskObjectList

    @classmethod
    def get_by_id(cls, id):
        """ Retrieves todo item with given id from database.
        Args:
            id(int): item id
        Returns:
            Todo: Todo object with a given id
        """
        sqlQuery = "SELECT id,name,done,priority,create_date,due_to FROM todo_items WHERE id=? "
        print('Get by ID', Database.query(sqlQuery, [id, ]))
        todoData = Database.query(sqlQuery, [id, ])[0]

        return Todo(todoData[0], todoData[1], todoData[2])
