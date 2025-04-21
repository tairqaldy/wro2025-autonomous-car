# motors.py
from buildhat import Motor
from time import sleep
from config import DRIVE_SPEED

rear_motor = Motor('A')

def drive_forward(speed=DRIVE_SPEED, duration=None):
    rear_motor.start(speed)
    if duration:
        sleep(duration)
        stop_all()

def drive_backward(speed=DRIVE_SPEED, duration=None):
    rear_motor.start(-speed)
    if duration:
        sleep(duration)
        stop_all()

def stop_all():
    rear_motor.stop()
