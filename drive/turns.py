# turns.py – Turn maneuver implementations using drive and steering motors and ultrasonic sensors.

import time, logging
from drive.motors import drive_forward, stop_all
from drive.steering import steering_motor, steer_straight
from sensors.ultrasonic_left import get_distance_left
from sensors.ultrasonic_right import get_distance_right
from config import DEFAULT_SPEED, MAX_TURN_ANGLE

def turn_left():
    """Execute a left turn maneuver: steer left and move forward until the left sensor sees a wall again."""
    logging.info("↩️ Initiating left turn maneuver")
    # Turn wheels fully to the left
    steering_motor.run_to_position(-MAX_TURN_ANGLE, speed=50)
    # Start moving forward
    drive_forward(speed=DEFAULT_SPEED)
    # Continue until left sensor detects a wall again (distance becomes available)
    start_time = time.time()
    while True:
        dist = get_distance_left()
        if dist != -1:
            # Wall detected on the left side again – turn is complete
            break
        # Safety timeout to avoid infinite loop (in case of unexpected scenario)
        if time.time() - start_time > 5.0:
            logging.warning("⌛ Left turn timeout: no wall detected within 5 seconds")
            break
        time.sleep(0.05)
    # Stop movement and straighten wheels after turn
    stop_all()
    steer_straight()
    logging.info("✅ Left turn completed")

def turn_right():
    """Execute a right turn maneuver: steer right and move forward until the right sensor sees a wall again."""
    logging.info("↪️ Initiating right turn maneuver")
    steering_motor.run_to_position(MAX_TURN_ANGLE, speed=50)
    drive_forward(speed=DEFAULT_SPEED)
    start_time = time.time()
    while True:
        dist = get_distance_right()
        if dist != -1:
            break
        if time.time() - start_time > 5.0:
            logging.warning("⌛ Right turn timeout: no wall detected within 5 seconds")
            break
        time.sleep(0.05)
    stop_all()
    steer_straight()
    logging.info("✅ Right turn completed")
