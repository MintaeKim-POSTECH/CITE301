import numpy as np
from enum import Enum


class Phase(Enum):
    NULL = 0
    ENABLE = 1
    UNABLE = 2
    WORKING = 3
    DONE = 4


class RobotPhase(Enum):
    STOP = 0
    MOVING = 1
    LIFTING = 2
    STACKING = 3


class Position:
    def __init__(self):
        self.pos = np.array([0.0, 0.0, 0.0])
        self.dir = np.array([1.0, 0.0, 0.0])

    def setPos(self, pos):
        for i in range(3):
            self.pos[i] = pos[i]

    def setDir(self, dir):
        for i in range(3):
            self.dir[i] = dir[i]

    def getPos(self):
        return self.pos

    def getDir(self):
        return self.dir

    def isEqual(self, b):
        return np.array_equal(self.pos, b.pos)

    def calDist(self, other):
        return sum((self.pos - other.pos) ** 2.0) ** (1 / 2)

    def upper(self, p):
        for i in range(3):
            if self.pos[2 - i] > p.pos[2 - i]:
                return True
            if self.pos[2-i]<p.pos[2-i]:
                return False

        return False
