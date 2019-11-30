import numpy as np
import math
import yaml
from PyQt5 import QtCore

from S_TaskManagement.BrickListManager import BrickListManager
from S_TaskManagement.Instruction import Instruction
from S_RoboticArmControl.RobotControl import Robot
from S_RoboticArmControl.Elements import RobotPhase

# Configurations
config = yaml.load(open("./Config.yaml", 'r'), Loader=yaml.FullLoader)

class TaskManager (QtCore.QObject) :
    updated_robot_info_conn = QtCore.pyqtSignal(Robot)
    updated_progress = QtCore.pyqtSignal(BrickListManager)

    def __init__(self, parent=None):
        super(TaskManager, self).__init__(parent)
        self.brickListManager = BrickListManager()

    # Push initial Instructions which moves robot to initial position.
    def pushInitialInstruction(self, robot_obj):
        cur_pos = robot_obj.getPos()
        init_pos = robot_obj.getInitPos() # Elemets.Position Object
        init_instList=[]
        init_instList.append(Instruction('FORWARD',[init_pos[1]-cur_pos[1]]))
        init_instList.append( Instruction('RIGHT', [init_pos[0] - cur_pos[0]]))
        robot_obj.push_back_inst_list(init_instList)

        # Update of Robot Information (While Connection)
        self.updated_robot_info_conn.emit(robot_obj)

    ## For CITD III, We need an initial position info to seperate two trajectories.
    ## In CITD IV, We will try to generalize for more than three trajectories.
    def fetchNextTask(self, robot_obj) :
        instList=[]
        rotatePosToWorking=config["ROBOT_ROTATING_DIAMETER"] -config["ROBOT_BODY_SIZE_MM"]
        center = self.brickListManager.srcCurrentLayer.center
        radius = self.brickListManager.dstCurrentLayer.getRadius()
        dirX = 1.0

        if (robot_obj.isQueueEmpty() == True) :
            # Push new Instructions for each robot_obj phase
            if(robot_obj.phase==RobotPhase.STOP):
                success = self.brickListManager.brick_move(robot_obj)
                if (success == True) :
                    # Move
                    srcBlock=robot_obj.getSrcBlock()
                    roboNum = robot_obj.get_robo_num()
                    endPos = calPositionForRotation(srcBlock.getPos())

                    dist_x=endPos()[0]-robot_obj.getPos().pos[0]
                    dist_y=endPos()[1]-robot_obj.getPos().pos[1]

                    instList.append(Instruction(('FORWARD', [(dist_x * config["DEGREE_PER_MM_FORWARD"])])))
                    instList.append(Instruction(('RIGHT', [(dist_y * config["DEGREE_PER_MM_RIGHT"])])))
                    instList.append(Instruction(('FORWARD', [(rotatePosToWorking * config["DEGREE_PER_MM_FORWARD"])])))

                    #grap brick

                    x = config["ROBOT_BODY_SIZE_MM"] - config["ROBOT_MOTOR_POS"][0]
                    y = srcBlock.getPos().pos[2] - config["ROBOT_MOTOR_POS"][1]
                    instList.append(Instruction('ARM', [x, y, 0.0, 0]))  # state(0 ~2)])(state 0: grab, 1: release , 2: just moving))

                    # move to moving posture
                    #posture=config["ROBOT_MOVING_POSTURE"]
                    #instList.appent(Instruction('ARM', [posture[0], posture[1], 0.0, 2]))
                    #instList.append(Instruction('ROTATE', [(180 * config["DEGREE_PER_MM_ROTATE"])]))

            elif (robot_obj.phase == RobotPhase.MOVING):
                success = self.brickListManager.brick_lift(robot_obj)
                if (success == True) :
                    dstBlock = robot_obj.getDstBlock()
                    brickDomain = brickArea(dstBlock.getPos(), center)
                    roboNum = robot_obj.get_robo_num()

                    startPos = calPositionForRotation(robot_obj.getPos())
                    endPos = calPositionForRotation(dstBlock.getPos())

                    x = 0.0
                    rotate = calRotationDegree(robot_obj.getPos().getDir(), -(dstBlock.getPos().getDir()))

                    if (brickDomain > 2 and roboNum == 0):
                        rotate = (-rotate)  # CCW
                        x = center.getPos()[0] - (config["ROBOT_ROTATING_DIAMETER"] + radius)
                    elif (brickDomain > 2 and roboNum == 1):
                        x = center.getPos()[0] + (config["ROBOT_ROTATING_DIAMETER"] + radius)
                    elif (roboNum == 0):
                        rotate = (-rotate)  # CCW
                        x = endPos[0]
                    else:
                        x = endPos[0]

                    dist_x1 = startPos[0] - x
                    dist_x2 = endPos[0] - x
                    dist_y = endPos[1] - startPos[1]

                    # move to starting point of lift instruction
                    instList.append(Instruction(
                        'FORWARD', [(config["ROBOT_ROTATING_DIAMETER"] * config["DEGREE_PER_MM_FORWARD"])]))

                    # move to rotation point for destination brick => 3 step(x axis move => y axis mov => x axis mov)
                    instList.append(Instruction('RIGHT', [(dist_x1 * config["DEGREE_PER_MM_RIGHT"])]))
                    instList.append(Instruction('FORWARD', [(dist_y * config["DEGREE_PER_MM_FORWARD"])]))
                    instList.append(Instruction('RIGHT', [(dist_x2 * config["DEGREE_PER_MM_RIGHT"])]))

                    # rotate until robot arm is just perpendicular to brick
                    # (robot Arm direction is just Opposite to direction of brick)
                    instList.append(Instruction('ROTATE', [(rotate * config["DEGREE_PER_MM_ROTATE"])]))

                    # move to working position
                    instList.append(Instruction('FORWARD', [(rotatePosToWorking * config["DEGREE_PER_MM_FORWARD"])]))

                    # release brick
                    x = config["ROBOT_BODY_SIZE_MM"]-config["ROBOT_MOTOR_POS"][0]
                    y = dstBlock.getPos().pos[2]-config["ROBOT_MOTOR_POS"][1]
                    instList.append(Instruction('ARM', [x ,y,0.0,1])) #state(0 ~2)])(state 0: grab, 1: release , 2: just moving))

       

            elif (robot_obj.phase == RobotPhase.LIFTING):
                success = self.brickListManager.brick_comeback(robot_obj)
                if (success == True) :

                    robotArmPosDomain = brickArea(robot_obj.getPos(), center)
                    roboNum = robot_obj.get_robo_num()

                    startPos = calPositionForRotation(robot_obj.getPos())
                    tmp=config["INIT_POS"]
                    tmp.append(0.0)
                    endPos=tmp

                    x = 0.0
                    rotate = calRotationDegree(robot_obj.getPos().getDir(),[0.0,-1.0,0.0])

                    if (robotArmPosDomain > 2 and roboNum == 0):
                        rotate = (-rotate)  # CCW
                        x = center.getPos()[0] - (config["ROBOT_ROTATING_DIAMETER"] + radius)
                    elif (robotArmPosDomain > 2 and roboNum == 1):
                        x = center.getPos()[0] + (config["ROBOT_ROTATING_DIAMETER"] + radius)
                    elif (roboNum == 0):
                        rotate = (-rotate)  # CCW
                        x = endPos[0]
                    else:
                        x = endPos[0]

                    dist_x1 = startPos[0] - x
                    dist_x2 = endPos[0] - x
                    dist_y = endPos[1] - startPos[1]

                    # move to Rotating position
                    instList.append(Instruction('FORWARD', [(rotatePosToWorking * config["DEGREE_PER_MM_FORWARD"])]))

                    #rotate until robotArm's diretion becomes [0.0,-1.0,0.0]
                    instList.append(Instruction('ROTATE', [(rotate * config["DEGREE_PER_MM_ROTATE"])]))

                    # move to end point (here initial point)
                    instList.append(Instruction('RIGHT', [(dist_x1 * config["DEGREE_PER_MM_RIGHT"])]))
                    instList.append(Instruction('FORWARD', [(dist_y * config["DEGREE_PER_MM_FORWARD"])]))
                    instList.append(Instruction('RIGHT', [(dist_x2 * config["DEGREE_PER_MM_RIGHT"])]))

            elif (robot_obj.phase == RobotPhase.COMEBACK):
                success=self.brickListManager.brick_fin(robot_obj)
            else :
                # Not Reached
                print("else condition!!! error jabja")
                pass

            robot_obj.push_back_inst_list(instList)

        # Pop_front instruction
        robot_obj.pop_inst()

        # Update of Robot Information (While Connection)
        self.updated_robot_info_conn.emit(robot_obj)
        self.updated_progress.emit(self.brickListManager)

        if (robot_obj.getCurrentInst() == None) :
            return None

        return robot_obj.getCurrentInst()

    # TODO: Fetching Ideal Position based on robot_obj current position & new_instruction
    def getIdealPos(self, robot_obj, new_instruction):
        pass

    # TODO: Push Front new Instructions to Callibrate. (Based on Heuristics)
    def callibrate(self, ideal_pos, robot_obj):
        pass

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
def calPositionForRotation(pos):
        ret = pos.getPos() + pos.getPos().getDir() * config["ROBOT_ROTATING_DIAMETER"]
        return ret

def calRotationDegree(dir1,dir2):
    #make dir1 & dir2 to unit direction vector
    dir1= dir1 /(np.linalg.norm(dir1))
    dir2 = (dir2 / (np.linalg.norm(dir2)))*(-1.0)
    dotProduct=(dir1*dir2)
    return 180*(math.acos(dotProduct[0]+dotProduct[1]))/math.pi


