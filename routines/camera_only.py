# routines/camera_only.py
from vision.camera_usb import init_camera, capture_frame
import cv2

def run_camera_test():
    print("📷 Камера: тест видеопотока")
    if not init_camera():
        print("❌ Камера не подключена")
        return

    while True:
        frame = capture_frame()
        if frame is None:
            break

        cv2.imshow("Camera Test", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
