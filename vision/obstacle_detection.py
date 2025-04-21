# obstacle_detection.py
# Логика обнаружения столбиков (препятствий) с камеры с фильтрацией по форме и размеру

import cv2
import numpy as np
from vision.camera_usb import capture_frame

def analyze_obstacle():
    """
    Анализирует кадр с камеры и возвращает направление для объезда:
    - "left": если обнаружен зелёный столбик справа (объезд слева)
    - "right": если обнаружен красный столбик слева (объезд справа)
    - None: если ничего не обнаружено
    """
    frame = capture_frame()
    if frame is None:
        return None

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Пороговые значения цвета (настроить под освещение)
    red_lower = np.array([0, 100, 100])
    red_upper = np.array([10, 255, 255])
    green_lower = np.array([50, 100, 100])
    green_upper = np.array([80, 255, 255])

    red_mask = cv2.inRange(hsv, red_lower, red_upper)
    green_mask = cv2.inRange(hsv, green_lower, green_upper)

    # Обработка красных объектов
    red_direction = detect_direction_from_mask(red_mask, color_name="red")
    if red_direction:
        return "right"

    # Обработка зелёных объектов
    green_direction = detect_direction_from_mask(green_mask, color_name="green")
    if green_direction:
        return "left"

    return None

def detect_direction_from_mask(mask, color_name="color"):
    """
    Поиск контуров прямоугольных столбиков подходящей формы и размера
    """
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        area = cv2.contourArea(cnt)
        aspect_ratio = h / w if w != 0 else 0

        # Фильтрация по площади и соотношению сторон
        if area > 1000 and 1.3 < aspect_ratio < 3.5:
            # Проверка положения: слева или справа на экране
            if x + w < mask.shape[1] // 2:
                print(f"🟥 Обнаружен {color_name} объект слева")
                return "left"
            elif x > mask.shape[1] // 2:
                print(f"🟩 Обнаружен {color_name} объект справа")
                return "right"

    return None
