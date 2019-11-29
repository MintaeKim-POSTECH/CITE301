# Referenced by...
# https://doc.qt.io/qtforpython/tutorials/basictutorial/uifiles.html

import sys
import yaml
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import *
from S_GUI.GUI import Ui_MainWindow

# Configurations
config = yaml.load(open("./Config.yaml", 'r'), Loader=yaml.FullLoader)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # ProgressBar Signal
        self.progress_tot_val = 0
        self.ui.progress_tot.valueChanged.connected(self.progress_tot_val)

        # Initial Image Fetched
        qPixmapVar_bg = QPixmap().load("./S_GUI/Images/bg_img.jpg").scaledToHeight(930)
        self.ui.bg_img.setPixmap(qPixmapVar_bg)
        self.ui.bg_img.repaint()
        qPixmapVar_l1 = QPixmap().load("./S_GUI/Images/Loading.png")
        self.ui.robo0_img.setPixmap(qPixmapVar_l1)
        self.ui.robo0_img.repaint()
        qPixmapVar_l2 = QPixmap().load("./S_GUI/Images/Loading.png")
        self.ui.robo1_img.setPixmap(qPixmapVar_l2)
        self.ui.robo1_img.repaint()

    # Extra Initiation
    def gui_extra_initiation(self, robot_status):
        self.ui.button_start.registerButtonHandler(robot_status.setProcessRunning, 1)
        self.ui.button_stop.registerButtonHandler(robot_status.setProcessRunning, 0)

        self.gui_update_robot_info(robot_status, 0)
        self.gui_update_robot_info(robot_status, 1)

    def gui_update_image(self, robot_obj, new_image_dir):
        robot_num = robot_obj.get_robo_num()
        qPixmapVar_newImage = QPixmap().load(new_image_dir).scaledToWidth(config["RESOLUTION_WIDTH_GUI"])
        if (robot_num == 0) :
            self.ui.robo0_img.setPixmap(qPixmapVar_newImage)
            self.ui.robo0_img.repaint()
        elif (robot_num == 1):
            self.ui.robo1_img.setPixmap(qPixmapVar_newImage)
            self.ui.robo1_img.repaint()

    def gui_update_robot_info(self, robot_status, robot_num):
        isConnected = robot_status.isRunning(robot_num)
        if (robot_num == 0) :
            if (isConnected == True) :
                robot0 = robot_status.getRobotEntry(robot_num)
                self.ui.robo0_dat_state = robot0.get
                self.ui.robo0_dat_pos
                self.ui.robo0_dat_inst_on
                self.ui.robo0_dat_inst_next
            else :
                self.ui.robo0_dat_state
                self.ui.robo0_dat_pos
                self.ui.robo0_dat_inst_on
                self.ui.robo0_dat_inst_next
        elif (robot_num == 1) :
            if (isConnected == True):
                self.ui.robo1_dat_state
                self.ui.robo1_dat_pos
                self.ui.robo1_dat_inst_on
                self.ui.robo1_dat_inst_next
            else :
                self.ui.robo0_dat_state
                self.ui.robo0_dat_pos
                self.ui.robo0_dat_inst_on
                self.ui.robo0_dat_inst_next

    def gui_update_robot_info_conn(self, robot_obj):
        self.ui.robo0_dat_state
        self.ui.robo0_dat_pos
        self.ui.robo0_dat_inst_on
        self.ui.robo0_dat_inst_next

    def gui_update_progress(self, brickListManager):
        self.progress_tot_val = brickListManager.get_progress_rate()
