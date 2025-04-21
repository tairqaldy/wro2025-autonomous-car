# ultrasonic_right.py – Interface for the right ultrasonic sensor on port D.
from buildhat import DistanceSensor
import time

# Initialize right ultrasonic sensor (port D on Build HAT)
ultrasonic_right = DistanceSensor('D')

def get_distance_right(samples=3):
    """
    Return the average distance in mm from the right sensor.
    Returns -1 if no reading.
    """
    readings = []
    for _ in range(samples):
        dist = ultrasonic_right.get_distance()
        if dist != -1:
            readings.append(dist)
        time.sleep(0.05)
    return sum(readings) / len(readings) if readings else -1
