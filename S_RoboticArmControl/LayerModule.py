import numpy as np
import yaml

from S_RoboticArmControl.Elements import Position as Pos
from S_RoboticArmControl.Elements import Phase

# Configurations
config = yaml.load(open("./Config.yaml", 'r'), Loader=yaml.FullLoader)

class Layer:
    def __init__(self):
        self.center = Pos()
        self.brickList = []

        self.readyList = []
        # In here, ongoing brick means bricks which is on-going
        # (hold - move - release - move to position near brick source)
        self.ongoingList = []
        self.stackedList = []

        self.diameter = 0.00

        self.phase = Phase.NULL

        self.processedBrickCnt = 0

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
        self.readyList.append(brick)

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

    # Mark brick as on-going
    def selectBrick(self, brick):
        brick.working()
        self.readyList.remove(brick)
        self.ongoingList.append(brick)
        for b in self.brickList:
            if (not b.pos.isEqual(brick.pos)) :
                if (b.getPhase() == Phase.ENABLE) :
                    if (b.getPos().calDist(brick.getPos()) < config["ROBOT_BODY_SIZE_MM"]) :
                        b.unable()

    # Mark brick as done
    def setBrickAsDone(self, brick):
        brick.done(brick)
        self.ongoingList.remove(brick)
        self.stackedList.append(brick)
        for b in self.brickList:
            if (not b.pos.isEqual(brick.pos)) :
                if (b.getPhase() == Phase.ENABLE) :
                    if (b.getPos().calDist(brick.getPos()) < config["ROBOT_BODY_SIZE_MM"]) :
                        b.enable()

    # Returns True if all tasks in this layer are done
    def isLayerTasksDone(self):
        return (len(self.brickList) == len(self.stackedList))

    def getStackedList(self):
        return self.stackedList

    def calRadius(self):
        new_pos = Pos()
        new_pos.setPos(self.calCenter())
        self.diameter=self.brickList[0].getPos().calDist(new_pos)

    def getRadius(self):
        return self.diameter

# test
'''

'''
