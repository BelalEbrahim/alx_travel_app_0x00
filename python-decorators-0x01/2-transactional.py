import sqlite3
import functools
from 1-with_db_connection import with_db_connection

def transactional(func):
    """Decorator that wraps DB operations in a transaction."""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            return result
        except Exception:
            conn.rollback()
            raise
    return wrapper

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET email = ? WHERE id = ?",
        (new_email, user_id)
    )

if __name__ == '__main__':
    update_user_email(user_id=1, new_email='alice@newdomain.com')
    print("Email updated.")
