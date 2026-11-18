from adafruit_motorkit import MotorKit


class MotorHat:
    """
    Adapter for the Adafruit DC & Stepper Motor HAT (through MotorKit).

    Create one per HAT, then call output(n) for each motor terminal (1 to 4).
    The returned function takes a value from -1.0 to 1.0, which is what
    MotorDriver expects.
    """

    def __init__(self, i2c=None):

        # Passing an existing i2c bus (e.g. shared with the IMU) is optional
        if i2c is not None:
            self.kit = MotorKit(i2c=i2c)
        else:
            self.kit = MotorKit()

    def output(self, number):

        if number not in (1, 2, 3, 4):
            raise ValueError("The HAT has motor terminals 1 to 4")

        motor = getattr(self.kit, f"motor{number}")

        def write(value):
            motor.throttle = value

        return write
