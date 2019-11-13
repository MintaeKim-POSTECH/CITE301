from socket import *
import yaml

# Configurations
config = yaml.load(open("../Config.yaml", 'r'), Loader=yaml.FullLoader)

# --- Import Motor/Car.py ---
import os
import sys

path_for_car = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
path_for_car = os.path.join(path_for_car, 'Motor')
sys.path.append(path_for_car)

# Modify if this invokes error
from Car import Car
# --- Import Motor/Car.py ---

clientSock = socket(AF_INET, SOCK_STREAM)
clientSock.connect((config["SERVER_IP_ADDR"], config["SERVER_PORT"]))

# New Car Module
car = Car.Car()

# TOOD : Action for robot arms
while (True) :
    recv_inst = clientSock.recv(config["MAX_BUF_SIZE"])
    recv_inst = recv_inst.decode('utf-8')
    recv_inst_tok = str.split(recv_inst, ' ')
    
    if (recv_inst_tok[0] == 'ROTATE') :
        car.rotate(float(recv_inst_tok[1]))
    elif (recv_inst_tok[0] == 'FORWARD') :
        car.move_forward(float(recv_inst_tok[1]))
    elif (recv_inst_tok[0] == 'RIGHT') :
        car.move_right(float(recv_inst_tok[1]))
    elif (recv_inst_tok[0] == 'EXIT') :
        clientSock.send("INST_DONE")
        break

    # Noticing Current Task is totally done.
    clientSock.send("INST_DONE")
    
    # Get Position infos
    recv_inst = clientSock.recv(config["MAX_BUF_SIZE"])
    recv_inst = recv_inst.decode('utf-8')
    
    print (recv_inst)
    
    recv_inst_tok = str.split(recv_inst, ' ')