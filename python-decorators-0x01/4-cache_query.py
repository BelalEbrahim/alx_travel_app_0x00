import sqlite3
import functools
from db_connection import with_db_connection

query_cache = {}

def cache_query(func):
    """Decorator that caches query results by SQL string."""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        query = kwargs.get('query') or (args[0] if args else None)
        if query in query_cache:
            print("[CACHE] Returning cached result")
            return query_cache[query]
        result = func(conn, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

if __name__ == '__main__':
    # First call (hits DB)
    users = fetch_users_with_cache(query="SELECT * FROM users")
    print(users)
    # Second call (cached)
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    print(users_again)
