import socket

HOST = ("localhost", 8080)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(HOST)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect(HOST)
        data = 'Hello'.encode()
        client.send(data)
        msg = client.recv(1024)
        print(msg.decode('UTF-8'))


def login():
    LOGIN = input("Введите логин: ")
    PASSWORD = input("Введите пароль: ")





def sign_in(login, password):
    pass


def hash_psw(password):
    pass
