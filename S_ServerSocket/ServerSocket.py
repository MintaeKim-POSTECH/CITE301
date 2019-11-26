# Referenced from https://soooprmx.com/archives/8737
# Referenced from https://wayhome25.github.io/python/2017/02/26/py-14-list/
# Referenced from https://codechacha.com/ko/how-to-import-python-files/

# Assume that Server IPs are fixed
# Assume that Camera is connected to Server
# Assume that we can correspond the robot_arm in the images and the robot_arm sockets (Important)

# For Multi-Threading & Usage of Synchronization (Semaphore, Lock)
import threading
import socket
import yaml

# Saving Socket List
SOCKET_LIST = []

# Configurations
config = yaml.load(open("../Config.yaml", 'r'), Loader=yaml.FullLoader)

# --- Import S_RoboticArmControl/RobotControl.py ---
import os
import sys
path_for_roboAC = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
path_for_roboAC = os.path.join(path_for_roboAC, 'S_RoboticArmControl')
sys.path.append(path_for_roboAC)

from RobotControl import Robot
# --- Import S_RoboticArmControl/RobotControl.py ---


# --- Import S_TaskManagement/TaskManager  ---
path_for_tm = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
path_for_tm = os.path.join(path_for_tm, 'S_TaskManagement')
sys.path.append(path_for_tm)

from TaskManager import TaskManager
# --- Import S_TaskManagement/TaskManager  ---


# --- Import S_CameraVision/ImageManager.py & ImageDetection.py ---
path_for_CV = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
path_for_CV = os.path.join(path_for_CV, 'S_CameraVision')
sys.path.append(path_for_CV)

from ImageManager import ImageManager
from ImageDetection import updatePosition
# --- Import S_CameraVision/ImageManager.py & ImageDetection.py ---

class RobotInfos :
    def __init__ (self) :
        self.armList_conn = []
        # Construction of roboInfoList
        self.roboInfoList = []

        for i in range(config["MAX_ROBOT_CONNECTED"]) :
            self.armList_conn.append(None)
            self.roboInfoList.append(None)

    def action_conn_init(self, conn, robot_arm_num, robot_arm_color, robot_arm_init_pos):
        # Adding current connection to the list.
        self.armList_conn[robot_arm_num] = conn
        self.roboInfoList[robot_arm_num] = Robot()
        self.roboInfoList[robot_arm_num].setColorRGB(robot_arm_color)

        self.roboInfoList[robot_arm_num].setInitPos(robot_arm_init_pos)

        # Reset Current Position & Direction Information
        global im
        updatePosition(self.roboInfoList[robot_arm_num], im)

        # TODO: Push Initial Instructions based on Infos (Move to Initial Position)

    def action_conn(self, robot_arm_num):
        # For Iterating while loop, get the instructions from image
        while True :
            # Calculate the next instructions by Task Manager
            ## For CITD III, We need an robo_arm_num infos to seperate two trajectories.
            ## In CITD IV, We will try to generalize for more than three trajectories.
            next_instruction = tm.fetchNextTask(self.roboInfoList[robot_arm_num])

            # If the robot is waiting for the other robot to finish their task,
            # then this robot would be waiting for a new block by a condition variable in BrickListManager.
            # That means if next_instruction is None, which means no instruction left in queue
            # infers that all tasks are done.
            if (next_instruction == None) :
                break

            self.armList_conn[robot_arm_num].sendall(next_instruction.decode())
            end_msg = self.armList_conn[robot_arm_num].recv(config["MAX_BUF_SIZE"]).decode()

            global im
            updatePosition(self.roboInfoList[robot_arm_num], im)
            # TODO: Callibration

        # Exit Condition - Reset infos
        self.armList_conn[robot_arm_num] = None
        self.roboInfoList[robot_arm_num] = None

# Task Manager
tm = None
# Image Manager
im = None
# Robot Status Information
robot_status = None

# Connection Handler
def connection_handler(conn, addr, ):
    # Server Flow 1: First line is the Robot Arm Information info
    recv_info = conn.recv(config["MAX_BUF_SIZE"]).decode().split(' ')
    robot_arm_num = int(recv_info[0])
    # TODO: Already exists? then exit

    robot_arm_color = [float(recv_info[1]), float(recv_info[2]), float(recv_info[3])]
    robot_arm_init_pos = (float(recv_info[4]), float(recv_info[5]))

    # Server Flow 2: Actions for Robo_arms
    robot_status.action_conn_init(conn, robot_arm_num, robot_arm_color, robot_arm_init_pos)
    # TODO : WAIT until user starts
    robot_status.action_conn(robot_arm_num)

def run_server(_im, t_grandchild_list):
    serverSock = socket.socket()
    serverSock.bind((config["SERVER_IP_ADDR"], config["SERVER_PORT"]))

    # Initializing Status Informations & Task Manager
    global tm, im, robot_status
    tm = TaskManager()
    im = _im
    robot_status = RobotInfos()

    # Setting Timeout as 5 seconds
    serverSock.settimeout(5)

    # Server Routine
    while True:
        serverSock.listen(config["MAX_ROBOT_CONNECTED"])
        conn, addr = serverSock.accept()
        t = threading.Thread(target=connection_handler, args=(conn, addr))
        t.start()

        # Adding Current Thread to grandchild thread list.
        t_grandchild_list.append(t)

        # Assuming that if all tasks are done, then there would be time-out!
