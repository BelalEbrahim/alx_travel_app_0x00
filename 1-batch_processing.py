#!/usr/bin/env python3
"""
Fetch users in batches and filter by age > 25.
"""
from seed import connect_to_prodev

def stream_users_in_batches(batch_size):
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
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                print(user)

if __name__ == '__main__':
    batch_processing(50)