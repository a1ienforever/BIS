import pickle
import random
import socket
import sqlite3
from hashlib import sha256


class Server:
    def __init__(self):
        self.HOST = (socket.gethostname(), 10000)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.max_size_msg = 100
        self.N = random.randint(0, 1000)
        self.A = 1

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
                conn.send(str(self.N).encode())
                login_and_password = pickle.loads(conn.recv(1024))
                print(login_and_password)
                method = login_and_password[0]
                login = login_and_password[1]
                hashed_password = login_and_password[2]
                if method == 'registration':
                    msg = self.registration(login, hashed_password)
                    conn.send(pickle.dumps(msg))
                elif method == 'sign in':
                    conn.send(pickle.dumps(self.A))

                    check_password = pickle.loads(conn.recv(1024))

                    hashed_password = self.recursion_hashing(check_password, self.A)
                    password_from_db = self.get_password_by_username(login)
                    print(hashed_password)
                    print(password_from_db)
                    if hashed_password == password_from_db:
                        conn.send(pickle.dumps('Authorization Successful'))
                        self.A += 1

                    else:
                        conn.send(pickle.dumps('Incorrect login or password'))
                    print(self.A)
            except Exception as e:
                print(e)

    def registration(self, login, password):
        self.add_db(login, password)
        return "Registration successful"

    def get_password_by_username(self, login):
        with sqlite3.connect('users.sqlite') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT password FROM users WHERE login=?", (login,))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return None

    def add_db(self, login, password):
        with sqlite3.connect('users.sqlite') as db:
            cursor = db.cursor()
            cursor.execute(f"SELECT login FROM users WHERE login = '{login}'")
            if cursor.fetchone() is None:
                cursor.execute(f"INSERT INTO users VALUES(?,?)",
                               (login, password))
                db.commit()
                print("Запись сделана!")

    def recursion_hashing(self, P, n, counter=0):
        if counter < int(n):
            counter += 1
            return self.recursion_hashing(sha256(P.encode()).hexdigest(), n, counter)
        return P

if __name__ == '__main__':
    Server()