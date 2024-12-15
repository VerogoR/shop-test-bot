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
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Catalog (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT NOT NULL,
        item_photo TEXT NOT NULL,
        item_price INTEGER NOT NULL,
        category TEXT NOT NULL
        )
        ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Category (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cat_name TEXT NOT NULL
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

def show_catalog(category):
    with sqlite3.connect(PATH) as db:
        cursor = db.cursor()
        cursor.execute('''SELECT * FROM Catalog WHERE category = ?''', (category))
        items = cursor.fetchall()
        return items;

def add_item(name, photo, price, category):
    with sqlite3.connect(PATH) as db:
        cursor = db.cursor()
        try:
            cursor.execute('BEGIN')
            cursor.execute('INSERT INTO Catalog (item_name, item_photo, item_price, category) VALUES (?, ?, ?, ?)',
                           (f'{name}', f'{photo}', f'{price}', f'{category}'))
            cursor.execute('COMMIT')
        except:
            cursor.execute('ROLLBACK')

def if_admin(user_id):
    with sqlite3.connect(PATH) as db:
        cursor = db.cursor()
        cursor.execute('''SELECT if_admin FROM Users WHERE tg_id = ?''', (user_id,))
        res = cursor.fetchall()
        return res;