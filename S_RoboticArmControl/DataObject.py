from S_RoboticArmControl.LayerModule import Layer
from S_RoboticArmControl.Elements import Position
from S_RoboticArmControl.BrickModule import Brick
import json

class DB:
    def __init__(self,fileName):
        self.fName=fileName
        self.srcBricks = []
        self.dstBricks = []
        self.srcLayerList = []
        self.dstLayerList = []

    def getData(self):
        with open(self.fName) as j:
            data = json.load(j)
        dataList = data["bricks"]

        for ob in dataList:
            p = Position()
            p.setPos(ob["point"])
            p.setDir(ob["dir"])
            b = Brick()
            b.pos = p
            if ob["src"]:
                b.src = True
                self.srcBricks.append(b)
            else:
                b.src = False
                self.dstBricks.append(b)

        self.srcBricks.sort()
        self.dstBricks.sort()

        h = 0.0
        l = Layer()
        for src in self.srcBricks:
            if abs(h - src.pos.pos[2]) > 1.0:
                self.srcLayerList.append(l)
                l = Layer()
                h = src.pos.pos[2]
            l.addBrick(src)

        h = 0.0
        l = Layer()
        for dst in self.dstBricks:
            if abs(h - dst.pos.pos[2]) > 1.0:
                self.dstLayerList.append(l)
                l = Layer()
                h = dst.pos.pos[2]
            l.addBrick(dst)

        # Calculation of Dst Layer Center
        for layer in self.srcLayerList :
            layer.calCenter()

        for lay in self.dstLayerList:
            lay.calCenter()

        return (self.scrLayer, self.dstlayerList)


    def compare(b1, b2):
        if b1.src:
             return b1.pos.upper(b2.pos)
        else:
             return not b1.pos.upper(b2.pos)
