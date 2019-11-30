import threading

from S_RoboticArmControl.Elements import RobotPhase
from S_RoboticArmControl.Elements import Position as pos

class Robot:
    def __init__(self):
        # Robot State & Ongoing Src-Brick/Dst-Brick
        self.phase = RobotPhase.STOP

        self.robot_num = -1
        self.brick_src = None
        self.brick_ongoing = None
        self.brick_dst = None

        # Robot Wheel Information
        self.cur_pos = pos()

        # Instruction Queue
        self.cur_inst = None
        self.next_inst_queue = []

        # Angle Information for Robot Arm
        self.cur_arm_angle = [0.0, 0.0, 0.0]
        self.next_arm_angle = [0.0, 0.0, 0.0]

        # Initial Position
        ## For CITD III, We need an initial position info to seperate two trajectories.
        ## In CITD IV, We will try to generalize for more than three trajectories.
        self.initial_pos = pos()

        # Color
        self.color_rgb = None

        # Locks for File Consistency
        self.lock = threading.Lock()

    def brick_info_move(self, srcBrick):
        self.lock.acquire()
        self.phase = RobotPhase.MOVING

        self.brick_src = srcBrick
        self.lock.release()

    def brick_info_lift(self, dstBrick):
        self.lock.acquire()
        self.phase = RobotPhase.LIFTING

        self.brick_dst = dstBrick
        self.brick_ongoing = self.brick_src
        self.brick_src = None
        self.lock.release()

    def brick_info_comeback(self):
        self.lock.acquire()
        self.phase = RobotPhase.COMEBACK

        self.brick_ongoing = None
        self.brick_dst = None
        self.lock.release()

    def brick_info_fin(self):
        self.lock.acquire()
        self.phase = RobotPhase.STOP
        self.lock.release()

    def isQueueEmpty(self):
        self.lock.acquire()
        l = len(self.next_inst_queue)
        self.lock.release()
        return (l == 0)
    def push_inst(self, new_inst):
        self.lock.acquire()
        self.next_inst_queue.append(new_inst)
        self.lock.release()
    def push_inst_list(self, new_inst_list):
        self.lock.acquire()
        self.next_inst_queue.extend(new_inst_list)
        self.lock.release()
    def pop_inst(self):
        self.lock.acquire()
        if (len(self.next_inst_queue) == 0):
            self.cur_inst = None
            self.lock.release()
            return
        self.cur_inst = self.next_inst_queue[0]
        self.next_inst_queue.remove(self.cur_inst)
        self.lock.release()

    def set_robo_num(self, num):
        self.robot_num = num
    def get_robo_num(self):
        return self.robot_num
    # Initial Position
    ## For CITD III, We need an initial position info to seperate two trajectories.
    ## In CITD IV, We will try to generalize for more than three trajectories.
    def setInitPos(self, init_pos):
        self.lock.acquire()
        init_pos.append(0)
        self.initial_pos.setPos(init_pos)
        self.lock.release()
    def getInitPos(self):
        self.lock.acquire()
        init_pos = self.initial_pos
        self.lock.release()
        return init_pos

    def setPos_position(self, pos):
        self.lock.acquire()
        self.cur_pos.setPos(pos)
        self.lock.release()
    def setPos_angle(self, angle):
        self.lock.acquire()
        self.cur_pos.setDir(angle)
        self.lock.release()
    def getPos(self):
        self.lock.acquire()
        pos = self.cur_pos
        self.lock.release()
        return pos
    def setColorRGB(self, color_rgb):
        self.lock.acquire()
        self.color_rgb = color_rgb
        self.lock.release()
    def getColorRGB(self):
        self.lock.acquire()
        rgb = self.color_rgb
        self.lock.release()
        return rgb
    def getSrcBlock(self):
        self.lock.acquire()
        brick_src=self.brick_src
        self.lock.release()
        return brick_src
    def getOngoingBlock(self):
        self.lock.acquire()
        brick_og = self.brick_ongoing
        self.lock.release()
        return brick_og
    def getDstBlock(self):
        self.lock.acquire()
        brick_dst = self.brick_dst
        self.lock.release()
        return brick_dst
    def getCurrentInst(self):
        self.lock.acquire()
        cur_inst = self.cur_inst
        self.lock.release()
        return cur_inst

    def getInformation(self):
        self.lock.acquire()
        state, pos, ongoing_inst= self.phase, self.cur_pos, self.cur_inst
        if (len(self.next_inst_queue) == 0) :
            next_inst = None
        else :
            next_inst = self.next_inst_queue[0]
        self.lock.release()
        return state, pos, ongoing_inst, next_inst

'''
    def setMotorPin(self):
        pass
    def lift(self, pos):
            # self.nextPos = pos
            # angles = cal.calNextAngle(self.curPos, self.nextPos);
            # self.curPos = pos
            # communicate with robot arm
            # send robot arm the next Angle
        pass
'''