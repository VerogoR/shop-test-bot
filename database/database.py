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
        cost INTEGER,
        num INTEGER
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

def show_catalog(*category):
    with sqlite3.connect(PATH) as db:
        cursor = db.cursor()
        if len(category) >= 1:
            cursor.execute('''SELECT * FROM Catalog WHERE category = ?''', (category))
        else:
            cursor.execute('''SELECT * FROM Catalog''')
        items = cursor.fetchall()
        db.commit()
        return items

def add_item(name, photo, price, category):
    with sqlite3.connect(PATH) as db:
        cursor = db.cursor()
        try:
            cursor.execute('BEGIN')
            cursor.execute('INSERT INTO Catalog (item_name, item_photo, item_price, category) VALUES (?, ?, ?, ?)',
                           (f'{name}', f'{photo}', int(f'{price}'), f'{category}'))
            cursor.execute('COMMIT')
        except:
            cursor.execute('ROLLBACK')
        db.commit()

def if_admin(user_id):
    with sqlite3.connect(PATH) as db:
        cursor = db.cursor()
        cursor.execute('''SELECT if_admin FROM Users WHERE tg_id = ?''', (user_id,))
        res = cursor.fetchall()
        db.commit()
        return res

def add_to_cart_db(user_id, item_name, item_price):
    with sqlite3.connect(PATH) as db:
        cursor = db.cursor()
        cursor.execute('''SELECT * FROM Catalog WHERE item_name = ?''', (str(item_name),))
        res = cursor.fetchall()
        item_id = res[0][0]
        cursor.execute('''SELECT * FROM Cart WHERE item = ?''', (str(item_id),))
        res2 = cursor.fetchall()
        if res2:
            num_of_item = res2[0][4]
        else:
            num_of_item = 0
        if num_of_item != 0:
            cursor.execute('''UPDATE Cart SET num = ? WHERE item = ?''', (num_of_item + 1, item_id))
            # cursor.execute('''INSERT INTO Cart (user_id, item, cost, num) VALUES (?, ?, ?)''',
            #                (user_id, item_id, item_price, num_of_item + 1))
        else:
            cursor.execute('''INSERT INTO Cart (user_id, item, cost, num) VALUES (?, ?, ?, ?)''',
                           (user_id, item_id, item_price, 1))
        db.commit()

def show_cart_db(user_id):
    with sqlite3.connect(PATH) as db:
        cursor = db.cursor()
        cursor.execute('''SELECT * FROM Cart WHERE user_id = ?''', (user_id,))
        res = cursor.fetchall()
        db.commit()
        return res

def get_item_db(item_id):
    with sqlite3.connect(PATH) as db:
        cursor = db.cursor()
        cursor.execute('''SELECT * FROM Catalog WHERE id = ?''', (item_id,))
        res = cursor.fetchall()
        db.commit()
        return res

def clear_cart_db(user_id):
    with sqlite3.connect(PATH) as db:
        cursor = db.cursor()
        cursor.execute('''DELETE FROM Cart WHERE user_id = ?''', (user_id,))
        db.commit()