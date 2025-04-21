# camera_usb.py

import cv2
from config import CAMERA_INDEX, FRAME_WIDTH, FRAME_HEIGHT

camera = None

def init_camera():
    global camera

    # Очистка предыдущей
    if camera:
        camera.release()
        cv2.destroyAllWindows()

    # Поддержка строкового пути (например, /dev/video10)
    camera = cv2.VideoCapture(CAMERA_INDEX)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    if not camera.isOpened():
        print(f"❌ Ошибка: камера не инициализирована ({CAMERA_INDEX})")
        return False

    print(f"✅ Камера инициализирована: {CAMERA_INDEX}")
    return True

def capture_frame():
    if not camera:
        print("⚠️ Камера не инициализирована")
        return None

    ret, frame = camera.read()
    if not ret:
        print("⚠️ Не удалось считать кадр")
        return None

    return frame

def show_live_feed():
    if not init_camera():
        return

    print("🎥 Видеопоток активен. Нажмите 'q' для выхода")
    while True:
        frame = capture_frame()
        if frame is None:
            break

        cv2.imshow("USB Camera", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()
