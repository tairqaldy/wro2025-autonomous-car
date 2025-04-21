# obstacle_detection.py
# Обнаружение столбиков по цвету и форме (зелёные и красные)

import cv2
import numpy as np
from vision.camera_usb import capture_frame

def analyze_obstacle():
    """
    Анализирует кадр с камеры и возвращает направление объезда:
    - "left"  → зелёный объект справа (объезд слева)
    - "right" → красный объект слева (объезд справа)
    - None    → ничего не обнаружено
    """
    frame = capture_frame()
    if frame is None:
        print("⚠️ Кадр не получен")
        return None

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Расширенные маски под освещение
    red_mask1 = cv2.inRange(hsv, np.array([0, 100, 100]), np.array([10, 255, 255]))
    red_mask2 = cv2.inRange(hsv, np.array([160, 100, 100]), np.array([180, 255, 255]))
    red_mask = cv2.bitwise_or(red_mask1, red_mask2)

    green_mask = cv2.inRange(hsv, np.array([50, 100, 100]), np.array([85, 255, 255]))

    # Уменьшаем шум
    red_mask = cv2.medianBlur(red_mask, 5)
    green_mask = cv2.medianBlur(green_mask, 5)

    # Анализ красного — препятствие слева → объехать справа
    if detect_pillar_in_mask(red_mask, color_name="red") == "left":
        return "right"

    # Анализ зелёного — препятствие справа → объехать слева
    if detect_pillar_in_mask(green_mask, color_name="green") == "right":
        return "left"

    return None

def detect_pillar_in_mask(mask, color_name="color"):
    """
    Ищет столбики подходящей формы и размера, возвращает bounding boxes.
    Возвращает: список кортежей (x, y, w, h, side, color_name)
    """
    bounding_boxes = []
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        area = cv2.contourArea(cnt)
        aspect_ratio = h / w if w != 0 else 0

        if area > 1000 and 1.5 < aspect_ratio < 4.5:
            side = "left" if x + w < mask.shape[1] // 2 else "right"
            bounding_boxes.append((x, y, w, h, side, color_name))
            print(f"🎯 Найден {color_name.upper()} столбик | side={side}, area={int(area)}, ratio={round(aspect_ratio, 2)}")

    return bounding_boxes
