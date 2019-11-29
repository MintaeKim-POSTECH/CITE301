from S_RoboticArmControl.LayerModule import Layer
from S_RoboticArmControl.BrickModule import Brick
import numpy as np
from S_RoboticArmControl.DataObject import DB

'''
#Layer Test
layer = Layer()

for i in range(10):
    tmp = Brick()
    tmp.pos.setPos(np.array([float(i), 0.0, 0.0]))
    layer.addBrick(tmp)
'''

#DB Test
db=DB("data.txt")
db.getData()

print("Source")
for d in db.srcLayerList:
    for brick in d:
        print(brick.pos.pos)

print("DST")
for d in db.dstLayerList:
    for brick in d:
        print(brick.pos.pos)
