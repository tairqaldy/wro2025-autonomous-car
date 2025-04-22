# vision/camera_stream.py
import cv2

STREAM_URL = "http://limelight.local:5800/stream.mjpg"
cap = None

def init_camera():
    global cap
    cap = cv2.VideoCapture(STREAM_URL)
    if not cap.isOpened():
        print("❌ Ошибка: не удалось подключиться к потоку камеры")
        return False
    print("✅ Камера Limelight подключена через HTTP")
    return True

def get_frame():
    if cap is None:
        return None
    ret, frame = cap.read()
    if not ret:
        print("⚠️ Не удалось получить кадр")
        return None
    return frame

def release_camera():
    global cap
    if cap is not None:
        cap.release()
        cap = None
