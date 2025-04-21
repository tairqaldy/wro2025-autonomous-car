# steering.py – Control for the steering motor (front steering on port B).
# Provides functions to steer left, steer right, and straighten the wheels.
from buildhat import Motor
from config import MAX_TURN_ANGLE, STRAIGHT_ANGLE
import time

# Steering motor on port B
steering_motor = Motor('B')

def steer_left():
    """Turn the wheels to the left briefly, then return to center."""
    print("↩️ Поворот влево (Steering left)")  # debug print
    steering_motor.run_to_position(-MAX_TURN_ANGLE, speed=100)
    time.sleep(0.3)
    steer_straight()

def steer_right():
    """Turn the wheels to the right briefly, then return to center."""
    print("↪️ Поворот вправо (Steering right)")
    steering_motor.run_to_position(MAX_TURN_ANGLE, speed=100)
    time.sleep(0.3)
    steer_straight()

def steer_straight():
    """Straighten the wheels (return steering to straight angle)."""
    print("⬆️ Ровное положение (Steering straight)")
    steering_motor.run_to_position(STRAIGHT_ANGLE, speed=100)
    time.sleep(0.3)
    print(f"📍 Current steering position: {steering_motor.get_position()}°")
