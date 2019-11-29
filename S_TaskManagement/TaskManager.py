from BrickListManager import BrickListManager
from Instruction import Instruction
import yaml
import numpy as np

# Configurations
config = yaml.load(open("./Config.yaml", 'r'), Loader=yaml.FullLoader)

# --- Import S_RoboticArmControl/RobotControl.py ---
import os
import sys

path_for_roboAC = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
path_for_roboAC = os.path.join(path_for_roboAC, 'S_RoboticArmControl')
sys.path.append(path_for_roboAC)
from RobotControl import Robot
from Elements import RobotPhase

# --- Import S_RoboticArmControl/RobotControl.py ---

# --- Import S_CameraVision/ImageManager.py & ImageDetection.py ---
path_for_CV = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
path_for_CV = os.path.join(path_for_CV, 'S_CameraVision')
sys.path.append(path_for_CV)

from ImageManager import ImageManager
from ImageDetection import updatePosition
# --- Import S_CameraVision/ImageManager.py & ImageDetection.py ---

class TaskManager :
    def __init__(self) :
        self.brickListManager = BrickListManager()

    # TODO: Push initial Instructions which moves robot to initial position.
    def pushInitialInstruction(self, robot_obj):
        cur_pos = robot_obj.getPos()
        init_pos = robot_obj.getInitPos() # Elemets.Position Object
        init_instList=[]
        init_instList.append(Instruction('FORWARD',[init_pos[1]-cur_pos[1]]))
        init_instList.append( Instruction('RIGHT', [init_pos[0] - cur_pos[0]]))
        robot_obj.push_inst_list(init_instList)


    ## For CITD III, We need an initial position info to seperate two trajectories.
    ## In CITD IV, We will try to generalize for more than three trajectories.
    def fetchNextTask(self, robot_obj) :
        instList=[]
        if (robot_obj.isQueueEmpty() == True) :
            # TODO: Push new Instructions for each robot_obj phase

            if(robot_obj.phase==RobotPhase.STOP):
                success = self.brickListManager.brick_move(robot_obj)
                if (success == True) :
                    # TODO: move
                    pass
                else :
                    pass
                    robot_obj.getOngoingBlock
                    robot_obj.getDstBl
            elif (robot_obj.phase == RobotPhase.MOVING):
                success = self.brickListManager.brick_lift(robot_obj)
                if (success == True) :
                    # TODO: move
                    pass
                else :
                    pass
            elif (robot_obj.phase == RobotPhase.LIFTING):
                success = self.brickListManager.brick_comeback(robot_obj)
                if (success == True) :
                    # TODO: move
                    pass
                else :
                    pass
            elif (robot_obj.phase == RobotPhase.COMEBACK):
                success=self.brickListManager.brick_fin()
                if (success == True) :
                    # TODO: move
                    pass
                else :
                    pass
            else :
                pass

            center=self.brickListManager.srcCurrentLayer.center
            brickDomain=brickArea(robot_obj.getPos(),robot_obj.center)
            if(brickDomain==1):

            elif(brickDomain==2):

            elif(brickDomain==3):

            else:

            ## Usage :
            # new_inst_forward = Instruction('FORWARD', [(CALCULATED_MM * config["DEGREE_PER_MM_FORWARD"])])
            # new_inst_right = Instruction('RIGHT', [(CALCULATED_MM * config["DEGREE_PER_MM_RIGHT"])])
            # new_inst_rotate = Instruction('ROTATE', [(CALCULATED_DEGREE * config["DEGREE_PER_MM_ROTATE"])])
            # new_inst_arm = Instruction('ARM', [angle_1, angle_2, angle_3, state(0 or 1)]) (state 0 : grab, 1 : release)

            # Want to Fetch Src and Dst Brick Processing? -> robot_obj.getOngoingBlock() , robot_obj.getDstBlock()

             robot_obj.push_inst(new_inst)
            # robot_obj.push_inst_list(new_inst_list)

            # TODO: Delete (Test Purpose Only)
            new_inst_forward = Instruction('FORWARD', [(50 * config["DEGREE_PER_MM_FORWARD"])])
            robot_obj.push_inst(new_inst_forward)

            pass

        # Pop_front instruction
        robot_obj.pop_inst()
        if (robot_obj.getCurrentInst() == None) :
            return ""

        return str(robot_obj.getCurrentInst())

#Returns the domian of brick
#   1 2
#   3 4
def brickArea(pos,center):
    if(pos.upper(center)):
        if(pos.pos[0]<center.pos[0]):
            return 3
        else:
            return 4
    else:
        if(pos.pos[0]>center.pos[0]):
            return 2
        else:
            return 1
def calPositionForRotation(brick):
        ret = brick.getPos() + brick.getPos().getDir() * config['ROBOT_ROTATING_DIAMETER']
        return ret

def move(manager,robotobj,pos,center):
    dir=np.array([1.0, 0.0, 0.0])
    if(robotobj.)
    instList=[]

    if()


