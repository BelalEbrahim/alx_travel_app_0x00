# Python Context Managers & Async Operations (0x02)

This consolidated guide includes **all Python code** and **step-by-step instructions** to set up and run the **python-context-async-operations-0x02** project in **VS Code**. You'll implement class‐based context managers and asynchronous database queries with **SQLite**.

---

## Directory Structure

```
python-context-async-operations-0x02/
├── 0-databaseconnection.py
├── 1-execute.py
├── 3-concurrent.py
├── users.db          # SQLite database file with `users` table
└── README.md
```

---

## 1. Prerequisites & Environment Setup

1. **Install Python 3.8+**: [https://python.org](https://python.org)
2. **Install VS Code**: [https://code.visualstudio.com/](https://code.visualstudio.com/)
3. **Create (and activate) a virtual environment** (optional but recommended):

   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```
4. **Install `aiosqlite`** for async support:

   ```powershell
   pip install aiosqlite
   ```
5. **Ensure `users.db`** exists with a `users` table and sample data.

   In VS Code terminal:

   ```powershell
   sqlite3 users.db
   ```

   Then:

   ```sql
   CREATE TABLE users (
     id INTEGER PRIMARY KEY,
     name TEXT NOT NULL,
     age INTEGER NOT NULL
   );
   INSERT INTO users (name, age) VALUES
     ('Alice', 30), ('Bob', 45), ('Carol', 22);
   .quit
   ```

---

## 2. `0-databaseconnection.py`

```python
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
```

**Task 0**: Implements a class‐based context manager via `__enter__` and `__exit__`.

---

## 3. `1-execute.py`

```python
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
```

**Task 1**: A reusable query context manager combining connection handling and query execution.

---

## 4. `3-concurrent.py`

```python
import asyncio
import aiosqlite

async def async_fetch_users():
    async with aiosqlite.connect('users.db') as db:
        cursor = await db.execute("SELECT * FROM users")
        rows = await cursor.fetchall()
        await cursor.close()
        return rows

async def async_fetch_older_users():
    async with aiosqlite.connect('users.db') as db:
        cursor = await db.execute("SELECT * FROM users WHERE age > ?", (40,))
        rows = await cursor.fetchall()
        await cursor.close()
        return rows

async def fetch_concurrently():
    # Run both queries at once
    users, older = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    print('All users:', users)
    print('Users > 40:', older)

if __name__ == '__main__':
    asyncio.run(fetch_concurrently())
```

**Task 2**: Uses `asyncio` and `aiosqlite` to perform concurrent database queries with `asyncio.gather()`.

---

## 5. `README.md`

````markdown
# Python Context Managers & Async Operations (0x02)

**Project Duration**: Jul 7 – Jul 14 2025

Master Python context managers and asynchronous database operations:

## Setup Steps
1. Clone this directory into VS Code.
2. (Optional) Activate virtualenv: `venv\Scripts\activate`.
3. Install dependencies: `pip install aiosqlite`.
4. Ensure `users.db` has a `users` table (see instructions above).

## Running Tasks

- **Task 0** (Context Manager):
  ```bash
  python 0-databaseconnection.py
````

* **Task 1** (ExecuteQuery):

  ```bash
  python 1-execute.py
  ```

* **Task 2** (Async Queries):

  ```bash
  python 3-concurrent.py
  ```

## Manual QA Review

Request a manual QA review when all tasks run successfully. An auto-review will also run at the deadline (Jul 14 2025 01:00 AM).

```

---

**Ready for manual QA review** when you’ve verified each script’s output. Let me know if any adjustments are needed!  

```
