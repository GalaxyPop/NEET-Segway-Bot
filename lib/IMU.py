import math
import time

# Index of each axis in the gyro tuple
AXIS_INDEX = {"x": 0, "y": 1, "z": 2}


def quaternion_to_euler(x, y, z, w):
    """Convert a quaternion (x, y, z, w) to (roll, pitch, yaw) in radians.

    Roll is rotation about x, pitch about y, yaw about z.
    """
    roll = math.atan2(2 * (w * x + y * z), 1 - 2 * (x * x + y * y))
    pitch = math.asin(max(-1.0, min(1.0, 2 * (w * y - z * x))))
    yaw = math.atan2(2 * (w * z + x * y), 1 - 2 * (y * y + z * z))

    return roll, pitch, yaw


class IMUTilt:
    """Sensor-agnostic tilt angle and rate.

    Takes a quaternion (x, y, z, w) and a gyro tuple (x, y, z) in rad/s
    from any driver, the same way EncoderVelocity takes raw counts.
    """

    def __init__(self, tilt_axis="y", tau=0.0, invert=False):

        # Which axis the robot tips about, and which direction is positive
        self.axis = AXIS_INDEX[tilt_axis]
        self.sign = -1.0 if invert else 1.0

        # Filter parameters (tau = 0 disables the filter)
        self.tau = tau

        # Initialize tracking variables
        self.offset = 0.0
        self.last_check = time.perf_counter()

        self.angle = 0.0
        self.rate = 0.0
        self.filtered_rate = 0.0

    def _raw_angle(self, quaternion):

        euler = quaternion_to_euler(*quaternion)

        return self.sign * euler[self.axis]

    def get_angle(self, quaternion):

        # Tilt angle in radians, relative to the zeroed balance point
        self.angle = self._raw_angle(quaternion) - self.offset

        return self.angle

    def get_rate(self, gyro):

        current_time = time.perf_counter()
        check_dt = current_time - self.last_check

        # Tilt rate in rad/s
        self.rate = self.sign * gyro[self.axis]

        # First-order low-pass filter
        denominator = self.tau + check_dt

        if denominator > 0:
            alpha = check_dt / denominator
        else:
            alpha = 1.0

        self.filtered_rate += alpha * (self.rate - self.filtered_rate)

        self.last_check = current_time

        return self.filtered_rate

    def zero_angle(self, quaternion):

        # Call while the robot is held at its balance point
        self.offset = self._raw_angle(quaternion)

    def reset_filter(self):

        self.filtered_rate = 0.0
        self.last_check = time.perf_counter()
