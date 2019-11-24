from C_Motor import Motor
import time

motor = Motor(1.8, 1.0)

motor.set(13, 19)

motor.move (360, 1, False)
motor.motor_end()
time.sleep(0.3)
motor.move (-360, 1, False)
motor.motor_end()

print("End")

while (True) :
    pass
