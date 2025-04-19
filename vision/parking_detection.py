# parking_detection.py
# Обнаружение фиолетовой парковочной зоны

import cv2
import numpy as np

# HSV-границы для фиолетового цвета
PURPLE_LOWER = np.array([125, 50, 50])
PURPLE_UPPER = np.array([155, 255, 255])

MIN_AREA = 700  # минимальная площадь для фильтрации шума

def detect_parking_zone(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, PURPLE_LOWER, PURPLE_UPPER)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > MIN_AREA:
            print("Обнаружена фиолетовая зона (парковка)")
            return True

    return False
