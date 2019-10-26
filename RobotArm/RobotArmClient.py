import numpy as np

from Motor.Motor import Motor
import RPi.GPIO as gpio
import math
import operator

class armClient:
    def __init__(self ,dirPins, stpPins, maxAngles, minAngles,servoPin):
        self.curAngles = [0.0, 0.0, 0.0]
        self.motorList = []
        self.slice=50
        self.ratio=5.0 #ratio of rotation,  second motor rotates robot arm indirect wat
        gpio.setmode(gpio.BCM)
        gpio.setup(servoPin, gpio.OUT)

        self.servoPwm = gpio.PWM(servoPin, 50)
        self.servoPwm.start(0)

        for i in range(0, 3):
            motor = Motor(1.8, 50.0, self, 0.0, 0.0)
            motor.set(dirPins[i], stpPins[i])
            motor.maxAng = maxAngles[i]
            motor.minAng = minAngles[i]
            self.motorList.append(motor)

    def rotate(self,target):
        angle = target - self.curAngles[2]
        if(abs(angle)>180.0):
           angle=angle-360
        self.motorList[2].move(angle,0.02,True)
        self.curAngles[2]=target[2]

    def moveInDirectLine(self,a,b,a1,b1,resol):
        pos1=calPos(a,b)
        pos2=calPos(a1,b1)
        dif=[pos2[0]-pos1[0],pos2[1]-pos1[1]]/resol
        cur=calAngle(pos1)
        for i in range(0,resol):
            before = cur
            cur=calAngle(pos1[0]+i*dif[0],pos1[1]+i*dif[1])
            mov=map(operator.sub,cur,before)
            self.motorList[0].move(mov[0], 0.02, False)
            self.motorList[1].move(mov[1], 0.02, False)


    def work(self,target,lift):
        self.rotate(target[2])
        self.moveInDirectLine(self.curAngles[0],self.curAngles[1],target[0],target[1],self.slice)
        if lift:
            self.servoPwm.ChangeDutyCycle(3)
        else:
            self.servoPwm.ChangeDutyCycle(12)
        self.moveInDirectLine(target[0], target[1],self.curAngles[0], self.curAngles[1],self.slice)

    def basicPos(self):
        pass
    def initPos(self):
        pass

l1=140
l2=220
#l1=140, l2-220
def calPos(a,b):
    # 3 cases
    return [l1*math.cos(a)+l2*math.cos(a+b-math.pi),l1*math.sin(a)+l2*math.sin(a+b-math.pi)]

def calAngle(x,y):
    l3=math.sqrt(x**2+y**2)
    tan=math.atan(y/x)

    # cosine second law,  a3,a2
    a3=math.acos((l3**2-l1**2-l2**2)/(-2.0*l1*l2))
    a2 = math.acos((l2 ** 2 - l3 ** 2 - l1 ** 2) / (-2.0 * l1 * l3))
    return [tan+a2,a3]




