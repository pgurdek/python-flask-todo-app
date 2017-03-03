import sqlite3


class Database():
    def connect_db(DATABASE_NAME='../db.sqlite'):
        return sqlite3.connect(DATABASE_NAME)

    def query(query, params=''):
        """
        :param query: query with ?
        :param params: list or tuple of params (replace ?)
        :return: list of object or null
        """
        # query = "SELECT * FROM Users WHERE `E-mail` =? and `password`=?"
        # params = list([login, password])

        query_result = list()
        conn = connect_db()
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        for row in c.execute(query, params):
            query_result.append(row)

        conn.commit()

        close_db(conn)

        if query_result != []:
            return query_result

    def close_db(conn):
        conn.close()
