import pygame, socket, sys, pickle, threading
from entity import *

class Client:
    def __init__(self, ip: str, port: int, login: str):
        self.ip = socket.gethostbyname(str(ip))
        self.port = int(port)
        self.login = login
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.entities = EntityHandler()
        self._connect()

    def _playerHandler(self):
        print("Starting")
        while True :
            self.entities.recvall(self.socket)

    def _connect(self):
        self.socket.connect((self.ip, self.port))
        self.socket.send(str.encode(self.login))
        if(self.socket.recv(1024).decode('utf-8') == 'F') :
            print("Connection FAILED")
        else:
            print("Connecition SUCCESSFULL")
            threading.Thread(self._playerHandler(),[])

cli = Client(sys.argv[1], sys.argv[2], sys.argv[3])