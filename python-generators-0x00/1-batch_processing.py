#!/usr/bin/env python3
"""
Fetch users in batches and filter by age > 25 using generators.
"""
from seed import connect_to_prodev

def stream_users_in_batches(batch_size):
    """Yield successive batches of users from the database."""
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
    """Generator: yield users older than 25 by streaming in batches."""
    for batch in stream_users_in_batches(batch_size):  # loop 1
        for user in batch:  # loop 2
            if user['age'] > 25:
                yield user  # use yield instead of print

if __name__ == '__main__':
    # Example usage: print users >25 in batches of 50
    for user in batch_processing(50):
        print(user)