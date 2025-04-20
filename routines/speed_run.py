# speed_run.py

from drive.motors import drive_forward, stop_all, steering_motor
from sensors.color_line import check_turn_color
from sensors.ultrasonic import ultrasonic_sensor
from drive.turns import turn_left, turn_right
from config import DEFAULT_SPEED, TARGET_DISTANCE_MM, TOLERANCE_MM, TURN_ANGLE
from time import sleep

TOTAL_TURNS = 12
turn_counter = 0
first_turn_completed = False

def fast_speed_run():
    global turn_counter, first_turn_completed
    print("🚦 Начинаем движение...")

    while turn_counter < TOTAL_TURNS:

        if not first_turn_completed:
            turn_direction = check_turn_color()
            if turn_direction == "left":
                print("Первый поворот влево")
                turn_left()
                first_turn_completed = True
                turn_counter += 1
                continue
            elif turn_direction == "right":
                print("Первый поворот вправо")
                turn_right()
                first_turn_completed = True
                turn_counter += 1
                continue
            else:
                drive_forward(speed=DEFAULT_SPEED)
                sleep(0.05)
                continue

        # После первого поворота — обработка стены и дальнейших поворотов
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

        # Центрирование по правой стене
        distance = ultrasonic_sensor.get_distance()
        if distance == -1:
            # Датчик не видит — едем прямо
            drive_forward(speed=DEFAULT_SPEED)
        elif distance > TARGET_DISTANCE_MM + TOLERANCE_MM:
            steering_motor.run_for_degrees(-5, 30)
            drive_forward(speed=DEFAULT_SPEED)
        elif distance < TARGET_DISTANCE_MM - TOLERANCE_MM:
            steering_motor.run_for_degrees(5, 30)
            drive_forward(speed=DEFAULT_SPEED)
        else:
            steering_motor.run_to_position(0)
            drive_forward(speed=DEFAULT_SPEED)

        sleep(0.05)

    print("✅ Трасса завершена")
    stop_all()
    input("🔚 Нажмите Enter для остановки\n")
    stop_all()

if __name__ == "__main__":
    fast_speed_run()
