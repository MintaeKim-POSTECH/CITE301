from socket import *
import yaml
import time

# from C_Motor.Car import Car

# Configurations
config = yaml.load(open("./Config.yaml", 'r'), Loader=yaml.FullLoader)

def run_client() :
    clientSock = socket(AF_INET, SOCK_STREAM)
    clientSock.connect((config["SERVER_IP_ADDR"], config["SERVER_PORT"]))

    # New Car Module
    # car = Car()

    # Client Flow 1 : Send Robot_Arm Number & Color Data
    infoDat = str(config["ROBOT_ARM_NUM"]) + " " + str(config["ROBOT_ARM_COLOR"][0]) + " "
    infoDat += str(config["ROBOT_ARM_COLOR"][1]) + " " + str(config["ROBOT_ARM_COLOR"][2]) + " "
    infoDat += str(config["INIT_POS"][0]) + " " + str(config["INIT_POS"][1])

    clientSock.sendall(infoDat.encode())

    # Client Flow 2 : Iteration with While Loop, Executing action for robot arm instructions
    while (True) :
        recv_inst = clientSock.recv(config["MAX_BUF_SIZE"]).decode()
        recv_inst_tok = recv_inst.split(' ')
    
        if (recv_inst_tok[0] == 'ROTATE') :
            print ("rotate " + recv_inst_tok[1])
            # TODO: car.rotate(float(recv_inst_tok[1]))
        elif (recv_inst_tok[0] == 'FORWARD') :
            print("forward " + recv_inst_tok[1])
            # TODO: car.move_forward(float(recv_inst_tok[1]))
        elif (recv_inst_tok[0] == 'RIGHT') :
            print("right " + recv_inst_tok[1])
            # TODO: car.move_right(float(recv_inst_tok[1]))
        elif (recv_inst_tok[0] == 'ARM') :
            print("arm " + recv_inst_tok[1:4])
            # TODO: ARM arg[1] arg[2] arg[3] state
            state = int(recv_inst_tok[4])

            # TODO : Implement
            if (state == 0) : # GRAB
                pass
            else : # Release
                pass

        # TODO: Remove (Test Purpose Only)
        time.sleep(2)

        # Noticing Current Task is totally done.
        clientSock.sendall("DONE".encode())

if __name__ == "__main__" :
    run_client()