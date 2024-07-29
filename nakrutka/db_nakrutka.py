import sqlite3

def create_database():
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user (
        user_id TEXT PRIMARY KEY,
        authorization_header TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

def add_user(user_id, authorization_header):
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO user (user_id, authorization_header)
    VALUES (?, ?)
    ''', (user_id, authorization_header))
    conn.commit()
    conn.close()

def get_users():
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT * FROM user
    ''', ())
    user = cursor.fetchall()
    conn.close()
    return user



create_database()
