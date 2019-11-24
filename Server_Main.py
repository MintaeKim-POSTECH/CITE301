# Referenced by ...
# https://docs.python.org/3/library/signal.html
import threading
import signal
from S_ServerSocket import ServerSocket

# --- Import S_CameraVision/ImageManager.py & ImageDetection.py ---
import os
import sys
path_for_CV = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
path_for_CV = os.path.join(path_for_CV, 'S_CameraVision')
sys.path.append(path_for_CV)

from ImageManager import ImageManager
from ImageDetection import saveImages
# --- Import S_CameraVision/ImageManager.py & ImageDetection.py ---

# Thread t
t_child_saveImages = None
t_child_runServer = None
# Child Thread Lists
t_grandchild_list = None
# Image Manager
im = None

## According to the python docs,
## Python signal handlers are always executed in the main Python thread,
## even if the signal was received in another thread.
def sigint_handler(sig, frame) :
    signal.pthread_kill(t_child_saveImages, signal.SIGKILL)
    for t_grandchild in t_grandchild_list :
        signal.pthread_kill(t_grandchild, signal.SIGKILL)
    signal.pthread_kill(t_child_runServer, signal.SIGKILL)
    sys.exit(0)

def sigchld_handler(sig, frame):
    dead_thread_pid = os.waitpid(-1, 0)
    for t_grandchild in t_grandchild_list :
        if (t_grandchild == dead_thread_pid) :
            t_grandchild_list.remove(t_grandchild)
            return

    if (t_child_saveImages == dead_thread_pid) :
        t_child_saveImages = None
    elif (t_child_runServer == dead_thread_pid) :
        t_child_runServer = None


if __name__ == "__main__" :
    signal.signal(signal.SIGINT, sigint_handler)
    signal.signal(signal.SIGCHLD, sigchld_handler)

    # Initiation of ImageManager
    im = ImageManager()

    # Initiation of t_grandchild
    t_grandchild_list = []

    # Execution of saveImages() by Multi-threading
    t = threading.Thread(target=saveImages, args=(im,))
    t.start()
    t_child_saveImages = t

    # Execution of Server Loop by Multi-threading
    t = threading.Thread(target=ServerSocket.run_server, args=(im, t_grandchild_list))
    t.start()
    t_child_runServer = t

    # Wait until all the tasks are finished normally.
    t_child_runServer.join()
    signal.pthread_kill(t_child_saveImages, signal.SIGKILL)
    sys.exit(0)

