import yaml
from PyQt5 import QtCore

from S_TaskManagement.BrickListManager import BrickListManager
from S_TaskManagement.Instruction import Instruction
from S_RoboticArmControl.RobotControl import Robot

# Configurations
config = yaml.load(open("./Config.yaml", 'r'), Loader=yaml.FullLoader)

class TaskManager (QtCore.QObject) :
    updated_robot_info_conn = QtCore.pyqtSignal(Robot)
    updated_progress = QtCore.pyqtSignal(BrickListManager)

    def __init__(self, parent):
        super(TaskManager, self).__init__(parent)
        self.brickListManager = BrickListManager()

    # TODO: Push initial Instructions which moves robot to initial position.
    def pushInitialInstruction(self, robot_obj):

        # Update of Robot Information (While Connection)
        self.updated_robot_info_conn.emit(robot_obj)
        pass

    ## For CITD III, We need an initial position info to seperate two trajectories.
    ## In CITD IV, We will try to generalize for more than three trajectories.
    def fetchNextTask(self, robot_obj) :
        if (robot_obj.isQueueEmpty() == True) :
            # TODO: Push new Instructions for each robot_obj phase

            ## Usage :
            # new_inst_forward = Instruction('FORWARD', [(CALCULATED_MM * config["DEGREE_PER_MM_FORWARD"])])
            # new_inst_right = Instruction('RIGHT', [(CALCULATED_MM * config["DEGREE_PER_MM_RIGHT"])])
            # new_inst_rotate = Instruction('ROTATE', [(CALCULATED_DEGREE * config["DEGREE_PER_MM_ROTATE"])])
            # new_inst_arm = Instruction('ARM', [angle_1, angle_2, angle_3, state(0 or 1)]) (state 0 : grab, 1 : release)

            # success = self.brickListManager.brick_move(robot_obj)
            # success = self.brickListManager.brick_lift(robot_obj)
            # self.brickListManager.brick_comeback(robot_obj)
            # self.brickListManager.brick_fin(robot_obj)

            # Want to Fetch Src and Dst Brick Processing? -> robot_obj.getOngoingBlock() , robot_obj.getDstBlock()

            # robot_obj.push_inst(new_inst)
            # robot_obj.push_inst_list(new_inst_list)

            # TODO: Delete (Test Purpose Only)
            new_inst_forward = Instruction('FORWARD', [(50 * config["DEGREE_PER_MM_FORWARD"])])
            robot_obj.push_inst(new_inst_forward)
            print ("new instruction")

        # Pop_front instruction
        robot_obj.pop_inst()

        # Update of Robot Information (While Connection)
        self.updated_robot_info_conn.emit(robot_obj)
        self.updated_progress.emit(self.brickListManager)

        if (robot_obj.getCurrentInst() == None) :
            return ""
        return str(robot_obj.getCurrentInst())