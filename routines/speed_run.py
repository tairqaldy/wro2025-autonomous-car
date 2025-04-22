# routines/speed_run.py

import time
from drive.motors import drive_forward, stop_all
from drive.steering import steer_left, steer_right, steer_straight
from sensors.ultrasonic_left import get_distance_left
from sensors.ultrasonic_right import get_distance_right

def run_speed_mode():
    print("🚗 Запуск автономного режима (speed_run) на основе ультразвука")
    
    try:
        while True:
            left_distance = get_distance_left()
            right_distance = get_distance_right()

            print(f"🔵 Расстояние слева: {left:.2f} мм")
            print(f"🟠 Расстояние справа: {right:.2f} мм")

            if left_distance == -1:
                print("🔵 Стена слева не найдена – поворот влево")
                steer_left()
            elif right_distance == -1:
                print("🟠 Стена справа не найдена – поворот вправо")
                steer_right()
            else:
                print("🟩 Стены обнаружены – движение прямо")
                steer_straight()

            drive_forward(speed=80)  # скорость в процентах
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("⛔ Прерывание – остановка машины")
        stop_all()
        steer_straight()
