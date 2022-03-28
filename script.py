from serial.tools import list_ports 
from pydobot import Dobot 
port = list_ports.comports()[0].device
device = Dobot(port=port, verbose=False)

import time
device.rotate_joint(3, 3, 3, 0.779, wait=True)
