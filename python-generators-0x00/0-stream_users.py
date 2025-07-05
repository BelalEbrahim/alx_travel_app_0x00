#!/usr/bin/env python3
"""
Yield one user record at a time.
"""
from seed import connect_to_prodev

def stream_users():
    conn = connect_to_prodev()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT user_id, name, email, age FROM user_data")
    for row in cursor:
        yield row
    cursor.close()
    conn.close()