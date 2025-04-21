# ultrasonic_left.py
# Левый ультразвуковой сенсор

from buildhat import DistanceSensor
import time

# Подключённый порт: D (уточни при необходимости)
ultrasonic_left = DistanceSensor('C')

def get_distance_left(samples=3):
    """
    Возвращает усреднённое расстояние от левого сенсора в мм
    """
    readings = []
    for _ in range(samples):
        dist = ultrasonic_left.get_distance()
        if dist != -1:
            readings.append(dist)
        time.sleep(0.05)

    return sum(readings) / len(readings) if readings else -1
