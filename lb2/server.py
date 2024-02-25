import base64
import hashlib
import os
import pickle
import socket
import sqlite3

from argon2 import PasswordHasher


class Server:
    def __init__(self):
        self.HOST = (socket.gethostname(), 8080)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.max_size_msg = 100
        self.ph = PasswordHasher()

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

                method = login_and_password[0]
                login = login_and_password[1]
                encrypt_password = login_and_password[2]
                key = login_and_password[3]
                password = self.descrypte(encrypt_password, key)

                if method == 'Sign in':
                    msg = self.sign_in(login, password).encode()
                    conn.send(msg)
                    print(msg)
                elif method == 'Log in':
                    msg = self.log_in(login, password).encode()
                    conn.send(msg)
                    print(msg)
            except Exception as e:
                print(f"Exception bind: {e}")



    def generate_salt(self):
        return base64.b64encode(os.urandom(16)).decode()

    def hash_with_salt(self, password, salt):
        password_salt = salt + password
        hashed_password = hashlib.sha256(password_salt.encode()).hexdigest()

        return hashed_password

    def add_db(self, login, password, salt):
        with sqlite3.connect('database.sqlite') as db:
            cursor = db.cursor()
            cursor.execute(f"SELECT login FROM users WHERE login = '{login}'")
            if cursor.fetchone() is None:
                cursor.execute(f"INSERT INTO users VALUES(?,?,?)",
                               (login, password, salt))
                db.commit()
                print("Запись сделана!")

    def get_user_by_username(self, login):
        with sqlite3.connect('database.sqlite') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT password, salt FROM users WHERE login=?", (login,))
            result = cursor.fetchone()
            if result:
                return result[0], result[1]
            else:
                return None


    def descrypte(self, ciphertext, shift):
        shift = -shift
        result = ""
        for char in ciphertext:
            if char.isalpha():
                shifted_char = chr(((ord(char.lower()) - 97 + shift) % 26) + 97)
                if char.isupper():
                    shifted_char = shifted_char.upper()
                result += shifted_char
            else:
                result += char
        return result

    def sign_in(self, login, password):
        salt = self.generate_salt()
        password = self.hash_with_salt(password, salt)
        self.add_db(login, password, salt)
        return "Registration successful"


    def log_in(self, login, password):
        password_check, salt = self.get_user_by_username(login)
        if self.hash_with_salt(password, salt) == password_check:
            return "successful authorization"
        else:
            return "Incorrect login or password"


if __name__ == '__main__':
    Server()
