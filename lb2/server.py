import socket

class Server:
    def __init__(self):
        self.HOST = (socket.gethostname(), 8080)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.max_size_msg = 100
        try:
            self.server_socket.bind(self.HOST)
        except Exception as e:
            print(f"Exception bind: {e}")
        self.server_socket.listen(10)
        while True:
            conn, addr = self.server_socket.accept()
            print(f"Connected client {addr}")





def generate_salt():
    pass


if __name__ == '__main__':
    Server()