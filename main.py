# main.py
# Запуск различных режимов работы робота в зависимости от файла mode.txt

from routines.main_run import main_autonomous_run
from routines.test_drive import run_all_tests
import sys
import time

def run_selected_mode():
    """
    Читает mode.txt и запускает соответствующий режим:
    - main  → основной автономный заезд
    - test  → тестовая проверка компонентов
    """
    try:
        with open("mode.txt", "r") as file:
            mode = file.read().strip().lower()
    except FileNotFoundError:
        print("⚠️ Файл mode.txt не найден. Используем режим 'main'")
        mode = "main"

    time.sleep(1)

    if mode == "main":
        print("🚗 Запуск основного маршрута...")
        main_autonomous_run()
    elif mode == "test":
        print("🔧 Запуск тестового режима...")
        run_all_tests()
    else:
        print(f"❗️ Неизвестный режим: {mode}. Доступны: 'main', 'test'.")
        sys.exit(1)

if __name__ == "__main__":
    try:
        run_selected_mode()
    except KeyboardInterrupt:
        print("\n🛑 Остановка пользователем")
    except Exception as e:
        print(f"❌ Ошибка выполнения: {e}")
        sys.exit(1)
