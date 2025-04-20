# main.py
# Автозапуск по режиму из файла (main или speed)

from routines.main_run import main_autonomous_run
from routines.speed_run import fast_speed_run


def run_selected_mode():
    try:
        with open("mode.txt", "r") as file:
            mode = file.read().strip().lower()
    except FileNotFoundError:
        mode = "main"

    if mode == "main":
        print("🚗 Запуск основного маршрута...")
        main_autonomous_run()
    elif mode == "speed":
        print("⚡️ Запуск скоростного заезда...")
        fast_speed_run()
    else:
        print(f"❗️ Неизвестный режим: {mode}")


if __name__ == "__main__":
    run_selected_mode()
