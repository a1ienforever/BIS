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
        self.g = 5
        self.p = 23
        self.b = 9


        try:
            self.server_socket.bind(self.HOST)
            print("Server started...")
        except Exception as e:
            print(f"Exception bind: {e}")
        self.server_socket.listen()
        while True:
            self.conn, addr = self.server_socket.accept()
            print(f"Connected client {addr}")
            try:
                while True:
                    self.msg_handler()
            except Exception as e:
                print(e)

    def msg_handler(self):
        client_pk = pickle.loads(self.conn.recv(1024))
        public_key = self.create_public_key()
        self.conn.sendall(pickle.dumps(public_key))
        s = self.create_secret_key(client_pk)
        print(s)
        encrypted_msg = pickle.loads(self.conn.recv(1024))
        msg = self.decrypt(encrypted_msg, s)
        print("Зашифрованное сообщение:", encrypted_msg)
        print("Расшифрованное сообщение:", msg)

    def create_public_key(self):
        # a = random.randint(0,10)

        public_key = pow(self.g, self.b, self.p)
        return public_key  # 11

    def create_secret_key(self, client_pk):
        s = pow(client_pk, self.b, self.p)
        return s

    def decrypt(self, encrypted_message, key):
        decrypted_message = ""
        for char in encrypted_message:
            decrypted_char = chr((ord(char) - key) % 1024)  # Расшифровываем сообщение, вычитая ключ
            decrypted_message += decrypted_char
        return decrypted_message


if __name__ == '__main__':
    Server()
