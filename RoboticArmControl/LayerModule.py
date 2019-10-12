import numpy as np
from BrickModule import Brick
from Elements import Position as Pos
from Elements import Phase

class Layer:
    def __init__(self):
        self.center = Pos()
        self.brickList = []
        self.stackedList = []
        self.phase = Phase.NULL

    def calCenter(self):
        cen = np.array([0.0, 0.0, 0.0])
        for brc in self.brickList:
            pos = brc.pos.getPos()
            cen = cen + pos
        cen = cen / len(self.brickList)
        for i in range(3):
            if abs(cen[i])<0.0001:
                cen[i]=0.0
        self.center = cen
        return cen

    def getCenter(self):
        return self.center

    def addBrick(self, brick):
        self.brickList.append(brick)

    def setBrickList(self, bList):
        self.brickList = bList

    def getBrickList(self):
        return self.brickList

    def getEnableBrickList(self):
        bList = []
        for b in self.brickList:
            if b.getPhase() == Phase.ENABLE:
                bList.append(b)
        return bList

    def stackBrick(self, brick):
        for b in self.brickList:
            if b.pos.isEqual(brick.pos):
                self.stackedList.append(b)
                self.brickList.remove(b)
                b.done()
                return True
        return False

    def getStackedList(self):
        return self.stackedList


# test

layer = Layer()

for i in range(10):
    tmp = Brick()
    tmp.pos.setPos(np.array([float(i), 0.0, 0.0]))
    layer.addBrick(tmp)

print(len(layer.brickList))

for i in range(10):
    print(layer.brickList[i].pos.getPos())

print(layer.calCenter())

b = Brick()
b.pos.setPos(np.array([1.0, 0.0, 0.0]))
layer.stackBrick(b)
b.pos.setPos(np.array([2.0, 0.0, 0.0]))
layer.stackBrick(b)

print(len(layer.brickList))
print(layer.calCenter())
print(len(layer.stackedList))
