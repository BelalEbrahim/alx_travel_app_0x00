import time
import sqlite3
import functools
from db_connection import with_db_connection

def retry_on_failure(retries=3, delay=2):
    """Decorator to retry DB operations on failure."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(conn, *args, **kwargs):
            last_exc = None
            for attempt in range(1, retries+1):
                try:
                    return func(conn, *args, **kwargs)
                except Exception as e:
                    last_exc = e
                    print(f"[RETRY] Attempt {attempt} failed: {e}")
                    time.sleep(delay)
            raise last_exc
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

if __name__ == '__main__':
    users = fetch_users_with_retry()
    print(users)
