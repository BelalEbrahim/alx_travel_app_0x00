import sqlite3

class DatabaseConnection:
    """Context manager for SQLite DB connections."""
    def __init__(self, db_path):
        self.db_path = db_path

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()


if __name__ == '__main__':
    # Use DatabaseConnection to fetch all users
    with DatabaseConnection('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        print(results)
