from Elements import RobotPhase
from LayerModule import Layer
from Elements import Position
import numpy as np
from BrickModule import Brick
import json

with open('data.txt') as j:
    data = json.load(j)

dataList = data["bricks"]
srcBricks = []
dstBricks = []

for ob in dataList:
    p = Position()
    p.setPos(ob["point"])
    p.setDir(ob["dir"])
    b = Brick()
    b.pos = p
    if ob["src"]:
        b.src = True
        srcBricks.append(b)
    else:
        b.src = False
        dstBricks.append(b)


def compare(b1, b2):
    if b1.src:
        return b1.pos.upper(b2.pos)
    else:
        return not b1.pos.upper(b2.pos)


srcBricks.sort()
dstBricks.sort()


layerList=[]
h=0.0
l=Layer()
for dst in dstBricks:
    if abs(h-dst.pos.pos[2])>1.0:
        layerList.append(l)
        l = Layer()
        h=dst.pos.pos[2]
    l.addBrick(dst)


#test
"""
print("Source")
for d in srcBricks:
    print(d.pos.pos)

print("Destination")
for d in dstBricks:
    print(d.pos.pos)

for layer in layerList:
    print(layer.calCenter())

"""



