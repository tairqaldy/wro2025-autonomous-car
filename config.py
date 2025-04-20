# config.py
# Global parameters for all robot modules

# Movement parameters
DEFAULT_SPEED = 70    # Base speed for normal operation
FAST_SPEED = 70      # Speed for high-speed mode
PARKING_SPEED = 30   # Speed for parking maneuvers
FORWARD_SPEED = 50   # Speed for basic forward movement
MIN_SPEED = 30       # Minimum speed for precise control
MAX_SPEED = 80       # Maximum safe speed
WALL_FOLLOW_SPEED = 40  # Speed for wall following
WALL_SEARCH_SPEED = 35  # Speed for wall search
COLOR_DETECTION_SPEED = 25  # Speed for color detection
TURN_SPEED = 20      # Speed during turns

# Steering parameters
TURN_ANGLE = 25              # Maximum steering angle for turns
STEER_CORRECTION_ANGLE = 5   # Angle for minor course corrections
PARKING_TURN_ANGLE = 45      # Angle for parking maneuvers
STRAIGHT_ANGLE = 0           # Angle for straight movement
WALL_CORRECTION_ANGLE = 3    # Angle for wall following corrections
SNAKE_TURN_ANGLE = 15        # Angle for snake movement turns

# Wall following parameters
TARGET_DISTANCE_MM = 80      # Target distance from wall in millimeters
TOLERANCE_MM = 5            # Acceptable deviation from target distance
MIN_WALL_DISTANCE = 60      # Minimum safe distance from wall
MAX_WALL_DISTANCE = 100     # Maximum safe distance from wall
CORRECTION_THRESHOLD = 10    # Distance threshold for correction
WALL_SEARCH_TIMEOUT = 5.0   # Timeout for wall search in seconds

# Color codes for line following
BLUE = "blue"      # Left turn indicator
ORANGE = "orange"  # Right turn indicator
GREEN = "green"    # Left obstacle indicator
RED = "red"        # Right obstacle indicator

# Race parameters
TURNS_PER_LAP = 4          # Number of turns in one complete lap
TOTAL_LAPS = 3             # Total number of laps to complete
PARKING_ZONE_LENGTH = 500  # Length of parking zone in millimeters
LINES_PER_LAP = 8          # Number of color lines per lap (4 turns * 2 lines per turn)

# Timing parameters
TURN_DELAY = 0.5          # Delay after turns
OBSTACLE_DELAY = 0.5      # Delay for obstacle processing
WALL_CORRECTION_DELAY = 0.1  # Delay for wall following corrections
PARKING_DELAY = 1.0       # Delay for parking maneuvers
FORWARD_DELAY = 0.05      # Delay for basic forward movement control
WALL_READ_DELAY = 0.05    # Delay between ultrasonic readings
SNAKE_TURN_DELAY = 0.3    # Delay between snake turns
SNAKE_FORWARD_DELAY = 0.5 # Delay for forward movement in snake pattern
COLOR_READ_DELAY = 0.2    # Delay between color readings
TURN_DURATION = 1.2       # Duration of turn movement
COLOR_DETECTION_DURATION = 0.8  # Duration for color detection