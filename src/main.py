# ============================================================
# MAIN CONTROL LOOP
# ------------------------------------------------------------
# Central program execution and hardware initialization.
# Initializes motors, encoders, and IMU; continuously scans
# sensors, updates the current position, and calls the
# trajectory planning function.
# ============================================================

### finding path
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
### needed for every file we run

from trajectories import get_trajectory # or import trajectories
from drive import setupMotors, setupEncoder, setupIMU

def setup():
    """Initialize motors, encoders, and IMU."""
    setupMotors()
    setupEncoder()
    setupIMU()

def main():
    """Scan sensors to update position, get trajectory, update control."""


    trajectory = get_trajectory()
    print(f"Current trajectory: {trajectory}")

if __name__ == "__main__":
    setup()
    while True:
        main()
