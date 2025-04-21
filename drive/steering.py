# steering.py
# Управление рулевой системой: поворот влево, вправо и выравнивание

from buildhat import Motor
from config import MAX_TURN_ANGLE, STRAIGHT_ANGLE
import time

# Передний мотор, управляющий рулём
steering_motor = Motor('B')  # Убедись, что подключён к порту B

def steer_left():
    """Повернуть колёса влево и зафиксировать."""
    print("↩️ Поворот влево")
    steering_motor.run_to_position(-MAX_TURN_ANGLE)
    time.sleep(0.05)
    steering_motor.hold()
    print(f"📍 Текущая позиция: {steering_motor.get_position()}°")

def steer_right():
    """Повернуть колёса вправо и зафиксировать."""
    print("↪️ Поворот вправо")
    steering_motor.run_to_position(MAX_TURN_ANGLE)
    time.sleep(0.05)
    steering_motor.hold()
    print(f"📍 Текущая позиция: {steering_motor.get_position()}°")

def steer_straight():
    """Выпрямить колёса и зафиксировать."""
    print("⬆️ Ровное положение")
    steering_motor.run_to_position(STRAIGHT_ANGLE)
    time.sleep(0.05)
    steering_motor.hold()
    print(f"📍 Текущая позиция: {steering_motor.get_position()}°")
