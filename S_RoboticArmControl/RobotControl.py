from S_RoboticArmControl.Elements import RobotPhase
from S_RoboticArmControl.Elements import Position as pos
import numpy as np
from S_RoboticArmControl.BrickModule import Brick
import S_RoboticArmControl.CalArmPath_Test as cal
import C_Motor.Motor

class Robot:
    def __init__(self):
        # Robot State & Ongoing Src-Brick/Dst-Brick
        self.phase = RobotPhase.STOP
        self.brick_src = None
        self.brick_ongoing = None
        self.brick_dst = None

        # Robot Wheel Information
        self.cur_pos = pos()

        # Instruction Queue
        self.cur_inst = None
        self.next_inst_queue = []

        # Angle Information for Robot Arm
        self.cur_arm_angle = [0.0, 0.0, 0.0]
        self.next_arm_angle = [0.0, 0.0, 0.0]

        # Initial Position
        ## For CITD III, We need an initial position info to seperate two trajectories.
        ## In CITD IV, We will try to generalize for more than three trajectories.
        self.initial_pos = pos()

        # Color
        self.color_rgb = None

    def brick_info_move(self, srcBrick):
        self.phase = RobotPhase.MOVING

        self.brick_src = srcBrick

    def brick_info_lift(self, dstBrick):
        self.phase = RobotPhase.LIFTING

        self.brick_dst = dstBrick
        self.brick_ongoing = self.brick_src
        self.brick_src = None

    def brick_info_stack(self):
        self.phase = RobotPhase.STACKING

    def brick_info_comeback(self):
        self.phase = RobotPhase.COMEBACK

        self.brick_ongoing = None
        self.brick_dst = None

    def brick_info_fin(self):
        self.phase = RobotPhase.STOP

    def isQueueEmpty(self):
        return (len(self.next_inst_queue) == 0)
    def push_inst(self, new_inst):
        self.next_inst_queue.append(new_inst)
    def pop_inst(self):
        if (self.isQueueEmpty()):
            return None
        self.cur_inst = self.next_inst_queue[0]
        self.next_inst_queue.remove(self.cur_inst)

    # Initial Position
    ## For CITD III, We need an initial position info to seperate two trajectories.
    ## In CITD IV, We will try to generalize for more than three trajectories.
    def setInitPos(self, init_pos):
        # TODO: init_pos is 3-tuple (X, Y, Z)
        # TODO: Implement
        pass
    def getInitPos(self):
        return self.initial_pos

    def setPos_position(self, pos):
        self.cur_pos.setPos(pos)
    def setPos_angle(self, angle):
        self.cur_pos.setDir(angle)
    def getPos(self):
        return self.cur_pos

    def setColorRGB(self, color_rgb):
        self.color_rgb = color_rgb
    def getColorRGB(self):
        return self.color_rgb

    def getOngoingBlock(self):
        return self.brick_ongoing
    def getDstBlock(self):
        return self.brick_dst
    def getCurrentInst(self):
        return self.cur_inst

'''
    def setMotorPin(self):
        pass
    def lift(self, pos):
            # self.nextPos = pos
            # angles = cal.calNextAngle(self.curPos, self.nextPos);
            # self.curPos = pos
            # communicate with robot arm
            # send robot arm the next Angle
        pass
'''