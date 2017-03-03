import sqlite3
import os.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "db.sqlite")

class Database():

    @staticmethod
    def connect_db(database = db_path):
        print(database)
        return sqlite3.connect(database)

    @classmethod
    def query(cls,query, params=''):
        """
        :param query: query with ?
        :param params: list or tuple of params (replace ?)
        :return: list of object or null
        """
        # query = "SELECT * FROM Users WHERE `E-mail` =? and `password`=?"
        # params = list([login, password])

        query_result = list()
        conn = cls.connect_db()
        print('conntected')
        test = conn.execute(query)

        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        print(c)
        for row in c.execute(query, params):
            query_result.append(row)

        conn.commit()

        cls.close_db(conn)

        if query_result != []:
            return query_result

    @staticmethod
    def close_db(conn):
        conn.close()
