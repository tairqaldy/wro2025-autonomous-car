#!/usr/bin/env python3
# main_run.py — Универсальный сценарий: тестирование, скоростной и основной режимы

import sys, time, logging, argparse
from config import DEFAULT_SPEED, PARKING_SPEED, TARGET_DISTANCE_MM, TURNS_PER_LAP, TOTAL_LAPS, DEBUG_MODE
from drive.motors import drive_forward, drive_backward, stop_all, steering_motor
from drive.steering import steer_left, steer_right, steer_straight
from drive.turns import turn_left, turn_right
from sensors.ultrasonic_left import get_distance_left
from sensors.ultrasonic_right import get_distance_right
from sensors.color_line import check_turn_color
from vision.camera_usb import init_camera, capture_frame, release_camera
from vision.obstacle_detection import analyze_obstacle
from vision.parking_detection import detect_parking_zone

# Настройка логирования (консоль + файл), уровень в зависимости от DEBUG_MODE
log_level = logging.DEBUG if DEBUG_MODE else logging.INFO
logging.basicConfig(
    level=log_level,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
    handlers=[logging.StreamHandler(sys.stdout),
              logging.FileHandler("run.log", mode="w", encoding="utf-8")]
)

def run_test_mode():
    """Запуск тестирования всех компонентов."""
    logging.info("🚦 Запуск всех тестов (режим 'test')")
    # 1. Тест моторов движения вперед/назад
    logging.info("🧪 Тест: движение вперёд")
    drive_forward(speed=100, duration=2.0)
    stop_all()
    time.sleep(1)
    logging.info("🧪 Тест: движение назад")
    drive_backward(speed=100, duration=2.0)
    stop_all()
    time.sleep(1)
    # 2. Тест рулевого управления
    logging.info("🧪 Тест: поворот налево (руль)")
    steer_left(); time.sleep(1)
    logging.info("🧪 Тест: поворот направо (руль)")
    steer_right(); time.sleep(1)
    steer_straight()  # вернём колёса прямо
    # 3. Тест ультразвуковых датчиков
    logging.info("🧪 Тест: ультразвуковые датчики")
    left_dist = get_distance_left()
    right_dist = get_distance_right()
    if left_dist >= 0:
        logging.info(f"🔵 Расстояние слева: {left_dist:.2f} мм")
    else:
        logging.warning("🔵 Расстояние слева: нет данных")
    if right_dist >= 0:
        logging.info(f"🟠 Расстояние справа: {right_dist:.2f} мм")
    else:
        logging.warning("🟠 Расстояние справа: нет данных")
    # 4. Тест камеры
    logging.info("🧪 Тест: камера Limelight 3A")
    if init_camera():
        frame = capture_frame()
        if frame is not None:
            logging.info("✅ Кадр с камеры успешно получен")
        else:
            logging.warning("⚠️ Не удалось получить кадр с камеры")
    else:
        logging.error("❌ Камера не найдена")
    release_camera()
    # 5. Тест обнаружения препятствия (столбиков) 
    logging.info("🧪 Тест: обнаружение препятствий (столбики)")
    if init_camera():
        direction = analyze_obstacle()
        if direction == "left":
            logging.info("🟢 Объезд слева (препятствие обнаружено)")
        elif direction == "right":
            logging.info("🟢 Объезд справа (препятствие обнаружено)")
        else:
            logging.info("✅ Препятствий не обнаружено")
    else:
        logging.error("❌ Камера не подключена, пропуск теста препятствий")
    release_camera()
    # 6. Тест обнаружения парковочной зоны
    logging.info("🧪 Тест: поиск парковочной зоны")
    if init_camera():
        found = detect_parking_zone()
        if found:
            logging.info("🅿️ Парковочная зона найдена")
        else:
            logging.info("❌ Парковочная зона не обнаружена")
    else:
        logging.error("❌ Камера не подключена, пропуск теста парковки")
    release_camera()
    logging.info("✅ Все тесты завершены")

def run_speed_mode():
    """Запуск скоростного режима движения по прямой с автоматическими поворотами."""
    logging.info("🏁 Запуск скоростного режима (режим 'speed_run')")
    try:
        while True:
            # Едем прямо коротким отрезком
            drive_forward(speed=DEFAULT_SPEED, duration=1.2)
            stop_all()
            # Чтение расстояний слева и справа
            left = get_distance_left()
            right = get_distance_right()
            logging.info(f"📏 Ультразвук — Л: {left:.0f} мм, П: {right:.0f} мм")
            # Анализ потери стен
            if left == -1:   # левая стена пропала
                logging.info("🧱 Левая стена не видна — поворот влево")
                steer_left(); time.sleep(0.5)
                steer_straight()
            elif right == -1:  # правая стена пропала
                logging.info("🧱 Правая стена не видна — поворот вправо")
                steer_right(); time.sleep(0.5)
                steer_straight()
            # Небольшая пауза перед следующей итерацией
            time.sleep(0.2)
    except KeyboardInterrupt:
        logging.info("🛑 Скоростной заезд прерван пользователем")
    except Exception as e:
        logging.error(f"❌ Ошибка в скоростном режиме: {e}")

def run_main_mode():
    """Запуск основного автономного режима (объезд препятствий, круги, парковка)."""
    logging.info("🏎️ Запуск основного автономного заезда (режим 'main')")
    # Инициализация состояния
    turn_counter = 0
    lap_counter = 0
    steering_angle = 0  # текущий предполагаемый угол руля (0 = прямо)
    # Инициализация камеры для режима main (не критично, если не подключена)
    cam_available = init_camera()
    if not cam_available:
        logging.warning("⚠️ Камера Limelight не найдена — пропуск объезда препятствий и парковки")
    try:
        # Основной цикл движения по трассе (пока не пройдены все круги)
        while lap_counter < TOTAL_LAPS:
            # Проверяем, не настало ли время повернуть (датчик цвета или метки поворота)
            turn_signal = check_turn_color()
            if turn_signal in ["left", "right"]:
                # Выполняем поворот согласно сигналу
                if turn_signal == "left":
                    logging.info("🔄 Получен сигнал поворота налево")
                    turn_left()
                    logging.info(f"🔄 Поворот налево выполнен. Всего поворотов: {turn_counter+1}")
                    steering_angle = 0  # после маневра вернем руль прямо (предположительно)
                else:
                    logging.info("🔄 Получен сигнал поворота направо")
                    turn_right()
                    logging.info(f"🔄 Поворот направо выполнен. Всего поворотов: {turn_counter+1}")
                    steering_angle = 0
                turn_counter += 1
                # Проверяем, не завершен ли круг
                if turn_counter >= TURNS_PER_LAP:
                    lap_counter += 1
                    turn_counter = 0
                    logging.info(f"🏁 Круг {lap_counter} завершён")
                time.sleep(0.5)  # небольшая задержка после поворота (TURN_DELAY)
                continue  # перейти к следующей итерации цикла (продолжить движение)
            # Если поворот не требуется, едем прямо и корректируем положение по стене
            # Считываем расстояние до стены (левая сторона)
            dist = get_distance_left()  # используем левый дальномер для удержания дистанции
            if dist == -1:
                # Стена не видна - едем прямо
                drive_forward(speed=DEFAULT_SPEED)
                logging.debug("📏 Стена не обнаружена, держим курс прямо")
            elif dist > TARGET_DISTANCE_MM + 5:
                # Робот слишком далеко от левой стены — поворот влево
                steering_motor.run_for_degrees(-5, speed=30)
                steering_angle = max(steering_angle - 5, -25)  # обновляем угол, ограничивая -25°
                drive_forward(speed=DEFAULT_SPEED)
                logging.debug(f"📏 Дистанция слева {dist:.0f} мм > целевого ({TARGET_DISTANCE_MM}) — поворот влево на 5° (угол руля ~{steering_angle}°)")
            elif dist < TARGET_DISTANCE_MM - 5:
                # Робот слишком близко к стене — поворот вправо
                steering_motor.run_for_degrees(5, speed=30)
                steering_angle = min(steering_angle + 5, 25)   # обновляем угол, ограничивая 25°
                drive_forward(speed=DEFAULT_SPEED)
                logging.debug(f"📏 Дистанция слева {dist:.0f} мм < целевого ({TARGET_DISTANCE_MM}) — поворот вправо на 5° (угол руля ~{steering_angle}°)")
            else:
                # В пределах нормы — едем прямо, выравнивая руль
                steering_motor.run_to_position(0)
                steering_angle = 0
                drive_forward(speed=DEFAULT_SPEED)
                logging.debug(f"📏 Дистанция слева {dist:.0f} мм в норме — держим ровно (угол руля {steering_angle}°)")
            # Обнаружение препятствия (столбика) камерой, если доступна
            if cam_available:
                direction = analyze_obstacle()
                if direction:
                    if direction == "right":
                        logging.info("🔀 Обнаружен столбик, требуется объезд справа")
                        # Маневр: поворот вправо и объезд препятствия слева от робота
                        steer_right(); steering_angle = 25
                        drive_forward(speed=DEFAULT_SPEED, duration=1.0)
                        stop_all()
                        # Возврат к левой стене после обхода
                        steer_left(); steering_angle = -25
                        drive_forward(speed=DEFAULT_SPEED, duration=1.0)
                        stop_all()
                        steer_straight(); steering_angle = 0
                        logging.info("🔀 Объезд препятствия справа выполнен, продолжаем движение")
                    elif direction == "left":
                        logging.info("🔀 Обнаружен столбик, требуется объезд слева")
                        # Маневр: поворот влево и объезд препятствия справа от робота
                        steer_left(); steering_angle = -25
                        drive_forward(speed=DEFAULT_SPEED, duration=0.8)
                        stop_all()
                        steer_straight(); steering_angle = 0
                        logging.info("🔀 Объезд препятствия слева выполнен, продолжаем движение")
                    # Примечание: после объезда робот продолжит основной цикл, где ультразвук скорректирует его положение по стене
            time.sleep(0.1)  # задержка после коррекции (WALL_CORRECTION_DELAY)
        # Вышли из цикла после прохождения всех кругов
        logging.info(f"🏁 Все {lap_counter} круг(ов) пройдены, поиск зоны парковки...")
        # Финальная парковка по зоне (если камера доступна)
        if cam_available:
            parked = False
            # Плавное движение вперед, поиск метки парковки
            while not parked:
                found = detect_parking_zone()
                if found:
                    logging.info("🅿️ Обнаружена парковочная зона! Выполняем парковку.")
                    stop_all()
                    # Можно добавить небольшой проезд вперед для заезда в зону:
                    drive_forward(speed=PARKING_SPEED, duration=1.0)
                    stop_all()
                    parked = True
                    logging.info("✅ Парковка выполнена успешно")
                    break
                # Если пока не нашли, продвигаемся немного вперед и повторяем
                drive_forward(speed=PARKING_SPEED, duration=0.3)
                stop_all()
                time.sleep(0.5)  # пауза (PARKING_DELAY) перед следующим сканированием
            # Освобождаем камеру после парковки
            release_camera()
        else:
            logging.info("🎗 Пропуск поиска парковки (камера недоступна)")
        logging.info("🏁 Маршрут завершён")
    except KeyboardInterrupt:
        logging.warning("🛑 Автономный заезд прерван пользователем")
    except Exception as e:
        logging.error(f"❌ Ошибка в автономном режиме: {e}")
    finally:
        # Остановка моторов в конце или при прерывании
        stop_all()
        if cam_available:
            release_camera()

if __name__ == "__main__":
    # Парсим аргумент командной строки для выбора режима
    parser = argparse.ArgumentParser(description="Universal robot script (modes: test, speed_run, main)")
    parser.add_argument("mode", choices=["test", "speed_run", "main"], help="Режим работы: test / speed_run / main")
    args = parser.parse_args()
    try:
        if args.mode == "test":
            run_test_mode()
        elif args.mode == "speed_run":
            run_speed_mode()
        elif args.mode == "main":
            run_main_mode()
    except KeyboardInterrupt:
        logging.warning("🛑 Выполнение прервано пользователем")
    except Exception as e:
        logging.error(f"❌ Непредвиденная ошибка: {e}")
        sys.exit(1)
    finally:
        stop_all()
    