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

## -- Shared Objects (Connection Infos) --
# Shared Objects are often implemented by inner class, as an encapsulated models.
# Shared Objects are private to others.
# These shared objects must be modified by public methods in class.
# Refer to Operation System Class (CSED312)
class ConnectionInfos :
    def __init__ (self) :
        self.armList_conn = []
        self.armList_inst = []

        # (sema_isHeld, sema_isChanged)
        self.armList_condvar = []

        # Locks for Critical Sections
        self.lock = threading.Lock()
    def action_conn(self, conn):
        self.lock.acquire()

        # Adding current connection to the list.
        self.armList_conn.append(conn)
        self.armList_inst.append(None)

        # condVar_isChanged
        condvar_isChanged = threading.Condition(self.lock)
        self.armList_condvar.append(condvar_isChanged)

        # For Iterating while loop, get the instructions from image
        while True :
            # <ASSUMPTIONS>
            # TODO : Connect ROBOT ARM IN IMAGES and ROBOT ARM CONNECTED BY SOCKET
            ### TODO : Assumptions must be implemented correctly! (By Color)

            # ------------------------------
            # Fetch position of current robot by CVs
            # Calculate the next instructions
            nextInstruction = self.armList_inst[robot_idx]
            # ------------------------------

            # TODO : Exit Condition (Exit Instruction) or All Tasks Done
            ### TODO : What should be done in exit condition?
            # TODO : Send instructions if valid
            conn.send(nextInstruction)

            # After one task is finished, the client will send a message "INST_DONE"
            # If it is not "INST_DONE", then it should be terminated
            end_msg = conn.recv(MAX_BUF_SIZE)
            end_msg = end_msg.decode('utf-8')

            if (end_msg == "INST_DONE") :
                condvar_isChanged.wait()
            else :
                # Wrong End Message :: Break the loop and exit
                # TODO : Post-Process Needed?
                self.lock.release()
                break
        self.lock.release()
    def update_instruction(self):
        self.lock.acquire()

        # By Assumption... We know the robot index (robot_idx)
        # Update New Instructions allocated by Task Management
        nextInstruction = fetchInstruction (robot_idx)

        self.armList_inst[robot_idx] = nextInstruction
        self.armList_condvar[robot_idx].notify()

        self.lock.release()

conn_status = ConnectionInfos()
## -- Shared Objects --

# Connection Handler
def connection_handler(conn, addr, ):
    # First line is the module info
    conn_info = conn.recv (MAX_BUF_SIZE)
    # Data Decoding
    conn_info = conn_info.decode()

    # Actions for Robo_arms
    conn_status.action_conn(conn)

def run_server():
    serverSock = socket.socket()
    serverSock.bind(('', SERVER_PORT))
    while True:
        # Consideration of Camera (+ 1)
        serverSock.listen(MAX_ROBOT_CONNECTED + 1)
        conn, addr = serverSock.accept()
        t = threading.Thread(target=connection_handler, args=(conn, addr))
        t.start()
    sock.close()

if __name__ == '__main__':
    run_server()
