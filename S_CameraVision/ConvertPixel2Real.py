import numpy as np
import yaml

# Configurations
config = yaml.load(open("./Config.yaml", 'r'), Loader=yaml.FullLoader)

## Assumption
'''
In Final Demonstration, Camera would shoot the situation in this direction.
 --------------------------------
 | OOOOOOOOO  Blocks  OOOOOOOOO |
 |                              |
 |                              |
 |   Robo1              Robo2   |
 |                              |
 |            Target            |
 |                              |
 --------------------------------
'''

# Conversion between Pixel # in Image to Real Coordination
# Used in ImageDetection
def Pixel2Real (pos_pixel):
    return np.ndarray.tolist(np.array(pos_pixel) * config["MM_PER_PIXEL"])

# Conversion between Real Coordination to Pixel # in Image
# Used in GUIs
def Real2Pixel (pos_real_mm):
    return np.ndarray.tolist(np.array(pos_real_mm) / config["MM_PER_PIXEL"])