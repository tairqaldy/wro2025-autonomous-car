# turns.py
# Скрипты поворота влево и вправо с возвратом рулевой оси

from drive.motors import steering_motor, drive_forward, stop_all
from time import sleep
from config import TURN_ANGLE, DEFAULT_SPEED

# Поворот влево с возвратом оси

def turn_left():
    print("↪️ Поворот влево (с возвратом)")
    steering_motor.run_for_degrees(-TURN_ANGLE, 40)
    drive_forward(speed=DEFAULT_SPEED, duration=1.0)
    stop_all()
    steering_motor.run_for_degrees(TURN_ANGLE, 40)


# Поворот вправо с возвратом оси

def turn_right():
    print("↩️ Поворот вправо (с возвратом)")
    steering_motor.run_for_degrees(TURN_ANGLE, 40)
    drive_forward(speed=DEFAULT_SPEED, duration=1.0)
    stop_all()
    steering_motor.run_for_degrees(-TURN_ANGLE, 40)