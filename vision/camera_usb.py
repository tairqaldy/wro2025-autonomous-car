# camera_usb.py (обновленные функции)

import cv2
from config import CAMERA_INDEX, FRAME_WIDTH, FRAME_HEIGHT

camera = None

def init_camera():
    """Инициализирует камеру; возвращает True при успехе или False при ошибке."""
    global camera
    # Если камера уже была открыта ранее, освободим её перед повторной инициализацией
    if camera:
        camera.release()
        cv2.destroyAllWindows()
    try:
        camera = cv2.VideoCapture(CAMERA_INDEX)
    except Exception as e:
        print(f"❌ Ошибка: не удалось открыть камеру ({CAMERA_INDEX}): {e}")
        camera = None
        return False
    # Установка разрешения кадра
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    if not camera.isOpened():
        print(f"❌ Ошибка: камера не инициализирована ({CAMERA_INDEX})")
        return False
    print(f"✅ Камера инициализирована: {CAMERA_INDEX}")
    return True

def capture_frame():
    """Считывает единичный кадр с камеры; возвращает изображение или None при ошибке."""
    if not camera:
        print("⚠️ Камера не инициализирована")
        return None
    try:
        ret, frame = camera.read()
    except Exception as e:
        print(f"⚠️ Ошибка чтения с камеры: {e}")
        return None
    if not ret or frame is None:
        print("⚠️ Не удалось считать кадр")
        return None
    return frame

# ... release_camera() без изменений ...
