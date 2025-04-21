# test_obstacle_camera.py
# Тест реального времени: обнаружение и отображение столбиков

import cv2
import numpy as np
from vision.camera_usb import init_camera, capture_frame, camera
from vision.obstacle_detection import detect_pillar_in_mask

def run_obstacle_camera_test():
    print("🎥 Обнаружение препятствий в реальном времени")
    
    if not init_camera():
        print("❌ Камера не подключена")
        return

    print("🔍 Нажмите 'q' для выхода")

    while True:
        frame = capture_frame()
        if frame is None:
            continue

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Маски для красного и зелёного
        red_mask1 = cv2.inRange(hsv, np.array([0, 100, 100]), np.array([10, 255, 255]))
        red_mask2 = cv2.inRange(hsv, np.array([160, 100, 100]), np.array([180, 255, 255]))
        red_mask = cv2.bitwise_or(red_mask1, red_mask2)
        red_mask = cv2.medianBlur(red_mask, 5)

        green_mask = cv2.inRange(hsv, np.array([50, 100, 100]), np.array([85, 255, 255]))
        green_mask = cv2.medianBlur(green_mask, 5)

        # Обнаружение и отрисовка
        red_boxes = detect_pillar_in_mask(red_mask, "red")
        green_boxes = detect_pillar_in_mask(green_mask, "green")

        for (x, y, w, h, side, color_name) in red_boxes + green_boxes:
            color = (0, 0, 255) if color_name == "red" else (0, 255, 0)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            label = f"{color_name} ({side})"
            cv2.putText(frame, label, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

        # Показываем изображение
        cv2.imshow("🧪 Pillar Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("🛑 Завершение показа")
            break

    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_obstacle_camera_test()
