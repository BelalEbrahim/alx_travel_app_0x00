# Unittests and Integration Tests (0x03)

## Running Unit Tests

```bash
python3 -m unittest test_utils.py
python3 -m unittest test_client.py
````

## Project Requirements

* Ubuntu 18.04, Python 3.7+
* `parameterized` and `requests` installed

## Structure

* `utils.py`, `client.py`, `fixtures.py`: source modules
* `test_utils.py`, `test_client.py`: test suites

```(0x02)

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
