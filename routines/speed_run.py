# speed_run.py
# Скоростной заезд с ориентиром по стенам (центрирование по бокам)

from drive.motors import drive_forward, stop_all
from drive.steering import steer_left, steer_right, steer_straight
from sensors.ultrasonic_left import get_distance_left
from sensors.ultrasonic_right import get_distance_right
from config import DRIVE_SPEED
import time

def speed_run_loop():
    print("🚀 Старт скоростного заезда")

    try:
        while True:
            left = get_distance_left()
            right = get_distance_right()

            print(f"📡 Лево: {left:.0f} мм | Право: {right:.0f} мм")

            if left == -1 and right != -1:
                print("❌ Левая стена потеряна → поворот влево")
                steer_left()
            elif right == -1 and left != -1:
                print("❌ Правая стена потеряна → поворот вправо")
                steer_right()
            else:
                print("✅ Обе стены видим → едем прямо")
                steer_straight()

            drive_forward(speed=DRIVE_SPEED)
            time.sleep(0.08)

    except KeyboardInterrupt:
        print("🛑 Прервано пользователем")
        stop_all()
        steer_straight()
