import sqlite3


class DataBase:
    def __init__(self):
        self.start_database()

    def start_database(self):
        with sqlite3.connect('users.sqlite') as db:
            cursor = db.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS users(
            login TEXT,
            password TEXT
            )""")


if __name__ == '__main__':
    DataBase()