# speed_run.py
# Скоростной режим с учётом поворотов и завершением в стартовой зоне

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
    print("Скоростной заезд начат")

    while turn_counter < TOTAL_TURNS:
        # Считывание цвета линии для поворота
        result = check_turn_color()
        if result in ["left", "right"]:
            turn_counter += 1
            print(f"Поворот {result}. Всего поворотов: {turn_counter}")
            continue

        # Движение и коррекция по стенке (по-прежнему используем для стабильности)
        center_with_wall()
        drive_forward(speed=90)
        sleep(0.1)  # чтобы не перегрузить цикл

    print("Трасса завершена. Остановка в стартовой зоне")
    stop_all()

if __name__ == "__main__":
    fast_speed_run()
