# turns.py
# Скрипты поворота влево и вправо

from drive.motors import steer_left, steer_right, steer_straight, drive_forward, stop_all
from time import sleep

def turn_left():
    print("Выполняется поворот налево")
    steer_left()
    drive_forward(speed=50, duration=1.0)  # Время подбирается экспериментально
    stop_all()
    steer_straight()


def turn_right():
    print("Выполняется поворот направо")
    steer_right()
    drive_forward(speed=50, duration=1.0)
    stop_all()
    steer_straight()
