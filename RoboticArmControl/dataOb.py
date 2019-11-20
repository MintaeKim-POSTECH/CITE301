from RoboticArmControl.LayerModule import Layer
from RoboticArmControl.Elements import Position
from RoboticArmControl.BrickModule import Brick
import json

class DB:
    def __init__(self,fileName):
        self.fName=fileName
        self.srcBricks = []
        self.dstBricks = []
        self.layerList=[]

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
        h = 0.0
        l = Layer()
        for dst in self.dstBricks:
            if abs(h - dst.pos.pos[2]) > 1.0:
                self.layerList.append(l)
                l = Layer()
                h = dst.pos.pos[2]
            l.addBrick(dst)

        def compare(b1, b2):
            if b1.src:
                return b1.pos.upper(b2.pos)
            else:
                return not b1.pos.upper(b2.pos)
        self.srcBricks.sort()
        self.dstBricks.sort()