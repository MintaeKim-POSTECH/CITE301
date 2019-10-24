import numpy as np

from Motor.Motor import Motor


class armClient:
    def __init__(self):
        self.curAngles = [0.0, 0.0, 0.0]
        self.nextAngles = [0.0, 0.0, 0.0]
        self.motorList = []
        for i in range(0, 3):
            motor = Motor(1.8, 50.0, self, 0.0, 0.0)
            self.motorList.append(motor)

    def setMotor(self, dirPins, stpPins, maxAngles, minAngles):
        for i in range(0, 3):
            self.motorList[i].set(dirPins[i], stpPins[i])
            self.motorList[i].maxAng = maxAngles[i]
            self.motorList[i].minAng = minAngles[i]
    def rotate(self,angle):
        self.motorList[2].move()
    def lift(self, pos):
        self.nextPos = pos
        angles = cal.calNextAngle(self.curPos, self.nextPos);
        self.curPos = pos
        # communicate with robot arm
        # send robot arm the next Angle

