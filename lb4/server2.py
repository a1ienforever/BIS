import pickle
import random
import socket
import sqlite3
from hashlib import sha256
from Cryptodome.Util.number import *


class Server:
    def __init__(self):
        self.HOST = (socket.gethostname(), 10000)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.max_size_msg = 100



        try:
            self.server_socket.bind(self.HOST)
            print("Server started...")
        except Exception as e:
            print(f"Exception bind: {e}")
        self.server_socket.listen()
        while True:
            conn, addr = self.server_socket.accept()
            print(f"Connected client {addr}")
            try:
                login_and_password = pickle.loads(conn.recv(1024))
                print(login_and_password)
                method = login_and_password[0]
                login = login_and_password[1]
                password = login_and_password[2]
                if method == 'registration':
                    msg = self.registration(login, password)
                    conn.send(pickle.dumps(msg))
                elif method == 'sign in':
                    s, v, n = self.get_password_by_username(login)
                    conn.sendall(pickle.dumps(n))
                    print(s)
                    t = 16
                    count = 0

                    for i in range(t):
                        x = pickle.loads(conn.recv(1024))
                        e = random.randint(0, 1)
                        conn.sendall(pickle.dumps(e))

                        y = pickle.loads(conn.recv(1024))

                        if pow(y, 2, n) == (x * (v ** e)) % n:
                            print("Passed")
                            count += 1
                        else:
                            print("Failed")

                    if count == t:
                        conn.send(pickle.dumps('Authorization successful'))
                    else:
                        conn.send(pickle.dumps("Uncorrect login or password"))

            except Exception as e:
                print(e)

    def registration(self, login, password):
        p = getPrime(15)
        q = getPrime(15)

        n = p * q
        v = pow(password, 2, n)

        self.add_db(login, password, v, n)
        return "Registration successful"

    def get_password_by_username(self, login):
        with sqlite3.connect('users.sqlite') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT password, v, n FROM users WHERE login=?", (login,))
            result = cursor.fetchone()
            if result:
                return result
            else:
                return None

    def add_db(self, login, password, v, n):
        with sqlite3.connect('users.sqlite') as db:
            cursor = db.cursor()
            cursor.execute(f"SELECT login FROM users WHERE login = '{login}'")
            if cursor.fetchone() is None:
                cursor.execute(f"INSERT INTO users VALUES(?,?,?,?)",
                               (login, password, v, n))
                db.commit()
                print("Запись сделана!")


if __name__ == '__main__':
    Server()
