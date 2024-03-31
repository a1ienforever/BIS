import pickle
import random
import socket
import sys
from hashlib import sha256
from Cryptodome.Util.number import *


class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.HOST = (socket.gethostname(), 10000)
        self.client.connect(self.HOST)
        self.t = 16
        self.n = 1055951207

        self.form()

    def registration(self):
        LOGIN = input("Введите логин: ")
        PASSWORD = input("Введите пароль: ")
        S = bytes_to_long(PASSWORD.encode())
        self.client.sendall(pickle.dumps(('registration', LOGIN, S)))


        msg = pickle.loads(self.client.recv(1024))
        print(msg)

    def sign_in(self):
        LOGIN = input("Введите логин: ")
        S_ = input("Введите пароль: ")
        S = bytes_to_long(S_.encode())
        self.client.sendall(pickle.dumps(('sign in', LOGIN, None)))
        n = pickle.loads(self.client.recv(1024))
        for i in range(self.t):
            r = random.randint(1, n - 1)
            x = pow(r, 2, n)
            self.client.sendall(pickle.dumps(x))

            e = pickle.loads(self.client.recv(1024))
            y = (r * (S ** e)) % n
            self.client.sendall(pickle.dumps(y))

        msg = pickle.loads(self.client.recv(1024))

        print(msg)

    def form(self):
        print("""1 - Registration
        2 - Authorization
        3 - exit""")
        choice = input("Choice: ")
        if choice == '1':
            self.registration()
        elif choice == '2':
            self.sign_in()
        elif choice == '3':
            sys.exit()
        else:
            print("Incorrect input, try again")
            self.form()


if __name__ == '__main__':
    Client()
