# camera_only.py
import cv2
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)

# Limelight MJPG stream URL
CAMERA_URL = "http://limelight.local:5800/stream.mjpg"

# HSV color ranges
HSV_RANGES = {
    "red1": ((0, 100, 100), (10, 255, 255)),
    "red2": ((160, 100, 100), (180, 255, 255)),
    "green": ((50, 80, 80), (85, 255, 255)),
}

def detect_objects(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    detected = []

    # Red (two ranges due to hue wraparound)
    mask_red1 = cv2.inRange(hsv, *HSV_RANGES["red1"])
    mask_red2 = cv2.inRange(hsv, *HSV_RANGES["red2"])
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)

    # Green
    mask_green = cv2.inRange(hsv, *HSV_RANGES["green"])

    # Analyze contours
    for mask, color in [(mask_red, "RED"), (mask_green, "GREEN")]:
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 300:  # filter out small noise
                x, y, w, h = cv2.boundingRect(cnt)
                cx = x + w // 2
                cy = y + h // 2
                detected.append((color, area, (cx, cy)))

    return detected

def main():
    cap = cv2.VideoCapture(CAMERA_URL)
    if not cap.isOpened():
        logging.error("❌ Could not open camera stream at %s", CAMERA_URL)
        return

    logging.info("✅ Камера Limelight подключена через HTTP")

    while True:
        ret, frame = cap.read()
        if not ret:
            logging.warning("⚠️ Frame not received")
            continue

        detections = detect_objects(frame)
        if detections:
            print("\n📸 Объекты обнаружены:")
            for color, area, (cx, cy) in detections:
                print(f"🟢 Цвет: {color} | 📏 Площадь: {area:.0f} | 📍 Центр: ({cx}, {cy})")
        else:
            print("🔍 Объекты не найдены")

if __name__ == "__main__":
    main()
