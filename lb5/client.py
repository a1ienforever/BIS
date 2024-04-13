import pickle
import random
import socket


class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.HOST = (socket.gethostname(), 10000)
        self.client.connect(self.HOST)
        self.g = 5
        self.p = 23
        self.a = random.randint(1, 10)
        while True:
            self.send_msg()

    def send_msg(self):
        msg = input('Введите сообщение: ')
        public_key = self.create_public_key()
        self.client.sendall(pickle.dumps(public_key))
        server_pk = pickle.loads(self.client.recv(1024))
        s = self.create_secret_key(server_pk)
        encrypted_msg = self.encrypt(msg, s)
        print("Зашифрованное сообщение:", encrypted_msg)
        self.client.sendall(pickle.dumps(encrypted_msg))

    def create_public_key(self):
        public_key = pow(self.g, self.a, self.p)
        return public_key  # 8

    def create_secret_key(self, server_pk):
        s = pow(server_pk, self.a, self.p)
        return s

    # Шифр Вернама
    def encrypt(self, message, key):
        encrypted_message = ""
        for char in message:
            encrypted_char = chr((ord(char) + key) % 256)  # Применяем ключ к каждому символу сообщения
            encrypted_message += encrypted_char
        return encrypted_message


if __name__ == '__main__':
    Client()
