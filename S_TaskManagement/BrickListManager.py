import yaml
import threading

# Configurations
config = yaml.load(open("./Config.yaml", 'r'), Loader=yaml.FullLoader)

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
        db = DB('./S_RoboticArmControl/data.txt')
        (self.srcLayer, self.dstLayerList) = db.getData()

        # Block Reference Condition Variable
        self.cv = threading.Condition()

        # Initiation of Layer Information
        self.dstLayerIndex = 0
        self.dstCurrentLayer = self.dstLayerList[0]

    # -- Critical Section Ensured --
    ## For CITD III, We need an initial position info to seperate two trajectories.
    ## In CITD IV, We will try to generalize for more than three trajectories.
    def get_next_block_src(self, robot_obj):
        # Get Next Source Block based on Position Intormation from srcBricks
        # Termination Condition
        if (self.srcLayer.isLayerTasksDone() == True):
            # Tasks Completed, Returning None
            return -1

        # Searching by O(N)
        # Find the Nearest Block with Position Information
        minDist = 10000000.0
        minBlock = None

        # Getting Nearest Destination Brick
        for b in self.srcLayer.getEnableBrickList():
            ## Seperation of Target Blocks (Fixed For CITD III)
            ## TODO: getPos()[0] ?

            # Right Block Filtering
            if (robot_obj.getInitPos()[0] < self.srcLayer.getCenter()[0] and b.getPos()[0] > self.srcLayer.getCenter()[0]):
                continue
            # Left Block Filtering
            elif (robot_obj.getInitPos()[0] > self.srcLayer.getCenter()[0] and b.getPos()[0] < self.srcLayer.getCenter()[0]):
                continue

            if (minDist > b.getPos().calDist(robot_obj.getPos())):
                minDist = b.getPos().calDist(robot_obj.getPos())
                minBlock = b

        # Tasks Completed, Returning next destination block
        # If the robot needs to wait then returns None
        return minBlock

    ## For CITD III, We need an initial position info to seperate two trajectories.
    ## In CITD IV, We will try to generalize for more than three trajectories.
    def get_next_block_dest(self, robot_obj):
        # Get Next Destination Block based on Position Information
        # Termination Condition
        if (self.dstCurrentLayer.isLayerTasksDone() == True) :
            if (self.dstLayerIndex == len(self.dstLayerList) - 1) :
                # Tasks Completed, Returning None
                return -1
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
            ## Seperation of Target Blocks (Fixed For CITD III)
            ## TODO: getPos()[0] ?

            # Right Block Filtering
            if (robot_obj.getInitPos()[0] < self.dstCurrentLayer.getCenter()[0] and b.getPos()[0] > self.dstCurrentLayer.getCenter()[0]):
                continue
            # Left Block Filtering
            elif (robot_obj.getInitPos()[0] > self.dstCurrentLayer.getCenter()[0] and b.getPos()[0] < self.dstCurrentLayer.getCenter()[0]):
                continue

            if (minDist > b.getPos().calDist(robot_obj.getPos())) :
                minDist = b.getPos().calDist(robot_obj.getPos())
                minBlock = b

        # Tasks Completed, Returning next destination block
        # If the robot needs to wait then returns None
        return minBlock
    # -- Critical Section Ensured --

    def brick_move(self, robot_obj):
        self.cv.acquire()
        srcBrickSelected = self.get_next_block_src(robot_obj)
        if (srcBrickSelected == -1) :
            pass
        elif (not (srcBrickSelected == None)) :
            self.srcLayer.selectBrick(srcBrickSelected)
            robot_obj.brick_info_move(srcBrickSelected)
            self.cv.notify()
        else :
            # Wait until get_next_block_src is not None
            while (self.get_next_block_src(robot_obj) == None):
                self.cv.wait()

        self.cv.release()

    def brick_lift(self, robot_obj):
        self.cv.acquire()
        dstBrickSelected = self.get_next_block_dest(robot_obj)

        if (dstBrickSelected == -1) :
            pass
        elif (not (dstBrickSelected == None)) :
            self.dstCurrentLayer.selectBrick(dstBrickSelected)
            robot_obj.brick_info_lift(dstBrickSelected)
            self.cv.notify()
        else :
            # Wait until get_next_block_dst is not None
            while (self.get_next_block_src(robot_obj) == None):
                self.cv.wait()

        self.cv.release()

    def brick_comeback(self, robot_obj):
        self.cv.acquire()
        robot_obj.getOngoingBlock().done()
        # Enable Surrounding Blocks for SrcBlock
        self.srcLayer.setBrickAsDone(robot_obj.getOngoingBlock())

        robot_obj.brick_info_comeback()
        self.cv.release()

    def brick_fin(self, robot_obj):
        self.cv.acquire()
        # Enable Surrounding Blocks for DstBlock
        self.dstCurrentLayer.setBrickAsDone(robot_obj.getDstBlock())

        robot_obj.brick_info_fin()
        self.cv.release()
## -- Shared Objects (BrickListManager) --