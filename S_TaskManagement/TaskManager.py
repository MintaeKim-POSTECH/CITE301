from BrickListManager import BrickListManager

# --- Import S_RoboticArmControl/RobotControl.py ---
import os
import sys

path_for_roboAC = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
path_for_roboAC = os.path.join(path_for_roboAC, 'S_RoboticArmControl')
sys.path.append(path_for_roboAC)

from RobotControl import Robot
# --- Import S_RoboticArmControl/RobotControl.py ---

# --- Import S_CameraVision/SaveImages ---
path_for_CV = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
path_for_CV = os.path.join(path_for_CV, 'S_CameraVision')
sys.path.append(path_for_CV)

import SaveImages
# --- Import S_CameraVision/SaveImages ---

class TaskManager :
    def fetchNextTask(robot_obj) :

        # TODO: Check if all tasks are done or not
        # TODO: Check if no blocks enabled (cannot access: then wait for seconds (with sleep))

        # TODO: pop_front instructions
        pass

    # TODO: Saving Position Information with CVs
    def updatePosition(robot_obj):
        pass
## -- Shared Objects (BrickListManager, Task Manager) --