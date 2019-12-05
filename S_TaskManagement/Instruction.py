from enum import Enum

class InstType (Enum):
    INST_FORWARD = 0
    INST_RIGHT = 1
    INST_ROTATE = 2
    INST_ARM = 3


# return str(new_inst_arm) -> Change into String
class Instruction :
    def __init__(self, inst_type_str, args):
        if (inst_type_str == 'FORWARD') :
            self.inst_type = InstType.INST_FORWARD
        elif (inst_type_str == 'RIGHT') :
            self.inst_type = InstType.INST_RIGHT
        elif (inst_type_str == 'ROTATE') :
            self.inst_type = InstType.INST_ROTATE
        elif (inst_type_str == 'ARM') :
            self.inst_type = InstType.INST_ARM
        else :
            pass # Not Reached
        self.args = args

    def getInstType(self):
        return self.inst_type
    def getArgs(self):
        return self.args

    def __str__(self):
        if (self.inst_type == InstType.INST_FORWARD) :
            return ('FORWARD ' + str(self.args[0]))
        elif (self.inst_type == InstType.INST_RIGHT):
            return ('RIGHT ' + str(self.args[0]))
        elif (self.inst_type == InstType.INST_ROTATE):
            return ('ROTATE ' + str(self.args[0]))
        elif (self.inst_type == InstType.INST_ARM):
            return ('ARM ' + str(self.args[0]) + ' ' + str(self.args[1]) + ' ' + str(self.args[2]) + ' ' + str(self.args[3]))
        else:
            pass  # Not Reached