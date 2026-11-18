import math


class Motor:
    """
    Hardware-independent motor command handling.

    Takes a command from -1.0 (full reverse) to 1.0 (full forward) and sends it,
    scaled and limited, to `output`: any function that accepts a float from
    -1.0 to 1.0. See lib/drivers/MotorHat.py for the Adafruit HAT version.

        hat = MotorHat()
        left = Motor(hat.output(1), max_duty=0.81)
        right = Motor(hat.output(2), max_duty=0.81, invert=True)
    """

    def __init__(self, output, max_duty=1.0, invert=False):

        if not 0.0 < max_duty <= 1.0:
            raise ValueError("max_duty must be greater than 0 and at most 1")

        # Function that sends a value from -1.0 to 1.0 to the hardware
        self.output = output

        # The most the motor should ever get. Set this to (motor rated voltage /
        # supply voltage), e.g. 6.0 / 7.4. A command of 1.0 maps to this value.
        self.max_duty = max_duty

        # Flip direction if the motor is mounted mirrored (e.g. left vs right wheel)
        self.sign = -1.0 if invert else 1.0

        # Last command, as a signed fraction from -1.0 to 1.0
        self.current_duty_cycle = 0.0

        # Start from a known state
        self.stop()

    def drive(self, duty_cycle):
        """
        Drives the motor.

        duty_cycle: Value between -1.0 (full reverse)
                    and 1.0 (full forward).

        Returns the command actually used (after limiting to -1.0 to 1.0).
        """

        # A NaN would slip through min/max as full power, so stop instead
        if not math.isfinite(duty_cycle):
            self.stop()
            return self.current_duty_cycle

        # Constrain the command to the valid range
        duty_cycle = max(-1.0, min(1.0, duty_cycle))
        self.current_duty_cycle = duty_cycle

        # Scale so a full command is the most the motor should ever get
        self.output(self.sign * duty_cycle * self.max_duty)

        return self.current_duty_cycle

    def stop(self):
        """
        Sets the motor output to zero.
        """
        self.current_duty_cycle = 0.0
        self.output(0.0)

    def close(self):
        """
        Stops the motor. Call this when shutting down.
        """
        self.stop()

    def get_current_duty_cycle(self):
        """
        Returns the last command as a signed fraction (-1.0 to 1.0).
        """
        return self.current_duty_cycle

    # Lets you write "with Motor(...) as motor:" so the motor is
    # stopped even if the control loop crashes
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
