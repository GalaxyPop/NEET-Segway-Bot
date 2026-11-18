### finding path
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
### needed for every file we run

import math
import time

from drivers.BNO085 import BNO085
from lib.IMU import IMUTilt

sensor = BNO085()
tilt = IMUTilt(tilt_axis="y", tau=0.005)
tilt.zero_angle(sensor.read_quaternion())

while True:
    angle = tilt.get_angle(sensor.read_quaternion())
    rate = tilt.get_rate(sensor.read_gyro())
    print(f"angle {math.degrees(angle):7.2f} deg  rate {math.degrees(rate):8.2f} deg/s  errors {sensor.read_errors}")
    time.sleep(0.02)
