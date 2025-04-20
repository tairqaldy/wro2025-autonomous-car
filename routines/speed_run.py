# speed_run.py
# Базовый автономный тест: едем, держим дистанцию, реагируем на поворот

from drive.motors import drive_forward, stop_all
from sensors.color_line import check_turn_color
from sensors.ultrasonic import center_with_wall
from drive.turns import turn_left, turn_right
from time import sleep

TOTAL_TURNS = 12
turn_counter = 0
first_turn_completed = False


def fast_speed_run():
    global turn_counter
    print("🚦 Начинаем тест движения, удержания и поворотов")

    if not first_turn_completed:
    turn_direction = check_turn_color()
    if turn_direction == "left":
        turn_left()
        first_turn_completed = True
        continue
    elif turn_direction == "right":
        turn_right()
        first_turn_completed = True
        continue
    else:
        # До первого поворота просто едем прямо без коррекции
        drive_forward(speed=DEFAULT_SPEED)
        sleep(0.05)
        continue


    if first_turn_completed:
    distance = ultrasonic_sensor.get_distance()
    if distance == -1:
        drive_forward(speed=DEFAULT_SPEED)
    elif distance > TARGET_DISTANCE_MM + TOLERANCE_MM:
        # слегка влево
        steering_motor.run_for_degrees(-5, 40)
    elif distance < TARGET_DISTANCE_MM - TOLERANCE_MM:
        # слегка вправо
        steering_motor.run_for_degrees(5, 40)
    else:
        steering_motor.run_to_position(0)
    drive_forward(speed=DEFAULT_SPEED)
    sleep(0.05)



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
        drive_forward(DEFAULT_SPEED)
        sleep(0.05)

    print("✅ Завершено: 12 поворотов достигнуто")
    stop_all()

    input("🔚 Нажмите Enter для остановки робота\n")
    stop_all()

if __name__ == "__main__":
    fast_speed_run()