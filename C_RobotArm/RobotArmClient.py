import numpy as np

from C_Motor import Motor

import RPi.GPIO as gpio

import math

import operator

import threading

import time

import queue


class armClient:

    def __init__(self, dirPins, stpPins, maxAngles, minAngles, servoPin):

        a = calAngle(49.0, -5.0)

        self.curAngles = [a[0], a[1], 0.0]

        self.motorList = []

        self.slice = 50

        self.ratio = 5.0  # ratio of rotation,  second motor rotates robot arm indirect wat

        gpio.setmode(gpio.BCM)

        # gpio.setup(servoPin, gpio.OUT)

        # self.servoPwm = gpio.PWM(servoPin, 50)

        # self.servoPwm.start(0)

        for i in range(0, 3):
            motor = Motor(1.8, 10.0, 0.0, 0.0)

            motor.set(dirPins[i], stpPins[i])

            motor.maxAng = maxAngles[i]

            motor.minAng = minAngles[i]

            motor.curAng = self.curAngles[i]

            self.motorList.append(motor)

        self.motorList[0].gear = 50

        self.motorList[1].curAng = self.curAngles[1] + self.curAngles[0]

    def rotate(self, target):

        angle = target - self.curAngles[2]

        if (abs(angle) > 180.0):
            angle = angle - 360

        print(angle)

        self.motorList[2].move(angle, 1.0, False)

        self.motorList[2].curAng += (
                    self.motorList[2].getStep(angle * self.motorList[2].gear) * 1.8 / self.motorList[2].gear)

        self.curAngles[2] = self.motorList[2].curAng

    def moveInDirectLine(self, a1, b1, resol):
        cur = [self.curAngles[0], self.curAngles[1]]
        print(cur)
        pos1 = calPos(cur[0], cur[1])
        pos2 = calPos(a1, b1)
        dif = [(pos2[0] - pos1[0]) / resol, (pos2[1] - pos1[1]) / resol]
        m = self.motorList
        before = [cur[0], cur[1]]

        stpArr=[]
        velArr=[]
        len=0
        for i in range(1, resol + 1):
            cur = calAngle(pos1[0] + i * dif[0], pos1[1] + i * dif[1])
            # because the frame of robot arm always makes prallelogram
            mov = [(cur[0] - before[0]), cur[1] + cur[0] - (before[1] + before[0])]
            print(mov)
            stp = [int(mov[0] * m[0].gear / 1.8), int(mov[1] * m[1].gear / 1.8)]

            if(stp[0]>0 and stp[1]>0):
                len+=1
                stpArr.apeend(stp)
                v1 = 0.2
                v2 = 0.2
                if (stp[0] > stp[1]):
                    v2 = v1 * stp[1] / stp[0]
                else:
                    v1 = v2 * stp[0] / stp[1]
                velArr.append([v1,v2])

            m[0].curAng += (stp[0] * 1.8 / m[0].gear)
            m[1].curAng += (stp[1] * 1.8 / m[1].gear)
            before = [m[0].curAng, m[1].curAng - m[0].curAng]

        for i in range(0,len):
            v=velArr[i]
            stp=stpArr[i]
            t1 = threading.Thread(target=m[0].move, args=(-stpArr[0]*1.8*m[0].gear, v[0], False))
            t2 = threading.Thread(target=m[1].move, args=(stpArr[1]*1.8*m[1].gear, v[1], False))
            t1.start()
            t2.start()
            t1.join()
            t2.join()

        self.curAngles = [m[0].curAng, m[1].curAng - m[0].curAng, m[2].curAng]

    def work(self, target, lift):
        time.sleep(2)
        cur = [self.curAngles[0], self.curAngles[1], self.curAngles[2]]
        self.rotate(target[2])
        time.sleep(0.5)
        self.moveInDirectLine(target[0], target[1], 1)
        if lift:
            pass
            # self.servoPwm.ChangeDutyCycle(3)
        else:
            pass
            # self.servoPwm.ChangeDutyCycle(12)
        time.sleep(2)
        print(self.curAngles)
        self.moveInDirectLine(cur[0], cur[1], 1)
        time.sleep(0.5)
        self.rotate(cur[2])

    def initPos(self):
        pass

l1 = 145
l2 = 180

def calPos(a, b):
    # 3 cases
    return [l1 * math.cos(a * math.pi / 180) + l2 * math.cos((a + b - 180) * math.pi / 180),
            l1 * math.sin(a * math.pi / 180) + l2 * math.sin((a + b - 180) * math.pi / 180)]


def calAngle(x, y):
    l3 = math.sqrt(x ** 2 + y ** 2)
    tan = math.atan(y / x)
    # cosine second law,  a3,a2
    a3 = math.acos((l3 ** 2 - l1 ** 2 - l2 ** 2) / (-2.0 * l1 * l2))
    a2 = math.acos((l2 ** 2 - l3 ** 2 - l1 ** 2) / (-2.0 * l1 * l3))
    return [(tan + a2) * 180 / math.pi, a3 * 180 / math.pi]


test = armClient([21, 24, 15], [20, 23, 14], [0.0, 0.0, 0.0], [360.0, 360.0, 360.0], 10)
ang = calAngle(100.0, -71.0)
print(ang)
print(calPos(ang[0], ang[1]))
test.work([ang[0], ang[1], 50.0], False)
ang = calAngle(170.0, 0.0)
test.work([ang[0], ang[1], 50.0], False)