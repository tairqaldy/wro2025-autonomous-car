# speed_run.py
# Wall following and color detection routine with lap counting

from drive.motors import drive_forward, stop_all, steering_motor
from sensors.ultrasonic import ultrasonic_sensor
from sensors.color_line import check_turn_color
from config import (
    WALL_FOLLOW_SPEED, WALL_SEARCH_SPEED, MIN_SPEED,
    COLOR_DETECTION_SPEED, TURN_SPEED,
    STRAIGHT_ANGLE, WALL_CORRECTION_ANGLE, SNAKE_TURN_ANGLE,
    TURN_ANGLE, BLUE, ORANGE,
    TARGET_DISTANCE_MM, TOLERANCE_MM,
    MIN_WALL_DISTANCE, MAX_WALL_DISTANCE,
    CORRECTION_THRESHOLD, WALL_SEARCH_TIMEOUT,
    WALL_CORRECTION_DELAY, WALL_READ_DELAY,
    SNAKE_TURN_DELAY, SNAKE_FORWARD_DELAY,
    COLOR_READ_DELAY, TURN_DURATION,
    COLOR_DETECTION_DURATION, LINES_PER_LAP, TOTAL_LAPS
)
import time

line_counter = 0
lap_counter = 0
last_color = None
error_count = 0
MAX_ERRORS = 3

# speed_run.py
# Simplified version: just drive forward and count laps

from drive.motors import drive_forward, stop_all, steering_motor
from config import DEFAULT_SPEED, TURNS_PER_LAP, TOTAL_LAPS, WALL_CORRECTION_DELAY
import time

lap_counter = 0
turn_counter = 0


def drive_simple_laps():
    global lap_counter, turn_counter

    print("🚦 Начинаем упрощённый скоростной заезд (только движение по кругам)...")

    try:
        while lap_counter < TOTAL_LAPS:
            # Просто едем прямо и симулируем повороты через интервалы
            drive_forward(speed=DEFAULT_SPEED)
            time.sleep(2)  # Длительность между поворотами/секторами трассы (подбери вручную)

            turn_counter += 1
            print(f"🔁 Поворот #{turn_counter}")

            if turn_counter >= TURNS_PER_LAP:
                lap_counter += 1
                turn_counter = 0
                print(f"🏁 Круг {lap_counter} завершён")

        print("✅ Все круги завершены!")

    except KeyboardInterrupt:
        print("🛑 Остановлено пользователем")
    finally:
        stop_all()
        steering_motor.run_to_position(0)
        print("🏁 Остановлено")


if __name__ == "__main__":
    drive_simple_laps()