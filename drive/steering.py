# steering.py
# Управление рулевой системой: поворот влево, вправо и выравнивание

from buildhat import Motor
from config import MAX_TURN_ANGLE, STRAIGHT_ANGLE
import time

# Передний мотор, управляющий рулём
steering_motor = Motor('B')  # Проверь порт


def steer_left():
    """Повернуть колёса влево."""
    print("↩️ Поворот влево")
    steering_motor.run_to_position(-MAX_TURN_ANGLE)
    time.sleep(1)


def steer_right():
    """Повернуть колёса вправо."""
    print("↪️ Поворот вправо")
    steering_motor.run_to_position(MAX_TURN_ANGLE)
    time.sleep(1)


def steer_straight():
    """Выпрямить колёса."""
    print("⬆️ Ровное положение")
    steering_motor.run_to_position(STRAIGHT_ANGLE)
    time.sleep(0.2)
