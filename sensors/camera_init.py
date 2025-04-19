# camera_init.py
# Тестовое окно камеры с отображением прямого потока

import cv2

def show_camera_feed():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Ошибка: Камера не обнаружена")
        return

    print("Поток камеры запущен. Нажмите 'q' для выхода.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Ошибка захвата кадра")
            break

        cv2.imshow("Camera Preview", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    show_camera_feed()
