from RoboticArmControl.Elements import RobotPhase
from RoboticArmControl.Elements import Position as pos
import numpy as np
from RoboticArmControl.BrickModule import Brick
import RoboticArmControl.CalArmPath as cal
import Motor.Motor


class RobotControl:

    def __init__(self):
        self.phase = RobotPhase.STOP
        self.working = None
        self.next = None
        self.curAngles = [0.0, 0.0, 0.0]
        self.nextAngles = [0.0, 0.0, 0.0]
        self.center = None
        self.curPos=pos()
        self.nextPos=pos()

    def setNextAngle(self):
        pass

    def move(self):
        # communicate with robot arm
        self.center = self.working.dst


class Robot:
    def __init__(self):
        self.phase = RobotPhase.STOP
        self.working = None
        self.next = None
        self.curAngles = [0.0, 0.0, 0.0]
        self.nextAngles = [0.0, 0.0, 0.0]
        self.center = None
        self.curPos = pos()
        self.nextPos = pos()

    def setMotorPin(self):
        pass
    def lift(self, pos):
            self.nextPos = pos
            angles = cal.calNextAngle(self.curPos, self.nextPos);
            self.curPos = pos
            # communicate with robot arm
            # send robot arm the next Angle
