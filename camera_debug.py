
import cv2
import time

def find_working_camera():
    print("🔍 Поиск доступной камеры...")
    for i in range(32):
        cap = cv2.VideoCapture(i)
        if cap is not None and cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print(f"✅ Камера найдена: /dev/video{i}")
                cap.release()
                return i
            cap.release()
    print("❌ Камера не найдена.")
    return None

def show_camera(index):
    cap = cv2.VideoCapture(index)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    print("📹 Показ видеопотока. Нажмите 'q' для выхода.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ Не удалось получить кадр.")
            break
        cv2.imshow("Live Camera", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    index = find_working_camera()
    if index is not None:
        show_camera(index)
