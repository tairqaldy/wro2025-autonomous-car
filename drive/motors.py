# motors.py – Control for the drive motor (rear wheel motor on port A).
from buildhat import Motor
from time import sleep
from config import DRIVE_SPEED

rear_motor = Motor('A')  # Initialize motor on port A

def drive_forward(speed=DRIVE_SPEED, duration=None):
    """Start driving forward at the given speed. If duration is provided, drive for that time and then stop."""
    rear_motor.start(speed)
    if duration:
        sleep(duration)
        stop_all()

def drive_backward(speed=DRIVE_SPEED, duration=None):
    """Start driving backward at the given speed. If duration is provided, drive for that time and then stop."""
    rear_motor.start(-speed)
    if duration:
        sleep(duration)
        stop_all()

def stop_all():
    """Stop the drive motor."""
    rear_motor.stop()
