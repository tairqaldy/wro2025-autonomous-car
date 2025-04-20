# config.py
# Global parameters for all robot modules

# Movement parameters
DEFAULT_SPEED = 70  # Base speed for normal operation
FAST_SPEED = 70     # Speed for high-speed mode

# Steering parameters
TURN_ANGLE = 25              # Maximum steering angle for turns
STEER_CORRECTION_ANGLE = 10  # Angle for minor course corrections

# Wall following parameters
TARGET_DISTANCE_MM = 300     # Target distance from wall in millimeters
TOLERANCE_MM = 15           # Acceptable deviation from target distance

# Color codes for line following
BLUE = "blue"    # Left turn indicator
ORANGE = "orange" # Special marker
GREEN = "green"   # Special marker
RED = "red"      # Right turn indicator

# Race parameters
TURNS_PER_LAP = 4  # Number of turns in one complete lap
TOTAL_LAPS = 3     # Total number of laps to complete