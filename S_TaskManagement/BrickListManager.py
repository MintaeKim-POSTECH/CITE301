import yaml
import threading

from S_RoboticArmControl.DataObject import DB
from S_RoboticArmControl.Elements import Phase

# Configurations
config = yaml.load(open("./Config.yaml", 'r'), Loader=yaml.FullLoader)

## -- Shared Objects (BrickListManager) --
# Shared Objects are often implemented by inner class, as an encapsulated models.
# Shared Objects are private to others.
# These shared objects must be modified by public methods in class.
# Refer to Operation System Class (CSED312)
class BrickListManager :
    def __init__(self):
        # Fetch Brick Lists by Database
        db = DB('./S_RoboticArmControl/data.txt')
        (self.srcLayerList, self.dstLayerList) = db.getData()

        # Block Reference Monitor
        self.monitor = threading.Condition()

        # Initiation of Src Layer Information
        self.srcLayerIndex = 0
        self.srcCurrentLayer = self.srcLayerList[0]

        # Initiation of Dst Layer Information
        self.dstLayerIndex = 0
        self.dstCurrentLayer = self.dstLayerList[0]

    # -- Critical Section Ensured --
    ## For CITD III, We need an initial position info to seperate two trajectories.
    ## In CITD IV, We will try to generalize for more than three trajectories.
    def get_next_block_src(self, robot_obj):
        # Get Next Source Block based on Position Information
        # Termination Condition
        if (self.srcCurrentLayer.isLayerTasksDone() == True):
            if (self.srcLayerIndex == len(self.srcLayerList) - 1):
                # Tasks Completed, Returning None
                return -1
            else:
                # Fetch the next layer
                self.srcCurrentLayer = self.srcLayerList[self.srcLayerIndex + 1]
                self.srcLayerIndex = self.srcLayerIndex + 1

        # Searching by O(N)
        # Find the Nearest Block with Position Information
        minDist = 10000000.0
        minBlock = None

        # Getting Nearest Destination Brick
        for b in self.srcCurrentLayer.getEnableBrickList():
            ## Seperation of Target Blocks (Fixed For CITD III)
            ## TODO: getPos()[0] ?

            # Right Block Filtering
            if (robot_obj.getInitPos()[0] < self.srcCurrentLayer.getCenter()[0] and b.getPos()[0] > self.srcCurrentLayer.getCenter()[0]):
                continue
            # Left Block Filtering
            elif (robot_obj.getInitPos()[0] > self.srcCurrentLayer.getCenter()[0] and b.getPos()[0] < self.srcCurrentLayer.getCenter()[0]):
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
        self.monitor.acquire()
        srcBrickSelected = self.get_next_block_src(robot_obj)
        if (srcBrickSelected == -1) :
            self.monitor.release()
            return False
        elif (not (srcBrickSelected == None)) :
            self.srcCurrentLayer.selectBrick(srcBrickSelected)
            robot_obj.brick_info_move(srcBrickSelected)
            self.monitor.notify()
        else :
            # Wait until get_next_block_src is not None
            while (self.get_next_block_src(robot_obj) == None):
                self.monitor.wait()

        self.monitor.release()
        return True

    def brick_lift(self, robot_obj):
        self.monitor.acquire()
        dstBrickSelected = self.get_next_block_dest(robot_obj)

        if (dstBrickSelected == -1) :
            self.monitor.release()
            return False
        elif (not (dstBrickSelected == None)) :
            self.dstCurrentLayer.selectBrick(dstBrickSelected)
            robot_obj.brick_info_lift(dstBrickSelected)
            self.monitor.notify()
        else :
            # Wait until get_next_block_dst is not None
            while (self.get_next_block_src(robot_obj) == None):
                self.monitor.wait()

        self.monitor.release()
        return True

    def brick_comeback(self, robot_obj):
        self.monitor.acquire()
        robot_obj.getOngoingBlock().done()
        # Enable Surrounding Blocks for SrcBlock
        self.srcCurrentLayer.setBrickAsDone(robot_obj.getOngoingBlock())

        robot_obj.brick_info_comeback()
        self.monitor.release()

    def brick_fin(self, robot_obj):
        self.monitor.acquire()
        # Enable Surrounding Blocks for DstBlock
        self.dstCurrentLayer.setBrickAsDone(robot_obj.getDstBlock())

        robot_obj.brick_info_fin()
        self.monitor.release()


    def get_progress_rate(self):
        self.monitor.acquire()
        bricks_done = 0
        bricks_total = 0
        for dstLayer in self.dstLayerList :
            for dstBrick in dstLayer.getBrickList() :
                bricks_total = bricks_total + 1
                if (dstBrick.getPhase() == Phase.DONE) :
                    bricks_done = bricks_done + 1
        self.monitor.release()
        return (int)(bricks_done * 100.0 / bricks_total)

## -- Shared Objects (BrickListManager) --