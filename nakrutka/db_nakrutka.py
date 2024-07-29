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
    ''')
    users = cursor.fetchall()
    conn.close()
    return users

def get_user(user_id=None, authorization_header=None):
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()
    if user_id:
        cursor.execute('''
        SELECT * FROM user WHERE user_id = ?
        ''', (user_id,))
    elif authorization_header:
        cursor.execute('''
        SELECT * FROM user WHERE authorization_header = ?
        ''', (authorization_header,))
    user = cursor.fetchone()
    conn.close()
    return user

def delete_user(user_id=None, authorization_header=None):
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()
    if user_id:
        cursor.execute('''
        DELETE FROM user WHERE user_id = ?
        ''', (user_id,))
    elif authorization_header:
        cursor.execute('''
        DELETE FROM user WHERE authorization_header = ?
        ''', (authorization_header,))
    conn.commit()
    conn.close()

def update_user(user_id, new_user_id=None, new_authorization_header=None):
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()
    if new_user_id and new_authorization_header:
        cursor.execute('''
        UPDATE user SET user_id = ?, authorization_header = ? WHERE user_id = ?
        ''', (new_user_id, new_authorization_header, user_id))
    elif new_user_id:
        cursor.execute('''
        UPDATE user SET user_id = ? WHERE user_id = ?
        ''', (new_user_id, user_id))
    elif new_authorization_header:
        cursor.execute('''
        UPDATE user SET authorization_header = ? WHERE user_id = ?
        ''', (new_authorization_header, user_id))
    conn.commit()
    conn.close()


create_database()
