from BrickListManager import BrickListManager
from Instruction import Instruction
import yaml

# Configurations
config = yaml.load(open("./Config.yaml", 'r'), Loader=yaml.FullLoader)

# --- Import S_RoboticArmControl/RobotControl.py ---
import os
import sys

path_for_roboAC = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
path_for_roboAC = os.path.join(path_for_roboAC, 'S_RoboticArmControl')
sys.path.append(path_for_roboAC)

from RobotControl import Robot
# --- Import S_RoboticArmControl/RobotControl.py ---

# --- Import S_CameraVision/ImageManager.py & ImageDetection.py ---
path_for_CV = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
path_for_CV = os.path.join(path_for_CV, 'S_CameraVision')
sys.path.append(path_for_CV)

from ImageManager import ImageManager
from ImageDetection import updatePosition
# --- Import S_CameraVision/ImageManager.py & ImageDetection.py ---

class TaskManager :
    def __init__(self):
        self.brickListManager = BrickListManager()

    ## For CITD III, We need an initial position info to seperate two trajectories.
    ## In CITD IV, We will try to generalize for more than three trajectories.
    def fetchNextTask(self, robot_obj) :
        if (robot_obj.isQueueEmpty() == True) :
            # TODO: Push new Instructions for each robot_obj phase

            ## Usage :
            # new_inst_forward = Instruction('FORWARD', [(CALCULATED_MM / config["DEGREE_PER_MM_FORWARD"])])
            # new_inst_right = Instruction('RIGHT', [(CALCULATED_MM / config["DEGREE_PER_MM_RIGHT"])])
            # new_inst_rotate = Instruction('ROTATE', [(CALCULATED_DEGREE / config["DEGREE_PER_MM_ROTATE"])])
            # new_inst_arm = Instruction('ARM', [angle_1, angle_2, angle_3, state(0 or 1)]) (state 0 : grab, 1 : release)

            # robot_obj.push_inst(new_inst)
            # robot_obj.push_inst_list(new_inst_list)

            # TODO: Delete (Test Purpose Only)
            new_inst_forward = Instruction('FORWARD', [(50 / config["DEGREE_PER_MM_FORWARD"])])
            robot_obj.push_inst(new_inst_forward)

            pass

        # Pop_front instruction
        robot_obj.pop_inst()
        if (robot_obj.getCurrentInst() == None) :
            return ""
        return str(robot_obj.getCurrentInst())