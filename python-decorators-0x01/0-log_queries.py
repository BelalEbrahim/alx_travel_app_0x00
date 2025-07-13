import sqlite3
import functools
import time

def log_queries(func):
    """Decorator that logs SQL queries before execution."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get('query') or (args[1] if len(args) > 1 else None)
        print(f"[LOG] Executing query: {query}")
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"[LOG] Query executed in {elapsed:.4f}s")
        return result
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

if __name__ == '__main__':
    users = fetch_all_users(query="SELECT * FROM users")
    print(users)
