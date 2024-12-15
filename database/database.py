import sqlite3
from config import PATH

with sqlite3.connect(PATH) as db:
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tg_id INTEGER NOT NULL,
        first_name TEXT NOT NULL,
        username TEXT NOT NULL,
        money INTEGER,
        if_admin INTEGER
        )
        ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Cart (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        item TEXT NOT NULL,
        cost INTEGER
        )
        ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        item_id INTEGER NOT NULL,
        cost INTEGER,
        email TEXT NOT NULL,
        phone TEXT NOT NULL
        )
        ''')
    db.commit()

def registration(id, first_name, username):
    with sqlite3.connect(PATH) as db:
        cursor = db.cursor()
        cursor.execute('''SELECT * FROM Users WHERE username = ?''', (username,))
        users = cursor.fetchall()
        if len(users) == 0:
            data = (id, first_name, username, 0, 0)
            query = f'''INSERT INTO Users(tg_id, first_name, username, money, if_admin) VALUES (?,?,?,?,?)'''
            cursor.execute(query, data)
        db.commit()