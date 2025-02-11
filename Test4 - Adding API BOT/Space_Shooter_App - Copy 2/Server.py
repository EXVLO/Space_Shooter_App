import socket

class Server:
    def __init__(self):
        self.server_host = "localhost"
        self.server_port = 12345

        # Create a socket object
        self.serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)