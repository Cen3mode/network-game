import socket, pickle, random, pygame

class EntityHandler:
    def __init__(self, HEADERSIZE=10):
        self.entities = []
        self.HEADERSIZE = HEADERSIZE

    def sendMe(self, socket, name, type):
        me = [self.get(name, type)]
        if me != None :
            msg = pickle.dumps(me)
            msg = bytes(f"{len(msg):<{self.HEADERSIZE}}", "utf-8") + msg
            socket.sendall(msg)

    def sendAll(self, socket):
        msg = pickle.dumps(self.entities)
        msg = bytes(f"{len(msg):<{self.HEADERSIZE}}", "utf-8") + msg
        socket.sendall(msg)

    def sendActive(self, socket):
        active = []
        for entity in self.entities :
            if entity.active :
                active.append(entity)
        msg = pickle.dumps(active)
        msg = bytes(f"{len(msg):<{self.HEADERSIZE}}", "utf-8") + msg
        socket.sendall(msg)

    def sendChanged(self, socket):
        changed = []
        for entity in self.entities :
            if entity.changed :
                changed.append(entity)
        msg = pickle.dumps(changed)
        msg = bytes(f"{len(msg):<{self.HEADERSIZE}}", "utf-8") + msg
        socket.sendall(msg)

    def recvAll(self, socket):
        full_msg = b''
        new_msg = True
        while True:
            msg = socket.recv(16)
            if new_msg:
                msglen = int(msg[:self.HEADERSIZE])
                new_msg = False
        
            full_msg += msg

            if len(full_msg)-self.HEADERSIZE == msglen:
                decodedMsg = pickle.loads(full_msg[self.HEADERSIZE:])
                #if decodedMsg != None :
                for nEntity in decodedMsg :
                    nEntity.changed = False
                    searchResult = self.getIndex(nEntity.name, nEntity.type)
                    if searchResult != None :
                        self.entities[searchResult] = nEntity
                    else :
                        self.entities.append(nEntity)
                break

    def get(self, name="None", type="None"):
        for entity in self.entities :
            if entity.name == name and entity.type == type:
                return entity
        return None

    def getIndex(self, name="None", type="None"):
        for entityIndex in range(len(self.entities)) :
            if self.entities[entityIndex].name == name and self.entities[entityIndex].type == type:
                    return entityIndex
        return None

    def add(self, entity):
        self.entities.append(entity)

    def drawAll(self, surface):
        for entity in self.entities :
            entity._draw(surface)

    def updateAll(self, events = []):
        for entity in self.entities :
            entity._update(events)

    def updateMe(self, name, type="Player", events=[]):
        me = self.get(name, type)
        if me != None :
            me._update(events)

class Entity:
    def __init__(self, x=0, y=0, color = (0,0,0), type = "None", name = "None"):
        self.x, self.y = x, y
        self.active = False
        self.changed = True
        self.color = color
        self.name = name
        self.type = type

    def _draw(self, surface):
        if self.active :
            pass

    def _update(self, events):
        self.changed = False
        if self.active :
            pass

    def _activate(self):
        self.active = True

    def _deactivate(self):
        self.active = False

class Player(Entity):
    def __init__(self, x, y, color, name="None"):
        self.speed = 5
        super().__init__(x, y, color, "Player", name)

    def _draw(self, surface):
        super()._draw(surface)
        if self.active :
            pygame.draw.rect(surface, self.color, (self.x, self.y, 25, 25), 0)

    def _update(self, events):
        super()._update(events)
        if self.active :
            for event in events :
                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_RIGHT :
                        self.x += 5
                        self.changed = True
                    if event.key == pygame.K_LEFT :
                        self.x -= 5
                        self.changed = True
                    if event.key == pygame.K_UP :
                        self.y -= 5
                        self.changed = True
                    if event.key == pygame.K_DOWN :
                        self.y += 5
                        self.changed = True

    def login(self):
        super()._activate()

    def logout(self):
        super()._deactivate()

    def randomColor(self):
        self.color = [random.randrange(1,255), random.randrange(1,255), random.randrange(1,255)]