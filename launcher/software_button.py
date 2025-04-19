# software_button.py
# Выбор между основным заездом и скоростным режимом без физической кнопки

from routines.main_run import main_autonomous_run
from routines.speed_run import fast_speed_run

def wait_for_software_start():
    print("Выберите режим запуска:")
    print("1 — Основной автономный маршрут")
    print("2 — Скоростной заезд")
    choice = input("Введите 1 или 2: ").strip()

    if choice == "1":
        print("Запуск основного автономного маршрута...")
        main_autonomous_run()
    elif choice == "2":
        print("Запуск скоростного заезда...")
        fast_speed_run()
    else:
        print("Некорректный выбор. Попробуйте снова.")
        wait_for_software_start()

if __name__ == "__main__":
    wait_for_software_start()