# This code is a basic code for stpper motor.
# Cotrolling with A4988 and Rasberry Pi 3 B

import sys
import RPi.GPIO as gpio  # https://pypi.python.org/pypi/RPi.GPIO more info
import time

class Motor:

    def __init__(self, angPerSt, gear,maxAng=0.0, minAng=0.0):
        self.dir = 'right'  # direction of rotate, right=clockwise
        self.curAng = 0.00  # current angle, For robot arm positioning & coorection error of movility
        self.angPerSt = angPerSt  # stepper motor configuration
        self.gear = gear  # geared stpper motor configuration, when it 2 times slow down, then value is 2.00
        self.maxAng = maxAng  # maximun Angle that stepper can rotate, it's for robotArm
        self.minAng = minAng
        self.dirPin = 0
        self.stpPin = 0

    def set(self,dirPin, stpPin):
        gpio.setmode(gpio.BCM)
        gpio.setup(dirPin, gpio.OUT)  # setting gpio, dirPin controls direction of motor
        gpio.setup(stpPin, gpio.OUT)  # stpPin controls step number of motor, you must set connect pin on rasberry Pi 3B
        gpio.output(dirPin, True)
        gpio.output(stpPin, False)

        # Updating dir/stp Pins
        self.dirPin = dirPin
        self.stpPin = stpPin

    def getStep(self, angle):
        stp = int(angle / self.angPerSt)
        return stp

    def getDelay(self, vel):
        # rotation per sec => step/s
        totalStep = 360.0 / self.angPerSt
        t = 1.000 / vel
        return t / totalStep

    def getSmoothVel(self,maxVel,target,cur):
        return 1/(1+9*(cur/target)(cur/target))

    def move(self, angle, vel,smooth):
        if (angle + self.curAng < self.minAng or angle + self.curAng < self.maxAng) and self.maxAng != 0:
            return False

        angle = (-angle)

        delay = self.getDelay(vel*self.gear)
        stp = self.getStep(angle*self.gear)
        counter = 0

        if angle >= 0.0:
            gpio.output(self.dirPin, True)
            self.curAng += (stp * self.angPerSt)
        else:
            gpio.output(self.dirPin, False)
            self.curAng -= (stp * self.angPerSt)
        print(stp)
        print(delay)
        stp_origin = stp
        stp = abs(stp)
        if(not smooth):
            delay=self.getDelay(vel*self.gear)
            while counter < stp:
                gpio.output(self.stpPin, True)
                time.sleep(delay)
                gpio.output(self.stpPin, False)
                time.sleep(delay)
                counter += 1
        else:
            while counter < stp:
                v=self.getSmoothVel(vel,stp/2,stp/2-counter)
                delay=self.getDelay(v)
                gpio.output(self.stpPin, True)
                time.sleep(delay)
                gpio.output(self.stpPin, False)
                time.sleep(delay)
                counter += 1
        return True

    def __del__(self):
        print()
        gpio.cleanup()
