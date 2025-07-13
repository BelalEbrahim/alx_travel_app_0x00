Python Decorators Project (0x01)

This single consolidated guide includes all Python code and step-by-step instructions to set up, implement, and run the python-decorators-0x01 project using SQLite and Python decorators in VS Code.

Directory Structure

python-decorators-0x01/
├── 0-log_queries.py
├── 1-with_db_connection.py
├── 2-transactional.py
├── 3-retry_on_failure.py
├── 4-cache_query.py
├── users.db         # SQLite database file
└── README.md

1. Prerequisites & Environment Setup

Install Python 3.8+: https://python.org

Install VS Code: https://code.visualstudio.com/

Create a virtual environment (optional but recommended):

python -m venv venv
.\venv\Scripts\activate

Ensure SQLite3 is available (bundled with Python on Windows).

Open the folder python-decorators-0x01 in VS Code.

2. Prepare the SQLite Database

In VS Code terminal, create users.db and a users table with sample data:

sqlite3 users.db

Inside the SQLite prompt:

CREATE TABLE users (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT NOT NULL
);
INSERT INTO users (name, email) VALUES
  ('Alice', 'alice@example.com'),
  ('Bob',   'bob@example.com');
.quit

Verify by running:

sqlite3 users.db "SELECT * FROM users;"

3. 0-log_queries.py

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

4. 1-with_db_connection.py

import sqlite3
import functools

def with_db_connection(func):
    """Decorator to open/close DB connection automatically."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

if __name__ == '__main__':
    user = get_user_by_id(user_id=1)
    print(user)

5. 2-transactional.py

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

6. 3-retry_on_failure.py

import time
import sqlite3
import functools
from 1-with_db_connection import with_db_connection

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

7. 4-cache_query.py

import sqlite3
import functools
from 1-with_db_connection import with_db_connection

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

8. README.md

# Python Decorators Project (0x01)

Master Python decorators to streamline SQLite database operations.

## Setup
1. Clone this folder in VS Code.
2. (Optional) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or .\\venv\\Scripts\\activate

Ensure users.db exists with a users table (see guide above).

Run each script:

python 0-log_queries.py
python 1-with_db_connection.py
python 2-transactional.py
python 3-retry_on_failure.py
python 4-cache_query.py

Each script contains its own __main__ demonstration. Customize and integrate decorators into larger applications as needed.

