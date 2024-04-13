import sqlite3


class DataBase:
    def __init__(self):
        self.start_database()

    def start_database(self):
        with sqlite3.connect('user.sqlite') as db:
            cursor = db.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS user(
            login TEXT,
            password TEXT,
            v INT,
            n INT
            )""")


if __name__ == '__main__':
    DataBase()