# main.py
from routines.test_drive import run_all_tests
from routines.speed_run import speed_run
import sys, time

def run_selected_mode():
    try:
        with open("mode.txt", "r") as file:
            mode = file.read().strip().lower()
    except FileNotFoundError:
        print("⚠️ Файл mode.txt не найден. Используем режим 'test'")
        mode = "test"

    time.sleep(1)

    if mode == "test":
        print("🔧 Запуск тестового режима...")
        run_all_tests()
    elif mode == "speed_run":
        print("🏎️ Запуск скоростного режима...")
        speed_run()
    elif mode == "camera":
        print("🔧 Запуск теста камеры...")
        run_camera_test()
    else:
        print(f"❗ Неизвестный режим: {mode}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        run_selected_mode()
    except KeyboardInterrupt:
        print("\n🛑 Остановка пользователем")
    except Exception as e:
        print(f"❌ Ошибка выполнения: {e}")
        sys.exit(1)
