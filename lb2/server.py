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
        self.server_socket.listen(10)
        while True:
            conn, addr = self.server_socket.accept()
            print(f"Connected client {addr}")
            login_and_password = pickle.loads(conn.recv(1024))
            salt = self.hash_with_salt(login_and_password[2])
            print(salt)

    def generate_salt(self):
        return base64.b64encode(os.urandom(16)).decode()

    def hash_with_salt(self, password):
        salt = self.generate_salt()
        hashed_password = self.ph.hash(salt + password)
        return hashed_password



    def add_db(self):
        pass


if __name__ == '__main__':
    Server()
