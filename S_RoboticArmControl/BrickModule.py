import S_RoboticArmControl as rc
from S_RoboticArmControl.Elements import Phase
from S_RoboticArmControl.Elements import Position

minDist = 10.0


class Brick:
    def __init__(self):
        self.src = True
        self.pos = Position()
        self.phase = Phase.NULL
        self.unableStack = 0

    def enable(self):
        self.unableStack = self.unableStack - 1
        if (self.unableStack == 0) :
            self.phase = Phase.ENABLE

    def unable(self):
        self.phase = Phase.UNABLE
        self.unableStack = self.unableStack + 1

    def working(self):
        self.phase = Phase.WORKING

    def done(self):
        self.phase = Phase.DONE

    def getPos(self):
        return self.pos

    def getPhase(self):
        return self.phase

    def getRobotPosForWork(self):
        ret = self.dst.getPos() + self.dst.getDir() * minDist
        return ret

    def __repr__(self):
        return repr((self.pos, self.src))

    def __lt__(self, other):
        if self.src:
            return self.pos.upper(other.pos)
        else:
            return not self.pos.upper(other.pos)


