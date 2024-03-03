import pickle
import random
import socket
import sys
from hashlib import sha256


class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.HOST = (socket.gethostname(), 10000)
        self.client.connect(self.HOST)

        self.N = int(self.client.recv(1024).decode())
        self.A = None

        self.form()

    def registration(self):
        LOGIN = input("Введите логин: ")
        PASSWORD = input("Введите пароль: ")

        hashed_password = self.recursion_hashing(PASSWORD, self.N)
        self.client.sendall(pickle.dumps(('registration', LOGIN, hashed_password)))

        msg = pickle.loads(self.client.recv(1024))
        print(msg)

    def sign_in(self):
        LOGIN = input("Введите логин: ")
        P = input("Введите пароль: ")
        self.client.sendall(pickle.dumps(('sign in', LOGIN, None)))

        self.A = int(pickle.loads(self.client.recv(1024)))
        print(self.A)
        check_password = self.recursion_hashing(P, self.N - self.A)
        self.client.sendall(pickle.dumps(check_password))

        msg = pickle.loads(self.client.recv(1024))
        print(msg)



    def recursion_hashing(self, P, n, counter=0):
        if counter < n:
            counter += 1
            return self.recursion_hashing(sha256(P.encode()).hexdigest(), n, counter)
        return P
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