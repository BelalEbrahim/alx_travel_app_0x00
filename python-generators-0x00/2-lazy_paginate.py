#!/usr/bin/env python3
"""
Yield pages of users lazily.
"""
from seed import connect_to_prodev

def lazy_pagination(page_size):
    offset = 0
    while True:
        conn = connect_to_prodev()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT user_id, name, email, age FROM user_data LIMIT %s OFFSET %s",
            (page_size, offset)
        )
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        if not rows:
            break
        yield rows
        offset += page_size

if __name__ == '__main__':
    for page in lazy_pagination(100):
        for user in page:
            print(user)