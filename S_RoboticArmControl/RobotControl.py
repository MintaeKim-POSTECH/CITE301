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
        self.center = None
        self.cur_pos = pos()

        # Instruction Queue
        self.cur_inst = None
        self.next_inst_queue = []

        # Angle Information for Robot Arm
        self.cur_arm_angle = [0.0, 0.0, 0.0]
        self.next_arm_angle = [0.0, 0.0, 0.0]

    def stop_src_decided(self, srcBrick):
        self.brick_src = srcBrick

    def lifting_grabbed(self, dstBrick):
        self.brick_ongoing = self.brick_src
        self.brick_src = None
        self.brick_dst = dstBrick

    def stacking_released(self):
        self.brick_ongoing = None
        self.brick_dst = None

    def setMotorPin(self):
        pass
    def lift(self, pos):
            # self.nextPos = pos
            # angles = cal.calNextAngle(self.curPos, self.nextPos);
            # self.curPos = pos
            # communicate with robot arm
            # send robot arm the next Angle
        pass

    def getPos(self):
        return self.cur_pos
    def getOngoingBlock(self):
        return self.brick_ongoing
    def getDstBlock(self):
        return self.brick_dst