import numpy as np, pygame

class PhysicsHandler:
    def __init__(self, gravity=[0,0]):
        self.gravity = np.array(gravity)

class Rigidbody:
    def __init__(self, mass=1, frictionFactor=0.5, position=[0,0], velocity=[0,0], acceleration=[0,0]):
        self.mass = mass
        self.frictionFactor = frictionFactor
        self.position = np.array(position)
        self.velocity = np.array(velocity)
        self.acceleration = np.array(acceleration)

        self.prevDeltaTime = 0

    def _update(self):
        time = pygame.time.get_ticks()
        deltaTime = (time - self.prevDeltaTime) / 1000
        self.prevDeltaTime = time
        self.acceleration = np.multiply(self.acceleration, deltaTime)
        self.velocity = np.divide(np.add(self.velocity, self.acceleration), self.mass)
        self.velocity = np.divide(np.subtract(self.velocity, np.multiply(np.multiply(self.velocity, self.frictionFactor), deltaTime)), self.mass)
        self.position = np.add(self.position, self.velocity)
        self.acceleration = np.multiply(self.acceleration, 0)

    def applyForce(self, force=[0,0]):
        self.acceleration = np.add(self.acceleration, np.array(force))