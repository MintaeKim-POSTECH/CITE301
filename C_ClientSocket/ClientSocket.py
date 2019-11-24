from socket import *
import yaml

# Configurations
config = yaml.load(open("../Config.yaml", 'r'), Loader=yaml.FullLoader)

# --- Import C_Motor/Car.py ---
import os
import sys

path_for_car = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
path_for_car = os.path.join(path_for_car, 'C_Motor')
sys.path.append(path_for_car)

# Modify if this invokes error
from Car import Car
# --- Import C_Motor/Car.py ---

def run_client() :
    clientSock = socket(AF_INET, SOCK_STREAM)
    clientSock.connect((config["SERVER_IP_ADDR"], config["SERVER_PORT"]))

    # New Car Module
    car = Car()

    # Client Flow 1 : Send Robot_Arm Number & Color Data
    infoDat = str(config["ROBOT_ARM_NUM"]) + " " + str(config["ROBOT_ARM_COLOR"][0]) + " "
    infoDat += str(config["ROBOT_ARM_COLOR"][1]) + " " + str(config["ROBOT_ARM_COLOR"][2])

    clientSock.sendall(infoDat.encode())

    # Client Flow 2 : Iteration with While Loop, Executing action for robot arm instructions
    while (True) :
        recv_inst = clientSock.recv(config["MAX_BUF_SIZE"]).decode()
        recv_inst_tok = recv_inst.split('_')
    
        if (recv_inst_tok[0] == 'ROTATE') :
            print ("rotate " + recv_inst_tok[1])
            car.rotate(float(recv_inst_tok[1]))
        elif (recv_inst_tok[0] == 'FORWARD') :
            print("forward " + recv_inst_tok[1])
            car.move_forward(float(recv_inst_tok[1]))
        elif (recv_inst_tok[0] == 'RIGHT') :
            print("right " + recv_inst_tok[1])
            car.move_right(float(recv_inst_tok[1]))
        elif (recv_inst_tok[0] == 'ARM') :
            # TODO: ARM arg[1] arg[2] arg[3]
            pass
        elif (recv_inst_tok[0] == 'GRAB') :
            # TODO : GRAB
            pass
        elif (recv_inst_tok[0] == 'RELEASE') :
            # TODO : RELEASE
            pass
        elif (recv_inst_tok[0] == 'EXIT') : # Jobs Done
            break

        # Noticing Current Task is totally done.
        clientSock.sendall("DONE".encode())
    clientSock.sendall("CLIENT_ELIMINATED".encode())

if __name__ == "__main__" :
    run_client()