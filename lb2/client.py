import pickle
import random
import socket


class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.HOST = (socket.gethostname(), 8080)
        self.client.connect(self.HOST)
        self.sign_in()

    def login(self):
        LOGIN = input("Введите логин: ")
        PASSWORD = input("Введите пароль: ")

    def sign_in(self):
        LOGIN = 'admin'
        PASSWORD = 'qwerty'
        key = random.randint(0, 33)
        crypt_pass = self.encrypt(PASSWORD, key)
        print(crypt_pass)
        self.client.sendall(pickle.dumps(('Sign in', LOGIN, crypt_pass, key)))

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



if __name__ == '__main__':
    client = Client()
