# steering.py
# Управление рулевой системой: поворот влево, вправо и выравнивание

from buildhat import Motor
from config import MAX_TURN_ANGLE, STRAIGHT_ANGLE
import time

# Передний мотор, управляющий рулём
steering_motor = Motor('B')  # Проверь порт


def steer_left():
    print("↩️ Поворот влево")
    steering_motor.run_to_position(-MAX_TURN_ANGLE)
    print(f"📍 Текущая позиция: {steering_motor.get_position()}°")
    time.sleep(0.05)

def steer_right():
    print("↪️ Поворот вправо")
    steering_motor.run_to_position(MAX_TURN_ANGLE)
    print(f"📍 Текущая позиция: {steering_motor.get_position()}°")
    time.sleep(0.05)

def steer_straight():
    print("⬆️ Ровное положение")
    steering_motor.run_to_position(STRAIGHT_ANGLE)
    print(f"📍 Текущая позиция: {steering_motor.get_position()}°")
    time.sleep(0.05)
