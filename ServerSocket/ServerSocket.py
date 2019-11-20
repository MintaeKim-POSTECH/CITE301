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

class ConnectionInfos :
    def __init__ (self) :
        self.armList_conn = []

        for i in range(config["MAX_ROBOT_CONNECTED"]) :
            self.armList_conn.append(None)

    def action_conn(self, conn, robot_arm_num, robot_arm_color):
        # Adding current connection to the list.
        self.armList_conn[robot_arm_num] = conn

        # For Iterating while loop, get the instructions from image
        while True :
            # Calculate the next instructions by Task Manager
            next_instruction = fetchNextTask(robot_arm_num)

            conn.sendall(next_instruction.decode())
            end_msg = conn.recv(config["MAX_BUF_SIZE"]).decode()

            # TODO: Saving Position Information with CVs
            updatePosition(robot_arm_num, robot_arm_color)

            if (end_msg == "CLIENT_ELIMINATED") :
                break

        # TODO: Reset infos
        self.armList_conn[robot_arm_num] = None

conn_status = ConnectionInfos()

# Connection Handler
def connection_handler(conn, addr, ):
    # Server Flow 1: First line is the Robot Arm Information info
    recv_info = conn.recv(config["MAX_BUF_SIZE"]).decode().split(' ')
    robot_arm_num = int(recv_info[0])
    robot_arm_color = (float(recv_info[1]), float(recv_info[2]), float(recv_info[3]))

    # Server Flow 2: Actions for Robo_arms
    conn_status.action_conn(conn, robot_arm_num, robot_arm_color)

def run_server():
    serverSock = socket.socket()
    serverSock.bind((config["SERVER_IP_ADDR"], config["SERVER_PORT"]))
    while True:
        serverSock.listen(config["MAX_ROBOT_CONNECTED"])
        conn, addr = serverSock.accept()
        t = threading.Thread(target=connection_handler, args=(conn, addr))
        t.start()
    sock.close()

if __name__ == '__main__':
    run_server()


## -- Shared Objects (Connection Infos) --
# Shared Objects are often implemented by inner class, as an encapsulated models.
# Shared Objects are private to others.
# These shared objects must be modified by public methods in class.
# Refer to Operation System Class (CSED312)