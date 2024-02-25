import base64
import os
import pickle
import socket


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
            login_and_password = pickle.loads(conn.recv(1024))

            method = login_and_password[0]
            login = login_and_password[1]
            encrypt_password = login_and_password[2]
            key = login_and_password[3]
            password = self.descrypte(encrypt_password, key)
            if method is 'Sign in':
                self.sign_in(login, password)
            elif method is 'Log in':
                self.log_in(login, password)


    def generate_salt(self):
        return base64.b64encode(os.urandom(16)).decode()

    def hash_with_salt(self, password):
        salt = self.generate_salt()
        hashed_password = self.ph.hash(salt + password)
        return hashed_password

    def add_db(self):
        pass

    # Дешифрование
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
        pass

    def log_in(self, login, password):
        pass


if __name__ == '__main__':
    Server()
