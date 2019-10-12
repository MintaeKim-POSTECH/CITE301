from Elements import RobotPhase
from Elements import Position
import numpy as np
from BrickModule import Brick

class Robot:

    def __init__(self):
        self.phase = RobotPhase.STOP
        self.working = None
        self.next = None
        self.angles = [0.0, 0.0, 0.0]
        self.center = None

    def lift(self):
        self.calAngles()
        # communicate with robot arm
        self.center = self.working.src

    def move(self):
        # communicate with robot arm
        self.center = self.working.dst

    def calAngles(self):
        pass

