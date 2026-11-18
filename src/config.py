# ============================================================
# CONFIGURATION
# ------------------------------------------------------------
# Centralized settings and constants for the project.
# Update values here rather than modifying core logic.
# ============================================================

# IMU
IMU_TILT_AXIS = "y"             # axis the robot tips about; depends on mounting
IMU_INVERT = False              # flip if forward tilt reads negative
IMU_TAU = 0.005                 # rate filter time constant (s); 0 disables
IMU_REPORT_INTERVAL_US = 5000   # 200 Hz
