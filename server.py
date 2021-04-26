import pygame, socket, sys, pickle, threading
from entity import *

class Server:
    def __init__(self, ip, port):
        self.ip = socket.gethostbyname(ip)
        self.port = int(port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.entities = EntityHandler()
        self._startServer()

    def _playerHandler(self, conn, login, entities):
        while True:
            try:
                entities.sendActive(conn)
                entities.recvAll(conn)
            except:
                entities.get(login, "Player").logout()
                print(login + " has disconnected")
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
            key = conn.recv(1024).decode('utf-8')
            print("Attempting login to " + key)
            player = self.entities.get(key)
            if player != None :
                if player.active :
                    conn.send(str.encode('F'))
                    print("Login FAILED")
                else :
                    player.login()
                    player.randomColor()
                    conn.send(str.encode('S'))
                    print("Login SUCCESSFULL")
                    self._handlePlayer(conn, key)
            else :
                self.entities.add(Player(0, 0, (0,0,0), key))
                player = self.entities.get(key, "Player")
                if player != None :
                    player.login()
                    player.randomColor()
                conn.send(str.encode('S'))
                print("Login SUCCESSFULL")
                self._handlePlayer(conn, key)
            
    def _handlePlayer(self, conn, key):
        threading.Thread(target=self._playerHandler,args=(conn, key, self.entities)).start()

srv = Server(sys.argv[1], 8888)
