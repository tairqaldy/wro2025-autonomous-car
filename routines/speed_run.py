# routines/speed_run.py
from drive.motors import drive_forward, stop_all
from drive.steering import steer_left, steer_right
from sensors.ultrasonic_left import get_distance_left
from sensors.ultrasonic_right import get_distance_right
import time

def speed_run():
    print("🏁 Запуск скоростного круга...")
    while True:
        drive_forward(duration=1.2)  # Едем прямо короткими рывками

        left = get_distance_left()
        right = get_distance_right()

        print(f"📏 Ультразвук — Л: {left} мм, П: {right} мм")

        if left == -1:
            print("🧱 Левая стена потеряна — поворачиваем влево")
            steer_left()

        elif right == -1:
            print("🧱 Правая стена потеряна — поворачиваем вправо")
            steer_right()

        time.sleep(0.2)  # Небольшая пауза между циклами
