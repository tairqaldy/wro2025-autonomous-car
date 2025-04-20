# speed_run.py
# Базовый автономный тест: едем, держим дистанцию, реагируем на поворот

from drive.motors import drive_forward, stop_all
from sensors.color_line import check_turn_color
from sensors.ultrasonic import center_with_wall
from drive.turns import turn_left, turn_right
from time import sleep

TOTAL_TURNS = 12
turn_counter = 0

def fast_speed_run():
    global turn_counter
    print("🚦 Начинаем тест движения, удержания и поворотов")

    while turn_counter < TOTAL_TURNS:
        result = check_turn_color()
        if result == "left":
            print("↪️ Поворот влево")
            turn_left()
            turn_counter += 1
            continue
        elif result == "right":
            print("↩️ Поворот вправо")
            turn_right()
            turn_counter += 1
            continue

        # Центрирование по стене
        center_with_wall()
        drive_forward(speed=60)
        sleep(0.05)

    print("✅ Завершено: 12 поворотов достигнуто")
    stop_all()

    input("🔚 Нажмите Enter для остановки робота\n")
    stop_all()

if __name__ == "__main__":
    fast_speed_run()