# motors.py
# Управление движением: вперёд, назад, влево, вправо

from buildhat import Motor
from time import sleep

# Подключение моторов
rear_motor = Motor('A')      # Задний привод
steering_motor = Motor('C')  # Передняя рулевая ось

def drive_forward(speed=60, duration=None):
    rear_motor.start(speed)
    if duration:
        sleep(duration)
        rear_motor.stop()

def drive_backward(speed=60, duration=None):
    rear_motor.start(-speed)
    if duration:
        sleep(duration)
        rear_motor.stop()

def stop_all():
    rear_motor.stop()
    steering_motor.stop()

def steer_left(angle=25):
    steering_motor.run_to_position(-angle)

def steer_right(angle=25):
    steering_motor.run_to_position(angle)

def steer_straight():
    steering_motor.run_to_position(0)