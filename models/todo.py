import sqlite3


class Todo:
    """ Class representing todo item."""

    def __init__(self, id, name, done=False):
        pass

    def toggle(self):
        """ Toggles item's state """
        pass

    def save(self):
        """ Saves/updates todo item in database """
        pass

    def delete(self):
        """ Removes todo item from the database """
        pass

    @classmethod
    def get_all(cls):
        """ Retrieves all Todos form database and returns them as list.
        Returns:
            list(Todo): list of all todos
        """
        pass

    @classmethod
    def get_by_id(cls, id):
        """ Retrieves todo item with given id from database.
        Args:
            id(int): item id
        Returns:
            Todo: Todo object with a given id
        """
        pass
