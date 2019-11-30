# Referenced by ...
# https://docs.python.org/3/library/signal.html
# https://python.bakyeono.net/chapter-3-4.html
# https://docs.python.org/3/library/socket.html#socket.timeout
# https://docs.python.org/ko/3.8/library/os.html#os.WNOHANG
import threading
import signal
import os
import sys
from PyQt5.QtWidgets import QApplication

import S_ServerSocket.ServerSocket as ServerSocket
from S_CameraVision.ImageManager import ImageManager
from S_CameraVision.ImageDetection import UpdatePositionClass
from S_CameraVision.ImageDetection import saveImages
from S_ServerSocket.SharedRoboList import SharedRoboList
from S_TaskManagement.TaskManager import TaskManager
from S_GUI.GUIManager import MainWindow

# Task Manager
tm = None
# Image Manager
im = None
im_pos = None
# GUI Manager
gm = None
# Shared Robot Information List
robot_status = None

if __name__ == "__main__" :
    # Initiation of GUI & GUI Manager
    app = QApplication(sys.argv)

    gm = MainWindow()
    gm.show()

    # Initiation of ImageManager, TaskManager, and SharedRoboList
    im = ImageManager()
    im_pos = UpdatePositionClass()
    im_pos.updated_image_conn.connect(gm.gui_update_image_conn)

    tm = TaskManager()
    tm.updated_robot_info_conn.connect(gm.gui_update_robot_info_conn)
    tm.updated_progress.connect(gm.gui_update_progress)

    robot_status = SharedRoboList()
    robot_status.updated_image_connclose.connect(gm.gui_update_image_connclose)
    robot_status.updated_robot_info_connclose.connect(gm.gui_update_robot_info_connclose)
    robot_status.connection_ended.connect(gm.manage_grandchild)

    # Extra Initiation - Registering Function
    gm.gui_extra_initiation(robot_status)

    # Execution of saveImages() by Multi-threading
    t = threading.Thread(target=saveImages, args=(im, ))
    t.start()
    gm.t_child_saveImages = t

    # Execution of Server Loop by Multi-threading
    t = threading.Thread(target=ServerSocket.run_server, args=(tm, im, im_pos, gm, robot_status))
    t.start()
    gm.t_child_runServer = t

    # Execution of GUIs
    sys.exit(app.exec_())