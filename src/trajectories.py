# ============================================================
# TRAJECTORY GENERATION
# ------------------------------------------------------------
# Defines the desired motion paths: STILL, LEFT, RIGHT, and
# CIRCLE. Selects the active trajectory and calculates the
# desired position (xd) for the controller to follow.
# ============================================================

import numpy as np

trajectory = "STILL"
# trajectory = "LEFT"
# trajectory = "RIGHT"
# trajectory = "CIRCLE"


def get_trajectory():
    return trajectory

def get_desired_position(trajectory):
    """Return the desired vector
    xd = [theta_w,d; theta'_w,d; theta_b,d; theta'_b,d]
    for the given trajectory."""

    if trajectory == "STILL":
        return np.array([0, 0, 0, 0])
    elif trajectory == "LEFT":
        pass
    elif trajectory == "RIGHT":
        pass
    elif trajectory == "CIRCLE":
        pass
    else:
        pass

def follow_trajectory(xd):
    """Given the desired position:
    xd = [theta_w,d; theta'_w,d; theta_b,d; theta'_b,d]
    update the controller to follow the trajectory.
    """
    pass
