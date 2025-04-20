# speed_run.py

from drive.motors import drive_forward, stop_all, steering_motor
from sensors.color_line import check_turn_color
from sensors.ultrasonic import ultrasonic_sensor
from config import DEFAULT_SPEED, TURN_ANGLE
from time import sleep

# Центрирование по стене на 300 мм
TARGET_DISTANCE_MM = 300
TOLERANCE_MM = 20

TOTAL_TURNS = 12
turn_counter = 0
first_turn_completed = False

def fast_speed_run():
    global turn_counter, first_turn_completed
    print("🚦 Начинаем движение...")

    while turn_counter < TOTAL_TURNS:

        # 🚩 До первого поворота — просто едем вперёд, пока не увидим cyan/red
        if not first_turn_completed:
            turn_direction = check_turn_color()
            if turn_direction == "left":
                print("🔵 Первый поворот влево (Cyan)")
                steering_motor.run_for_degrees(-TURN_ANGLE, 40)
                drive_forward(speed=DEFAULT_SPEED, duration=0.8)
                stop_all()
                steering_motor.run_to_position(0)
                first_turn_completed = True
                turn_counter += 1
                continue
            elif turn_direction == "right":
                print("🔴 Первый поворот вправо (Red)")
                steering_motor.run_for_degrees(TURN_ANGLE, 40)
                drive_forward(speed=DEFAULT_SPEED, duration=0.8)
                stop_all()
                steering_motor.run_to_position(0)
                first_turn_completed = True
                turn_counter += 1
                continue
            else:
                drive_forward(speed=DEFAULT_SPEED)
                sleep(0.1)
                continue

        # 📍 После первого поворота — начинаем искать повороты и центрироваться
        color_result = check_turn_color()
        if color_result == "left":
            print("🔵 Поворот влево (Cyan)")
            steering_motor.run_for_degrees(-TURN_ANGLE, 40)
            drive_forward(speed=DEFAULT_SPEED, duration=0.8)
            stop_all()
            steering_motor.run_to_position(0)
            turn_counter += 1
            continue
        elif color_result == "right":
            print("🔴 Поворот вправо (Red)")
            steering_motor.run_for_degrees(TURN_ANGLE, 40)
            drive_forward(speed=DEFAULT_SPEED, duration=0.8)
            stop_all()
            steering_motor.run_to_position(0)
            turn_counter += 1
            continue

        # 🧭 Центрирование по правой стенке на 300 мм
        distance = ultrasonic_sensor.get_distance()
        if distance == -1:
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

        sleep(0.2)

    print("✅ Трасса завершена")
    stop_all()
    input("🔚 Нажмите Enter для остановки\n")
    stop_all()

if __name__ == "__main__":
    fast_speed_run()
