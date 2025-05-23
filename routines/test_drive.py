# test_drive.py
# Проверка всех основных компонентов: мотор, рулевое, сенсоры, камера, столбики, парковка

from drive.motors import drive_forward, drive_backward, stop_all
from drive.steering import steer_left, steer_right, steer_straight
from sensors.ultrasonic_left import get_distance_left
from sensors.ultrasonic_right import get_distance_right
from vision.camera_usb import init_camera, capture_frame
from vision.obstacle_detection import analyze_obstacle
from vision.parking_detection import detect_parking_zone
import time

def test_motors():
    print("\n🧪 Тест: движение вперёд")
    drive_forward(speed=100, duration=2.0)
    stop_all()
    time.sleep(1)

    print("🧪 Тест: движение назад")
    drive_backward(speed=100, duration=2)
    stop_all()
    time.sleep(1)

def test_steering():
    print("\n🧪 Тест: поворот налево")
    steer_left()
    time.sleep(1)

    print("🧪 Тест: поворот направо")
    steer_right()
    time.sleep(1)

def test_ultrasonic():
    print("\n🧪 Тест: ультразвуковые сенсоры")
    left = get_distance_left()
    right = get_distance_right()
    print(f"🔵 Расстояние слева: {left:.2f} мм")
    print(f"🟠 Расстояние справа: {right:.2f} мм")

def test_camera():
    print("\n🧪 Тест: камера USB")
    if init_camera():
        frame = capture_frame()
        if frame is not None:
            print("✅ Кадр успешно получен")
        else:
            print("⚠️ Кадр не получен")
    else:
        print("❌ Камера не найдена")
    release_camera()

def test_obstacle_detection():
    print("\n🧪 Тест: анализ препятствий по камере")
    if not init_camera():
        print("❌ Камера не подключена")
        return

    direction = analyze_obstacle()
    if direction == "left":
        print("🟢 Объезд слева")
    elif direction == "right":
        print("🟢 Объезд справа")
    else:
        print("✅ Препятствий не обнаружено")

    release_camera()

def test_parking_zone():
    print("\n🧪 Тест: поиск парковочной зоны")
    if not init_camera():
        print("❌ Камера не подключена")
        return

    found = detect_parking_zone()
    if found:
        print("🅿️ Парковочная зона найдена")
    else:
        print("❌ Парковка не обнаружена")

    release_camera()

def run_all_tests():
    print("🚦 Запуск всех тестов:")
    test_motors()
    test_steering()
    test_ultrasonic()
    test_camera()
    test_obstacle_detection()
    test_parking_zone()
    print("\n✅ Все тесты завершены")

if __name__ == "__main__":
    run_all_tests()