import time

import board
import busio
from adafruit_bno08x import BNO_REPORT_GAME_ROTATION_VECTOR, BNO_REPORT_GYROSCOPE
from adafruit_bno08x.i2c import BNO08X_I2C

# BNO085 default I2C address (0x4B if the address jumper is bridged)
DEFAULT_ADDRESS = 0x4A

# Errors the library/bus can raise on a bad read
READ_ERRORS = (RuntimeError, OSError, KeyError)


class BNO085:
    """Thin hardware driver: owns the I2C bus and returns raw readings.

    Quaternion is returned as (x, y, z, w), which is the BNO08x's (i, j, k, real).
    Gyro is returned as (x, y, z) in rad/s.

    If a read fails, the last good reading is returned and read_errors is
    incremented, so the control loop keeps running. Check read_errors to
    detect a sensor that has stopped updating.
    """

    def __init__(self, report_interval_us=5000, i2c=None, address=DEFAULT_ADDRESS):

        if i2c is None:
            i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)

        self.bno = BNO08X_I2C(i2c, address=address)

        # Game rotation vector = orientation without the magnetometer
        self.bno.enable_feature(BNO_REPORT_GAME_ROTATION_VECTOR, report_interval_us)
        self.bno.enable_feature(BNO_REPORT_GYROSCOPE, report_interval_us)

        # Last good readings and failure counter
        self.last_quaternion = (0.0, 0.0, 0.0, 1.0)
        self.last_gyro = (0.0, 0.0, 0.0)
        self.read_errors = 0

        self._wait_for_first_reading()

    def _wait_for_first_reading(self, timeout=2.0):

        # The sensor needs a moment before the first reports arrive
        start = time.perf_counter()

        while True:
            try:
                self.last_quaternion = self.bno.game_quaternion
                self.last_gyro = self.bno.gyro
                return
            except READ_ERRORS:
                if time.perf_counter() - start > timeout:
                    raise RuntimeError("BNO085 did not report data, check wiring/I2C")
                time.sleep(0.01)

    def read_quaternion(self):

        try:
            self.last_quaternion = self.bno.game_quaternion
        except READ_ERRORS:
            self.read_errors += 1

        return self.last_quaternion

    def read_gyro(self):

        try:
            self.last_gyro = self.bno.gyro
        except READ_ERRORS:
            self.read_errors += 1

        return self.last_gyro
