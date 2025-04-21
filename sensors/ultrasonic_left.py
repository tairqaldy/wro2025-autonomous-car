# ultrasonic_left.py – Interface for the left ultrasonic sensor (e.g., EV3 Ultrasonic) on port C.
from buildhat import DistanceSensor
import time

# Initialize left ultrasonic sensor (port C on Build HAT)
ultrasonic_left = DistanceSensor('C')

def get_distance_left(samples=3):
    """
    Return the average distance in mm from the left sensor.
    Returns -1 if no reading (wall out of range).
    """
    readings = []
    for _ in range(samples):
        dist = ultrasonic_left.get_distance()  # get_distance returns distance in mm or -1 if nothing detected
        if dist != -1:
            readings.append(dist)
        time.sleep(0.05)
    return sum(readings) / len(readings) if readings else -1
