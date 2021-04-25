import socket, pickle

class EntityHandler:
    def __init__(self):
        self.enties = []

    def sendall(self, socket):
        socket.send(pickle.dumps(len(self.enties)))
        for entity in self.enties :
            socket.send(pickle.dumps(entity))

    def recvall(self, socket):
        entityCnt = pickle.loads(socket.recv(1024))
        print(entityCnt)
        if type(entityCnt) == int :
            for entity in range(entityCnt):
                self.enties.insert(entity, pickle.loads(socket.recv(2048)))

    def get(self, name):
        for entity in self.enties :
            if entity.name == name :
                return entity
        return None

    def add(self, entity):
        self.enties.append(entity)

class Entity:
    def __init__(self, x=0, y=0, color = (0,0,0), type = "None", name = "None"):
        self.x, self.y = x, y
        self.active = False
        self.color = color
        self.name = name
        self.type = type

    def _draw(self):
        pass

    def _update(self):
        pass

    def _activate(self):
        self.active = True

    def _deactivate(self):
        self.active = False

class Player(Entity):
    def __init__(self, x, y, color, name="None"):
        super().__init__(x, y, color, "Player", name)

    def _login(self):
        self._activate()