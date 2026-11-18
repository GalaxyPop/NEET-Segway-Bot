### finding path
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
### needed for every file we run

import time

from lib.motor import MotorDriver
from drivers.FIT0450 import MotorHat

# WHEELS OFF THE GROUND for this test
hat = MotorHat()

with MotorDriver(hat.output(1)) as motor:
    for command in (0.3, 0.0, -0.3, 0.0):
        print("drive", command)
        motor.drive(command)
        time.sleep(1.0)
