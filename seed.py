import mysql.connector
import csv
import uuid

# Use your dedicated user credentials
db_config = {
    'host': 'localhost',
    'user': 'proj_user',
    'password': 'YourStrongPassword',
    'database': 'ALX_prodev'
}

def connect_db():
    return mysql.connector.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password']
    )

def create_database(conn):
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    cursor.close()

def connect_to_prodev():
    return mysql.connector.connect(**db_config)

def create_table(conn):
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age INT NOT NULL,
            INDEX(user_id)
        ) ENGINE=InnoDB
        """
    )
    print("Table user_data created successfully")
    cursor.close()

def insert_data(conn, csv_path):
    cursor = conn.cursor()
    with open(csv_path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            uid = str(uuid.uuid4())
            cursor.execute(
                "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                (uid, row['name'], row['email'], int(row['age']))
            )
    conn.commit()
    cursor.close()

if __name__ == '__main__':
    # Step through seeding
    conn = connect_db()
    create_database(conn)
    conn.close()

    conn = connect_to_prodev()
    create_table(conn)
    insert_data(conn, 'data/user_data.csv')
    conn.close()
    print("Seeding complete.")