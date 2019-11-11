from socket import *

# --- Import Motor/Car.py ---

import os
import sys

path_for_car = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
path_for_car = os.path.join(path_for_car, 'CameraVision')
sys.path.append(path_for_car)

# Modify if this invokes error
from Motor import Car
# --- Import Motor/Car.py ---

# ------ Configuration ------
# Server IP Address
SERVER_IP_ADDR = ''
SERVER_PORT = 8080
# Module Type Informations
MODULE_TYPE = 'ROBO_ARM'

# Maximum buffer size
MAX_BUF_SIZE = 1024
# ------ Configuration ------

clientSock = socket(AF_INET, SOCK_STREAM)
clientSock.connect((SERVER_IP_ADDR, SERVER_PORT))

# New Car Module
car = Car.Car()

# TOOD : Action for robot arms
while (True) :
    recv_inst = clientSock.recv(MAX_BUF_SIZE)
    recv_inst = recv_inst.decode('utf-8')

    recv_inst_tok = str.split(recv_inst, ' ')
    if (recv_inst_tok[0] == 'ROTATE') :
        car.rotate()
    elif (recv_inst_tok[0] == 'FORWARD') :
        car.move_forward()
    elif (recv_inst_tok[0] == 'RIGHT') :
        car.move_right()

    # Noticing Current Task is totally done.
    clientSock.send("INST_DONE")