# ============================================================
# MAIN CONTROL LOOP
# ------------------------------------------------------------
# Central program execution and hardware initialization.
# Initializes motors, encoders, and IMU; continuously scans
# sensors, updates the current position, and calls the
# trajectory planning function.
# ============================================================

from trajectories import get_trajectory

def main():
    trajectory = get_trajectory()
    print(f"Current trajectory: {trajectory}")

if __name__ == "__main__":
    main()
