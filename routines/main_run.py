# main_run.py
# Основной автономный заезд: объезд столбиков, повороты, парковка

from drive.motors import drive_forward, stop_all
from sensors.color_line import check_turn_color
from sensors.ultrasonic import center_with_wall
from vision.obstacle_detection import analyze_obstacle
from vision.parking_detection import detect_parking_zone
from drive.turns import steer_straight

import cv2

# Настройка камеры
camera = cv2.VideoCapture(0)

# Счётчики
turn_counter = 0
lap_counter = 0
TOTAL_LAPS = 3
TURNS_PER_LAP = 4

parking_done = False


def main_autonomous_run():
    global turn_counter, lap_counter, parking_done

    while lap_counter < TOTAL_LAPS:
        ret, frame = camera.read()
        if not ret:
            continue

        # 1. Проверка на парковку (только на последнем круге)
        if lap_counter == TOTAL_LAPS - 1 and not parking_done:
            if detect_parking_zone(frame):
                print("Финальная парковка — заезжаем")
                stop_all()
                # TODO: вызвать функцию для параллельной парковки
                parking_done = True
                break

        # 2. Распознавание столбиков камерой
        obstacle = analyze_obstacle(frame)
        if obstacle == "right":
            # TODO: объезд справа
            continue
        elif obstacle == "left":
            # TODO: объезд слева
            continue

        # 3. Проверка на поворот по цвету линии
        result = check_turn_color()
        if result in ["left", "right"]:
            turn_counter += 1
            print(f"Поворот {result} выполнен. Всего: {turn_counter}")

            if turn_counter >= TURNS_PER_LAP:
                lap_counter += 1
                turn_counter = 0
                print(f"Круг {lap_counter} завершён")
            continue

        # 4. Удержание вдоль стены
        center_with_wall()
        drive_forward(speed=60)

    print("Маршрут завершён")
    stop_all()
    camera.release()
