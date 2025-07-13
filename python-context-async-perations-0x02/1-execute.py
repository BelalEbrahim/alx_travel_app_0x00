import sqlite3

class ExecuteQuery:
    """Context manager that executes a SQL query and returns results."""
    def __init__(self, db_path, query, params=()):
        self.db_path = db_path
        self.query = query
        self.params = params

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        return self.cursor.fetchall()

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()


if __name__ == '__main__':
    # Fetch users older than 25 using ExecuteQuery
    with ExecuteQuery('users.db', "SELECT * FROM users WHERE age > ?", (25,)) as results:
        print(results)
