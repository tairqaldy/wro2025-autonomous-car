# ultrasonic.py
# Центрирование робота вдоль правой стены

from buildhat import DistanceSensor
from drive.motors import steer_left, steer_right, steer_straight

ultrasonic_sensor = DistanceSensor('B')  # Порт, где подключён датчик справа

TARGET_DISTANCE = 300  # Целевая дистанция в мм
TOLERANCE = 15        # Допустимое отклонение


def center_with_wall():
    distance = ultrasonic_sensor.get_distance()
    print(f"Расстояние справа: {distance} мм")

    if distance == -1:
        return None  # или вернуть -1 и обработать в вызывающем коде
    elif distance < TARGET_DISTANCE - TOLERANCE:
        steer_left(10)  # отодвигаемся от стены
    elif distance > TARGET_DISTANCE + TOLERANCE:
        steer_right(10)  # приближаемся к стене
    else:
        steer_straight()  # всё ок
