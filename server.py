import pygame, socket, sys, pickle, threading
from entity import *

class Server:
    def __init__(self):
        self.ip = socket.gethostbyname(sys.argv[1])
        self.port = int(sys.argv[2])
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.entities = EntityHandler()
        self._startServer()

    def _playerHandler(self, conn, login):
        while True:
            try:
                self.entities.sendall(conn)
            except:
                break
        conn.close()

    def _startServer(self):
        try:
            self.socket.bind((self.ip, self.port))
        except socket.error as e:
            print(str(e))
        
        self.socket.listen(2)
        print("Waiting for connections...")

        while True:
            conn, addr = self.socket.accept()
            print("Connection received from: ", addr)
            print("Attempting login...")
            key = conn.recv(1024).decode('utf-8')
            player = self.entities.get(key)
            if player != None :
                if player.active :
                    conn.send(str.encode('F'))
                    print("Login FAILED")
                else :
                    player._login()
                    conn.send(str.encode('S'))
                    print("Login SUCCESSFULL")
                    threading.Thread(self._playerHandler, (conn, key)).run()
            else :
                self.entities.add(Player(0, 0, (0,0,0), key))
                self.entities.get(key)._login()
                conn.send(str.encode('S'))
                print("Login SUCCESSFULL")
                threading.Thread(self._playerHandler, (conn, key)).run()
            

srv = Server()
