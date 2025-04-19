# obstacle_detection.py
# Обнаружение столбиков и выбор стороны объезда

import cv2
import numpy as np

# Цветовые границы в HSV
RED_LOWER = np.array([0, 120, 70])
RED_UPPER = np.array([10, 255, 255])
GREEN_LOWER = np.array([40, 40, 40])
GREEN_UPPER = np.array([80, 255, 255])

# Минимальная площадь объекта, чтобы не считывать шум
MIN_AREA = 500

# Определяет направление в зависимости от цвета объекта
def analyze_obstacle(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    red_mask = cv2.inRange(hsv, RED_LOWER, RED_UPPER)
    green_mask = cv2.inRange(hsv, GREEN_LOWER, GREEN_UPPER)

    red_contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    green_contours, _ = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in red_contours:
        area = cv2.contourArea(cnt)
        if area > MIN_AREA:
            print("Обнаружен КРАСНЫЙ столбик → объезд СПРАВА")
            return "right"

    for cnt in green_contours:
        area = cv2.contourArea(cnt)
        if area > MIN_AREA:
            print("Обнаружен ЗЕЛЁНЫЙ столбик → объезд СЛЕВА")
            return "left"

    return "none"
