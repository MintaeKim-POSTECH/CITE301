# Referenced from https://soooprmx.com/archives/8737

# Assume that Server IPs are fixed
# Assume that Camera is connected to Server
# Assume that we can correspond the robot_arm in the images and the robot_arm sockets (Important)

# For Multi-Threading & Usage of Synchronization (Semaphore, Lock)
import threading
import socket
import yaml
import time

from SharedRoboList import SharedRoboList

# Configurations
config = yaml.load(open("./Config.yaml", 'r'), Loader=yaml.FullLoader)

# Checking Termination Condition
def check_termination(robot_status):
    while True:
        if (robot_status.isTasksDone() == True):
            return
        # Checking for Every 3 Seconds
        time.sleep(5)

    # Further Handling will be processed in the sigchld handler

# Connection Handler
def connection_handler(conn, addr, tm, im, robot_status):
    # Server Flow 1: First line is the Robot Arm Information info
    recv_info = conn.recv(config["MAX_BUF_SIZE"]).decode().split(' ')
    robot_arm_num = int(recv_info[0])
    # Robot_arm_number already running? then exit.
    if (robot_status.isRunning(robot_arm_num)) :
        return

    robot_arm_color = [float(recv_info[1]), float(recv_info[2]), float(recv_info[3])]
    robot_arm_init_pos = [float(recv_info[4]), float(recv_info[5])]

    # Server Flow 2: Actions for Robo_arms
    robot_status.action_conn_init(conn, robot_arm_num, robot_arm_color, robot_arm_init_pos, tm, im)
    robot_status.action_conn(robot_arm_num, tm, im)

def run_server(tm, im, robot_status, t_grandchild_list):
    serverSock = socket.socket()
    serverSock.bind((config["SERVER_IP_ADDR"], config["SERVER_PORT"]))

    # Setting Timeout as 5 seconds
    # serverSock.settimeout(5)
    serverSock.settimeout(None)

    t = threading.Thread(target=check_termination, args=(robot_status, ))
    t.start()

    t_grandchild_list.append((t, "CHECK_TERMINATION"))

    # Server Routine
    while True:
        serverSock.listen(config["MAX_ROBOT_CONNECTED"])
        conn, addr = serverSock.accept()
        t = threading.Thread(target=connection_handler, args=(conn, addr, tm, im, robot_status))
        t.start()

        # Adding Current Thread to grandchild thread list.
        t_grandchild_list.append((t, "CONN"))
