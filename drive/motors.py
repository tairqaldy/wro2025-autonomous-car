# motors.py
# Управление движением робота: вперёд/назад и остановка

from buildhat import Motor
from time import sleep
from config import DRIVE_SPEED

# Один большой мотор для заднего привода (мост напрямую соединяет оба задних колеса)
rear_motor = Motor('A')  # Порт A


def drive_forward(speed=DRIVE_SPEED, duration=None):
    """
    Движение вперёд на заданной скорости. Если указана длительность, останавливается через неё.
    """
    rear_motor.start(speed)
    if duration:
        sleep(duration)
        stop_all()


def drive_backward(speed=DRIVE_SPEED, duration=None):
    """
    Движение назад на заданной скорости. Если указана длительность, останавливается через неё.
    """
    rear_motor.start(-speed)
    if duration:
        sleep(duration)
        stop_all()


def stop_all():
    """
    Остановка заднего привода.
    """
    rear_motor.stop()
