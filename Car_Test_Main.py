from C_Motor.Car import Car
import time

car = Car()

while(1):
    time.sleep(1)
    test=input()
    if test=="w" :
        car.move_forward(10000)
    elif (test=="s"):
        car.move_forward(-600)
    elif test=="d":
        car.move_right(300)
    elif(test=="a"):
        car.move_right(-300)
    elif(test=="e"):
        car.rotate(500)
    elif(test=="q"):
        car.rotate(-500)
    elif(test=="stop"):
        break
    else:
        continue