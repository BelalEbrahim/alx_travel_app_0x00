#!/usr/bin/env python3
"""
Lazy pagination: define `paginate_users` for fetching a page and `lazy_paginate` to yield pages on demand.
"""
from seed import connect_to_prodev

def paginate_users(page_size, offset):
    """Fetch a single page of users starting from offset."""
    conn = connect_to_prodev()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM user_data LIMIT %s OFFSET %s",
        (page_size, offset)
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


def lazy_paginate(page_size):
    """Yield lists of users lazily, fetching next page only when needed."""
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size

if __name__ == '__main__':
    for page in lazy_paginate(100):
        for user in page:
            print(user)