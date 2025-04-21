# steering.py
# Управление рулевой системой: поворот влево, вправо и выравнивание

from buildhat import Motor
import time

# Настройки поворота
MAX_TURN_ANGLE = 15   # угол для поворота
STRAIGHT_ANGLE = 0    # прямое положение

# Рулевой мотор подключён к порту B
steering_motor = Motor('B')

def steer_left():
    """Повернуть влево и вернуть в центр"""
    print("↩️ Поворот влево")
    steering_motor.run_to_position(-MAX_TURN_ANGLE, speed=100)
    time.sleep(0.2)
    steer_straight()

def steer_right():
    """Повернуть вправо и вернуть в центр"""
    print("↪️ Поворот вправо")
    steering_motor.run_to_position(MAX_TURN_ANGLE, speed=100)
    time.sleep(0.2)
    steer_straight()

def steer_straight():
    """Выпрямить колёса"""
    print("⬆️ Ровное положение")
    steering_motor.run_to_position(STRAIGHT_ANGLE, speed=100)
    time.sleep(0.2)
    print(f"📍 Текущая позиция: {steering_motor.get_position()}°")
