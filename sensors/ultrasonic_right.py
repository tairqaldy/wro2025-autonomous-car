# ultrasonic_right.py
# Правый ультразвуковой сенсор

from buildhat import DistanceSensor
import time

# Подключённый порт: B (уточни при необходимости)
ultrasonic_right = DistanceSensor('D')

def get_distance_right(samples=3):
    """
    Возвращает усреднённое расстояние от правого сенсора в мм
    """
    readings = []
    for _ in range(samples):
        dist = ultrasonic_right.get_distance()
        if dist != -1:
            readings.append(dist)
        time.sleep(0.05)

    return sum(readings) / len(readings) if readings else -1
