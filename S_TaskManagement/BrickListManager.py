import yaml
import threading

# Configurations
config = yaml.load(open("../Config.yaml", 'r'), Loader=yaml.FullLoader)

# --- Import S_RoboticArmControl/LayerModule.py, ... ---
import os
import sys

path_for_roboAC = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
path_for_roboAC = os.path.join(path_for_roboAC, 'S_RoboticArmControl')
sys.path.append(path_for_roboAC)

from LayerModule import Layer
from DataObject import DB
from BrickModule import Brick
import Elements
from RobotControl import Robot
# --- Import S_RoboticArmControl/LayerModule.py, ... ---

## -- Shared Objects (BrickListManager) --
# Shared Objects are often implemented by inner class, as an encapsulated models.
# Shared Objects are private to others.
# These shared objects must be modified by public methods in class.
# Refer to Operation System Class (CSED312)
class BrickListManager :
    def __init__(self):
        # Fetch Brick Lists by Database
        db = DB()
        (self.srcLayer, self.dstLayerList) = db.getData()

        # Block Reference Condition Variable
        self.cv = threading.Condition()

        # Initiation of Layer Information
        self.dstLayerIndex = 0
        self.dstCurrentLayer = self.dstLayerList[0]

    # -- Critical Section Ensured --
    def get_next_block_src(self, robot_pos):
        # TODO: Get Next Source Block based on Position Intormation from srcBricks

        pass

    def get_next_block_dest(self, robot_pos):
        # Get Next Destination Block based on Position Information
        # Termination Condition
        if (self.dstCurrentLayer.isLayerTasksDone() == True) :
            if (self.dstLayerIndex == len(self.dstLayerList) - 1) :
                # Tasks Completed, Returning Exit Code -2
                return -2
            else :
                # Fetch the next layer
                self.dstCurrentLayer = self.dstLayerList[self.dstLayerIndex + 1]
                self.dstLayerIndex = self.dstLayerIndex + 1

        # Searching by O(N)
        # Find the Nearest Block with Position Information
        minDist = 10000000.0
        minBlock = None

        # Getting Nearest Destination Brick
        for b in self.dstCurrentLayer.getEnableBrickList() :
            if (minDist > b.getPos().calDist(robot_pos)) :
                minDist = b.getPos().calDist(robot_pos)
                minBlock = b

        # Tasks Completed, Returning next destination block
        # If the robot needs to wait then returns None
        return minBlock
    # -- Critical Section Ensured --

    def select_block(self, robot_obj):
        self.cv.acquire()
        srcBrickSelected = self.get_next_block_src(robot_obj.getPos())

        if (not (srcBrickSelected == None)) :
            # TODO: Unable Surrounding Block if exists

            robot_obj.stop_src_decided(srcBrickSelected)
            self.cv.notify()
        else :
            # Wait until get_next_block_src is not None
            while (self.get_next_block_src(robot_obj.getPos()) == None):
                self.cv.wait()

        self.cv.release()

    def block_grabbed(self, robot_obj):
        self.cv.acquire()
        dstBrickSelected = self.get_next_block_dest(robot_obj.getPos())

        if (not (dstBrickSelected == None)) :
            self.dstCurrentLayer.selectBrick(dstBrickSelected)
            robot_obj.lifting_grabbed(dstBrickSelected)
            self.cv.notify()
        else :
            # Wait until get_next_block_dst is not None
            while (self.get_next_block_src(robot_obj.getPos()) == None):
                self.cv.wait()

        self.cv.release()

    def after_released(self, robot_obj):
        self.cv.acquire()
        robot_obj.getOngoingBlock().done()
        # TODO: Enable Surrounding Blocks

        self.dstCurrentLayer.setBrickAsDone(robot_obj.getDstBlock())
        robot_obj.stacking_released()
        self.cv.release()
## -- Shared Objects (BrickListManager) --