import time
import numpy as np

# Counts per revolution at the output shaft for goBILDA 5203 Yellow Jacket motors
# (quadrature, 4x decoding; values from the goBILDA spec sheets)
CPR_30_RPM = 5281.1
CPR_60_RPM = 2786.2
CPR_312_RPM = 537.7


class Encoder:
    """Sensor-agnostic encoder position and velocity.

    Takes the raw encoder count as an argument and returns radians and rad/s.
    The counts must be in the same units as counts_per_revolution (for goBILDA
    that means 4x quadrature decoding).
    """

    def __init__(self, counts_per_revolution, tau=0.01, minimum_velocity=0.01):

        # Conversion from encoder counts to radians
        self.counts_to_radians = 2 * np.pi / counts_per_revolution

        # Filter parameters
        self.tau = tau

        # Slowest speed (rad/s) treated as moving. Anything slower reads as zero.
        self.minimum_velocity = minimum_velocity

        # Initialize tracking variables
        now = time.perf_counter()

        self.offset = 0
        self.last_position = 0
        self.last_change = now
        self.last_check = now

        self.velocity = 0.0
        self.filtered_velocity = 0.0
        self.moving = False

    def get_velocity(self, current_position, current_time=None):

        # current_time is optional so the class can be tested with fake timestamps
        if current_time is None:
            current_time = time.perf_counter()

        change_dt = current_time - self.last_change
        check_dt = current_time - self.last_check

        if current_position != self.last_position and change_dt > 0:

            # New counts: velocity from counts moved over time since the last change
            self.velocity = (
                (current_position - self.last_position)
                * self.counts_to_radians / change_dt
            )

            self.last_position = current_position
            self.last_change = current_time

        elif change_dt > 0:

            # No new counts: the wheel can be going no faster than one count
            # per elapsed time, so the estimate decays instead of snapping to zero
            max_velocity = self.counts_to_radians / change_dt

            if abs(self.velocity) > max_velocity:
                self.velocity = np.sign(self.velocity) * max_velocity

        # Too slow to tell apart from standing still
        if abs(self.velocity) < self.minimum_velocity:
            self.velocity = 0.0

        self.moving = self.velocity != 0.0

        # First-order low-pass filter
        denominator = self.tau + check_dt

        if denominator > 0:
            alpha = check_dt / denominator
        else:
            alpha = 1.0

        self.filtered_velocity += alpha * (
            self.velocity - self.filtered_velocity
        )

        # Let the filter's tail settle to exactly zero when stopped
        if not self.moving and abs(self.filtered_velocity) < self.minimum_velocity:
            self.filtered_velocity = 0.0

        self.last_check = current_time

        return self.filtered_velocity

    def get_position(self, current_position):

        # Position in radians, relative to the last reset
        return (current_position - self.offset) * self.counts_to_radians

    def reset_position(self, current_position=0):

        # Pass the encoder's current count to zero here without touching the
        # hardware counter. Leave it at 0 if you also reset the hardware counter.
        self.offset = current_position
        self.last_position = current_position

        now = time.perf_counter()
        self.last_change = now
        self.last_check = now

        self.velocity = 0.0
        self.filtered_velocity = 0.0
        self.moving = False
