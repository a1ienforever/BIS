import os
import pickle
import random
import socket
import sys


class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.HOST = (socket.gethostname(), 8080)
        self.client.connect(self.HOST)
        self.key = random.randint(0, 33)

        self.form()
        msg = self.client.recv(1024).decode()
        print(msg)

    def sign_in(self):
        LOGIN = input("Введите логин: ")
        PASSWORD = input("Введите пароль: ")
        encrypt_password = self.encrypt(PASSWORD, self.key)
        self.client.sendall(pickle.dumps(('Log in', LOGIN, encrypt_password, self.key)))

    def registration(self):
        LOGIN = input("Введите логин: ")
        PASSWORD = input("Введите пароль: ")
        crypt_pass = self.encrypt(PASSWORD, self.key)
        self.client.sendall(pickle.dumps(('Sign in', LOGIN, crypt_pass, self.key)))


    def encrypt(self, text, shift):
        result = ""
        for char in text:
            if char.isalpha():
                shifted_char = chr(((ord(char.lower()) - 97 + shift) % 26) + 97)
                if char.isupper():
                    shifted_char = shifted_char.upper()
                result += shifted_char
            else:
                result += char
        return result

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
