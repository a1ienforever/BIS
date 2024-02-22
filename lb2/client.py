import pickle
import socket
from hashlib import md5
from argon2 import PasswordHasher


class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.HOST = (socket.gethostname(), 8080)
        self.client.connect(self.HOST)
        self.ph = PasswordHasher()

    def login(self):
        LOGIN = input("Введите логин: ")
        PASSWORD = input("Введите пароль: ")

    def hash(self, password):
        hashed_password = self.ph.hash(password)
        return hashed_password

    def sign_in(self):
        LOGIN = 'admin'
        PASSWORD = 'admin'
        hashed_pass = self.hash(PASSWORD.encode())
        print(hashed_pass.split('$'))
        self.client.send(pickle.dumps(('Sign in', LOGIN, hashed_pass)))


if __name__ == '__main__':
    client = Client()
    client.sign_in()
