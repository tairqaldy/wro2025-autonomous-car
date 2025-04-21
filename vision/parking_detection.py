# parking_detection.py
# Заготовка: определение парковочной зоны по цвету (например, фиолетовый)

import cv2
import numpy as np
from vision.camera_usb import capture_frame

def detect_parking_zone():
    """
    Заглушка: проверяет наличие фиолетовой зоны на изображении.
    Возвращает True, если обнаружена, иначе False
    """
    frame = capture_frame()
    if frame is None:
        return False

    # Преобразуем кадр в HSV для поиска цвета
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Диапазон HSV для фиолетового (подбирается по реальному примеру)
    lower_purple = np.array([130, 50, 50])
    upper_purple = np.array([160, 255, 255])

    mask = cv2.inRange(hsv, lower_purple, upper_purple)
    purple_area = cv2.countNonZero(mask)

    if purple_area > 4000:
        print("🟣 Обнаружена парковочная зона!")
        return True

    return False
