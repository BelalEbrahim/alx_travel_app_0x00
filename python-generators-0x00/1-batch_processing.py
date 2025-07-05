#!/usr/bin/env python3
"""
Batch processing: stream users in batches and return a generator for users over 25.
"""
from seed import connect_to_prodev

def stream_users_in_batches(batch_size):
    """Yield lists of rows in batches."""
    conn = connect_to_prodev()
    cursor = conn.cursor(dictionary=True)
    offset = 0
    while True:
        cursor.execute(
            "SELECT user_id, name, email, age FROM user_data LIMIT %s OFFSET %s",
            (batch_size, offset)
        )
        batch = cursor.fetchall()
        if not batch:
            break
        yield batch
        offset += batch_size
    cursor.close()
    conn.close()

def batch_processing(batch_size):
    """Return a generator filtering users older than 25."""
    # Use return with a generator expression
    return (
        user
        for batch in stream_users_in_batches(batch_size)
        for user in batch
        if user['age'] > 25
    )

if __name__ == '__main__':
    for user in batch_processing(50):
        print(user)