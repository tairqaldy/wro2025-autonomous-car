# steering.py
from buildhat import Motor
from config import MAX_TURN_ANGLE, STRAIGHT_ANGLE
import time

steering_motor = Motor('B')

def steer_left():
    print("↩️ Поворот влево")
    steering_motor.run_to_position(-MAX_TURN_ANGLE, speed=100)
    time.sleep(0.2)
    return_to_center()

def steer_right():
    print("↪️ Поворот вправо")
    steering_motor.run_to_position(MAX_TURN_ANGLE, speed=100)
    time.sleep(0.2)
    return_to_center()

def return_to_center():
    print("⬆️ Возврат в центр")
    steering_motor.run_to_position(STRAIGHT_ANGLE, speed=100)
    time.sleep(0.2)
    print(f"📍 Текущая позиция: {steering_motor.get_position()}°")
