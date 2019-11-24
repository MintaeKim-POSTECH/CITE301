from BrickListManager import BrickListManager
import yaml

# Configurations
config = yaml.load(open("../Config.yaml", 'r'), Loader=yaml.FullLoader)

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
            pass

        # Pop_front instruction
        robot_obj.pop_inst()
        return robot_obj.getCurrentInst()