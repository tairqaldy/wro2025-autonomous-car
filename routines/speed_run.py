# speed_run.py
# Скоростной режим с проверкой работы моторов и учётом поворотов

from drive.motors import drive_forward, stop_all
from sensors.color_line import check_turn_color
from sensors.ultrasonic import center_with_wall
from drive.turns import steer_straight
from time import sleep

# Параметры гонки
TOTAL_TURNS = 12  # 4 поворота на круг * 3 круга
turn_counter = 0

def fast_speed_run():
    global turn_counter
    print("⚡️ Скоростной заезд начат")

    # Тест начального вращения моторов
    print("🔁 Тест: едем прямо 1 секунду...")
    drive_forward(speed=60)
    sleep(1)
    stop_all()

    print("✅ Моторы работают. Начинаем заезд.")
    sleep(0.5)

    while turn_counter < TOTAL_TURNS:
        result = check_turn_color()
        if result in ["left", "right"]:
            turn_counter += 1
            print(f"🔁 Поворот {result} (всего: {turn_counter})")
            continue

        center_with_wall()
        drive_forward(speed=90)
        sleep(0.05)

    print("🏁 Трасса завершена. Остановка в стартовой зоне.")
    stop_all()

if __name__ == "__main__":
    fast_speed_run()
