import os
import sys

# --- Import Motor/Car.py ---
path_for_roboAC = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
path_for_roboAC = os.path.join(path_for_roboAC, 'RoboticArmControl')
sys.path.append(path_for_roboAC)

# Modify if this invokes error
from LayerModule import Layer

# --- Import Motor/Car.py ---