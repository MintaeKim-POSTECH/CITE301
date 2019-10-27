# Reference : https://www.youtube.com/watch?v=o-j9TReI1aQ&app=desktop

from Motor import Motor
from multiprocessing import Process # for multiprocessing

# GPIO Pins
## GPIO[0] : Up-LEFT / GPIO[1] : Up-RIGHT
## GPIO[2] : Down-LEFT / GPIO[3] : Down-RIGHT
GPIO_DIRPINS = [23, 0, 0, 0] # GPIO DIR PINS
GPIO_STPPINS = [24, 0, 0, 0] # GPIO STEPPER PINS

# Motor Configurations
MOTOR_ANG_PER_SEC = 1.8
MOTOR_GEAR = 1.0

# Rotation per one move_* or rotation operation
ANGLE_PER_ONE_OPS_FRONT = 10
ANGLE_PER_ONE_OPS_RIGHT = 5
ANGLE_PER_ONE_OPS_ROTATION = 5

class Car:
    # Class Constructor
    def __init__(self):
        self.wheels = []
        for i in range(4):
            wheel = Motor(MOTOR_ANG_PER_SEC, MOTOR_GEAR)
            wheel.set(GPIO_DIRPIN[i], GPIO_STPPIN[i])

            self.wheels.append(wheel)

    # Move forward (backwards for - linear_velocity)
    def move_forward (self, linear_velocity, angle = ANGLE_PER_ONE_OPS_FRONT) :
        wheels_process_list = []
        # Initiation of concurrent programming
        for i in range(4):
            # Forward & Backwoards = 4 wheels same direction
            wheels_process = Process(target=wheel_move, args=(self.wheels[i], angle, linear_velocity, ))
            wheels_process.start()
            wheels_process_list.append(wheels_process)

        for i in range(4):
            # Wait the child process to finish
            wheels_process_list[i].join()

        # TODO : Position & Rotation Callibration (using CVs)

        # TODO : Return Current Position
        return NULL

    # Move Right (left for - linear_velocity)
    def move_right(self, linear_velocity, angle = ANGLE_PER_ONE_OPS_RIGHT):
        wheels_process_list = []
        # Initiation of concurrent programming
        for i in range(4):
            # Right & Left = Wheel (#0, #3) (#1, #2) Same Direction
            if (i == 0 or i == 3) :
                wheels_process = Process(target=wheel_move, args=(self.wheels[i], angle, linear_velocity,))
            else :
                wheels_process = Process(target=wheel_move, args=(self.wheels[i], -angle, linear_velocity))
            wheels_process.start()
            wheels_process_list.append(wheels_process)

        for i in range(4):
            # Wait the child process to finish
            wheels_process_list[i].join()

        # TODO : Position & Rotation Callibration (using CVs)

        # TODO : Return Current Position
        return NULL

    # Rotation Clockwise (Counter-clockwise for - angular_velocity)
    def rotate (self, angular_velocity):
        wheels_process_list = []
        # Initiation of concurrent programming
        for i in range(4):
            # Rotation = Wheel (#0, #2) (#1, #3) Same Direction
            if (i == 0 or i == 2) :
                wheels_process = Process(target=wheel_move, args=(self.wheels[i], angle, linear_velocity,))
            else :
                wheels_process = Process(target=wheel_move, args=(self.wheels[i], -angle, linear_velocity))
            wheels_process.start()
            wheels_process_list.append(wheels_process)

        for i in range(4):
            # Wait the child process to finish
            wheels_process_list[i].join()

        # TODO : Position & Rotation Callibration (using CVs)

        # TODO : Return Current Position
        return NULL

# Multiprocessing
def wheel_move(wheel, angle, vel):
    wheel.move(angle, vel, smooth=True)