# routines/speed_run.py

import time
from drive.motors import drive_forward, stop_all
from drive.steering import steer_left, steer_right, steer_straight
from sensors.ultrasonic_left import get_distance_left
from sensors.ultrasonic_right import get_distance_right

def run_speed_mode():
    print("🏁 Starting autonomous track loop...")

    lost_wall_left_counter = 0
    lost_wall_right_counter = 0
    steer_straight()
    drive_forward(speed=60)  # PWM может быть -50 или 50 — зависит от подключения

    try:
        while True:
            left_distance = get_distance_left()
            right_distance = get_distance_right()

            print(f"📏 Distances | Left: {left_distance:.2f} mm | Right: {right_distance:.2f} mm")

            # Потеря стены
            if left_distance == -1:
                lost_wall_left_counter += 1
            else:
                lost_wall_left_counter = 0

            if right_distance == -1:
                lost_wall_right_counter += 1
            else:
                lost_wall_right_counter = 0

            # Логика объезда
            if lost_wall_left_counter >= 2:
                print("🔵 No wall on the left → turning LEFT")
                steer_left()
                time.sleep(0.3)
                steer_straight()

            elif lost_wall_right_counter >= 2:
                print("🟠 No wall on the right → turning RIGHT")
                steer_right()
                time.sleep(0.3)
                steer_straight()

            else:
                steer_straight()

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("🛑 Stopping all motors...")
        stop_all()
        steer_straight()

# Direct run
if __name__ == "__main__":
    run_speed_mode()
