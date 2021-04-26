import socket, sys, pickle
from entity import *

class Client:
    def __init__(self, ip: str, port: int, login: str):
        self.ip = socket.gethostbyname(str(ip))
        self.port = int(port)
        self.login = login
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.entities = EntityHandler()
        self._connect()

    def frameBegin(self):
        self.entities.recvall(self.socket)
        
    def frameEnd(self):
        self.entities.sendme(self.socket, self.login, "Player")

    def _connect(self):
        self.socket.connect((self.ip, self.port))
        self.socket.send(str.encode(self.login))
        if(self.socket.recv(1024).decode('utf-8') == 'F') :
            print("Connection FAILED")
        else:
            print("Connecition SUCCESSFULL")