# Referenced by...
# https://doc.qt.io/qtforpython/tutorials/basictutorial/uifiles.html

import yaml
import math
import threading
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import *

from S_GUI.GUI import Ui_MainWindow
from S_RoboticArmControl.Elements import RobotPhase
from S_TaskManagement.Instruction import InstType
# Configurations
config = yaml.load(open("./Config.yaml", 'r'), Loader=yaml.FullLoader)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # ProgressBar Signal
        self.progress_tot_val = 0
        self.ui.progress_tot.setValue(self.progress_tot_val)

        # Initial Image Fetched
        qPixmapVar_bg = QPixmap("./S_GUI/Images/bg_img.jpg")
        qPixmapVar_bg = qPixmapVar_bg.scaledToWidth(1600)
        self.ui.bg_img.setPixmap(qPixmapVar_bg)
        self.ui.bg_img.repaint()
        qPixmapVar_l1 = QPixmap("./S_GUI/Images/Loading.png")
        self.ui.robo0_img.setPixmap(qPixmapVar_l1)
        self.ui.robo0_img.repaint()
        qPixmapVar_l2 = QPixmap("./S_GUI/Images/Loading.png")
        self.ui.robo1_img.setPixmap(qPixmapVar_l2)
        self.ui.robo1_img.repaint()

        # Locks for Image
        self.lock = threading.Lock()

    # Extra Initiation
    def gui_extra_initiation(self, robot_status):
        self.ui.button_start.registerButtonHandler(robot_status.setProcessRunning, 1)
        self.ui.button_stop.registerButtonHandler(robot_status.setProcessRunning, 0)

        self.gui_update_robot_info(robot_status, 0)
        self.gui_update_robot_info(robot_status, 1)

    def gui_update_image_connclose(self, robot_obj):
        self.lock.acquire()
        robot_num = robot_obj.get_robo_num()
        qPixmapVar_l = QPixmap("./S_GUI/Images/Loading.png")
        if (robot_num == 0):
            self.ui.robo0_img.setPixmap(qPixmapVar_l)
            self.ui.robo0_img.repaint()
        else :
            self.ui.robo1_img.setPixmap(qPixmapVar_l)
            self.ui.robo1_img.repaint()
        self.lock.release()


    def gui_update_image(self, robot_obj, new_image_dir):
        self.lock.acquire()
        robot_num = robot_obj.get_robo_num()
        qPixmapVar_newImage = QPixmap(new_image_dir)
        qPixmapVar_newImage = qPixmapVar_newImage.scaledToWidth(config["RESOLUTION_WIDTH_GUI"])

        if (robot_num == 0) :
            self.ui.robo0_img.setPixmap(qPixmapVar_newImage)
            self.ui.robo0_img.repaint()
        elif (robot_num == 1):
            self.ui.robo1_img.setPixmap(qPixmapVar_newImage)
            self.ui.robo1_img.repaint()
        self.lock.release()

    def gui_update_robot_info(self, robot_status, robot_num):
        isConnected = robot_status.isRunning(robot_num)
        if (robot_num == 0) :
            if (isConnected == True) :
                robot0 = robot_status.getRobotEntry(robot_num)
                state_raw, pos_raw, ongoing_inst_raw, next_inst_raw = robot0.getInformation()
                state, pos, ongoing_inst, next_inst = self.tostring(state_raw, pos_raw, ongoing_inst_raw, next_inst_raw)
                self.ui.robo0_dat_state.setText(state)
                self.ui.robo0_dat_pos.setText(pos)
                self.ui.robo0_dat_inst_on.setText(ongoing_inst)
                self.ui.robo0_dat_inst_next.setText(next_inst)
            else :
                self.ui.robo0_dat_state.setText("Disconnected")
                self.ui.robo0_dat_pos.setText("Disconnected")
                self.ui.robo0_dat_inst_on.setText("Disconnected")
                self.ui.robo0_dat_inst_next.setText("Disconnected")
        elif (robot_num == 1) :
            if (isConnected == True):
                robot1 = robot_status.getRobotEntry(robot_num)
                state_raw, pos_raw, ongoing_inst_raw, next_inst_raw = robot1.getInformation()
                state, pos, ongoing_inst, next_inst = self.tostring(state_raw, pos_raw, ongoing_inst_raw, next_inst_raw)
                self.ui.robo1_dat_state.setText(state)
                self.ui.robo1_dat_pos.setText(pos)
                self.ui.robo1_dat_inst_on.setText(ongoing_inst)
                self.ui.robo1_dat_inst_next.setText(next_inst)
            else :
                self.ui.robo1_dat_state.setText("Disconnected")
                self.ui.robo1_dat_pos.setText("Disconnected")
                self.ui.robo1_dat_inst_on.setText("Disconnected")
                self.ui.robo1_dat_inst_next.setText("Disconnected")

    def gui_update_robot_info_conn(self, robot_obj):
        state_raw, pos_raw, ongoing_inst_raw, next_inst_raw = robot_obj.getInformation()
        state, pos, ongoing_inst, next_inst = self.tostring(state_raw, pos_raw, ongoing_inst_raw, next_inst_raw)
        robot_num = robot_obj.get_robo_num()
        if (robot_num == 0) :
            self.ui.robo0_dat_state.setText(state)
            self.ui.robo0_dat_pos.setText(pos)
            self.ui.robo0_dat_inst_on.setText(ongoing_inst)
            self.ui.robo0_dat_inst_next.setText(next_inst)
        elif (robot_num == 1) :
            self.ui.robo1_dat_state.setText(state)
            self.ui.robo1_dat_pos.setText(pos)
            self.ui.robo1_dat_inst_on.setText(ongoing_inst)
            self.ui.robo1_dat_inst_next.setText(next_inst)

    def gui_update_progress(self, brickListManager):
        self.progress_tot_val = brickListManager.get_progress_rate()

    def tostring(self, state_raw, pos_raw, ongoing_inst_raw, next_inst_raw):
        # 1. State
        if (state_raw == RobotPhase.STOP) :
            state = "Stopped"
        elif (state_raw == RobotPhase.MOVING) :
            state = "Moving"
        elif (state_raw == RobotPhase.LIFTING) :
            state = "Lifting"
        else :
            state = "Returning, Heading to Initial Position"

        # 2. Position
        robot_position = pos_raw.getPos()
        robot_direction = pos_raw.getDir()
        pos = "X: " + str(robot_position[0]) + " Y: " + str(robot_position[1]) + " Degree: "

        if (robot_direction[1] == 0) :
            if (robot_direction[0] == 1) :
                pos += '90˚'
            elif (robot_direction[0] == -1) :
                pos += '270˚'
        else :
            pos += str(math.degrees(math.atan2(robot_direction[1], robot_direction[0]))) + "˚"

        return state, pos, self.tostring_inst(ongoing_inst_raw), self.tostring_inst(next_inst_raw)

    def tostring_inst(self, inst_raw):
        # 3. Instruction
        inst_type = inst_raw.getInstType()
        inst_args = inst_raw.getArgs()
        if (inst_type == InstType.INST_FORWARD) :
            if (inst_args[0] > 0) :
                inst = 'Moving ' + str(inst_args[0]) + 'mm FORWARD'
            else :
                inst = 'Moving ' + str(abs(inst_args[0])) + 'mm BACKWARD'
        elif (inst_type == InstType.INST_RIGHT) :
            if (inst_args[0] > 0):
                inst = 'Moving ' + str(inst_args[0]) + 'mm RIGHT'
            else:
                inst = 'Moving ' + str(abs(inst_args[0])) + 'mm LEFT'
        elif (inst_type == InstType.INST_RIGHT) :
            if (inst_args[0] > 0):
                inst = 'Moving ' + str(inst_args[0]) + '˚ CLOCKWISE'
            else:
                inst = 'Moving ' + str(abs(inst_args[0])) + '˚ COUNTER-CLOCKWISE'
        else :
            if (inst_args[3] == 0):
                inst = 'Using Robot Arm with Angle ' + str(inst_args[0]) + "˚, " + str(inst_args[1]) + "˚, " + str(inst_args[2]) + "˚ and GRAB"
            else :
                inst = 'Using Robot Arm with Angle ' + str(inst_args[0]) + "˚, " + str(inst_args[1]) + "˚, " + str(inst_args[2]) + "˚ and RELEASE"

        return inst