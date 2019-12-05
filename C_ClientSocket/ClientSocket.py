from socket import *
from os.path import expanduser
import yaml
import time

# from C_Motor.Car import Car
# from C_RobotArm.RobotArmClient import armClient

# Configurations
home = expanduser("~")
try :
    config = yaml.load(open(home + "/Desktop/CITE301/Config.yaml", 'r'), Loader=yaml.FullLoader)
except :
    config = yaml.load(open("./Config.yaml", 'r'), Loader=yaml.FullLoader)

def run_client() :
    clientSock = socket(AF_INET, SOCK_STREAM)
    clientSock.connect((config["SERVER_IP_ADDR"], config["SERVER_PORT"]))

    # New Car Module
    # car = Car()

    # robotArm=armClient(config["GPIO_ARM_DIRPINS"],config["GPIO_ARM_STPPINS"],config["ROBOTARM_MIN_ANGLES"],config["ROBOTARM_MAX_ANGLES"],config["GPIO_SERVO_PIN"])

    # Client Flow 1 : Send Robot_Arm Number & Color Data
    infoDat = str(config["ROBOT_ARM_NUM"]) + " " + str(config["ROBOT_ARM_HUE"]) + " "
    infoDat += str(config["INIT_POS"][0]) + " " + str(config["INIT_POS"][1])

    try :
        clientSock.sendall(infoDat.encode())
    except BrokenPipeError:
        time.sleep(2)
        print("Broken Pipe")
        return

    # Client Flow 2 : Iteration with While Loop, Executing action for robot arm instructions
    while (True) :
        try :
            recv_inst = clientSock.recv(config["MAX_BUF_SIZE"]).decode()
        except BrokenPipeError:
            time.sleep(2)
            print ("Broken Pipe")
            break

        recv_inst_tok = recv_inst.split(' ')
    
        if (recv_inst_tok[0] == 'ROTATE') :
            print ("rotate " + recv_inst_tok[1])
            # car.rotate(float(recv_inst_tok[1]))
        elif (recv_inst_tok[0] == 'FORWARD') :
            print("forward " + recv_inst_tok[1])
            # car.move_forward(float(recv_inst_tok[1]))
        elif (recv_inst_tok[0] == 'RIGHT') :
            print("right " + recv_inst_tok[1])
            # car.move_right(float(recv_inst_tok[1]))
        elif (recv_inst_tok[0] == 'ARM') :
            # print("arm"+recv_inst_tok[4])
            # print("arm " + recv_inst_tok[1:4])
            # TODO: ARM arg[1] arg[2] arg[3] state
            state = int(recv_inst_tok[4])
            if (state == 0) : # GRAB
                print("grap")
                # robotArm.work([float(recv_inst_tok[1]),float(recv_inst_tok[2]),float(recv_inst_tok[3])], True)
            else : # Release
                print("release")
                # robotArm.work([float(recv_inst_tok[1]),float(recv_inst_tok[2]),float(recv_inst_tok[3])], False)

        # Noticing Current Task is totally done.
        try :
            clientSock.sendall("DONE".encode())
        except BrokenPipeError:
            time.sleep(2)
            print ("Broken Pipe")
            break

if __name__ == "__main__" :
    run_client()
