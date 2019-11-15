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
# from Car import Car
# --- Import Motor/Car.py ---

clientSock = socket(AF_INET, SOCK_STREAM)
clientSock.connect((config["SERVER_IP_ADDR"], config["SERVER_PORT"]))

# New Car Module
# car = Car()

# TOOD : Action for robot arms
while (True) :
    recv_inst = clientSock.recv(config["MAX_BUF_SIZE"])
    recv_inst = recv_inst.decode()
    print ("recv_inst : ")
    print (recv_inst)
    print ("-----")
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
    elif (recv_inst_tok[0] == 'EXIT') :
        clientSock.sendall("DONE".encode())
        break

    # Noticing Current Task is totally done.
    clientSock.sendall("DONE".encode())
    
    # Get Position infos
    recv_inst = clientSock.recv(config["MAX_BUF_SIZE"])
    recv_inst = recv_inst.decode()
    
    print (recv_inst)
    
    recv_inst_tok = recv_inst.split('_')