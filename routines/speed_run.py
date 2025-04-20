# speed_run.py
# Simplified version: just drive forward and count laps

from drive.motors import drive_forward, stop_all, steering_motor
from config import DEFAULT_SPEED, TURNS_PER_LAP, TOTAL_LAPS, WALL_CORRECTION_DELAY
import time

lap_counter = 0
turn_counter = 0

def fast_speed_run():
    """
    Simple autonomous loop for speed run. Drives forward and counts laps.
    """
    global lap_counter, turn_counter

    print("🚦 Начинаем упрощённый скоростной заезд (только движение по кругам)...")

    try:
        while lap_counter < TOTAL_LAPS:
            # Просто едем прямо и симулируем повороты через интервалы
            drive_forward(speed=DEFAULT_SPEED)
            time.sleep(2)  # Длительность между поворотами/секторами трассы (подбери вручную)

            turn_counter += 1
            print(f"🔁 Поворот #{turn_counter}")

            if turn_counter >= TURNS_PER_LAP:
                lap_counter += 1
                turn_counter = 0
                print(f"🏁 Круг {lap_counter} завершён")

        print("✅ Все круги завершены!")

    except KeyboardInterrupt:
        print("🛑 Остановлено пользователем")
    finally:
        stop_all()
        steering_motor.run_to_position(0)
        print("🏁 Остановлено")

if __name__ == "__main__":
    fast_speed_run()
