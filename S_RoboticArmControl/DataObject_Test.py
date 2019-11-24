from S_RoboticArmControl.LayerModule import Layer
from S_RoboticArmControl.Elements import Position
from S_RoboticArmControl.BrickModule import Brick
import numpy as np
from S_RoboticArmControl.DataObject import DB


#Layer Test
layer = Layer()

for i in range(10):
    tmp = Brick()
    tmp.pos.setPos(np.array([float(i), 0.0, 0.0]))
    layer.addBrick(tmp)


#DB Test
db=DB("data.txt")
db.getData()

print("Source")
for d in db.srcBricks:
    print(d.pos.pos)

print("Destination")
for d in db.dstBricks:
    print(d.pos.pos)

for layer in db.layerList:
    print(layer.calCenter())
