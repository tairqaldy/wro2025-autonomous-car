# config.py
# Global parameters for all robot modules

# === Movement Parameters ===
DEFAULT_SPEED = 70
PARKING_SPEED = 30
MIN_SPEED = 30
MAX_SPEED = 100

# === Steering Configuration ===
STRAIGHT_ANGLE = 0            # Steering straight angle (default)
MAX_TURN_ANGLE = 30           # Maximum rotation for front steering (degrees)

# === Ultrasonic Sensor Settings ===
TARGET_DISTANCE_MM = 300      # Desired wall distance in mm (centered)
TOLERANCE_MM = 10             # Acceptable range for error

# === Lap Logic (optional for speed_run) ===
TURNS_PER_LAP = 4
TOTAL_LAPS = 3

# === Timing ===
WALL_CORRECTION_DELAY = 0.1
TURN_DELAY = 0.5
PARKING_DELAY = 1.0

# === USB Camera Settings ===
CAMERA_INDEX = 0  # Default webcam index for OpenCV
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# === Debug ===
DEBUG_MODE = True
