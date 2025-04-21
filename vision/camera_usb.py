# camera_usb.py
# Инициализация и захват кадров с USB-камеры

import cv2
from config import CAMERA_INDEX, FRAME_WIDTH, FRAME_HEIGHT

# Инициализация камеры
camera = None

def init_camera():
    global camera
    camera = cv2.VideoCapture(CAMERA_INDEX)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    if not camera.isOpened():
        print("❌ Ошибка: камера не инициализирована")
        return False

    print("✅ Камера подключена")
    return True

def capture_frame():
    """Считывает один кадр с камеры"""
    if not camera:
        print("⚠️ Камера не инициализирована")
        return None

    ret, frame = camera.read()
    if not ret:
        print("⚠️ Не удалось считать кадр")
        return None

    return frame

def show_live_feed():
    """Показывает видеопоток с камеры в реальном времени. Завершение — клавиша 'q'"""
    if not init_camera():
        return

    print("🎥 Включён режим реального времени. Нажмите 'q' для выхода")
    while True:
        frame = capture_frame()
        if frame is None:
            break

        cv2.imshow("Live USB Camera", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()
