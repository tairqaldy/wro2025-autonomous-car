# main_run.py
# Main autonomous routine: obstacle avoidance, turns, and parking

from drive.motors import drive_forward, stop_all, steering_motor
from sensors.color_line import check_turn_color
from sensors.ultrasonic import center_with_wall, ultrasonic_sensor
from drive.turns import turn_left, turn_right
from config import (
    TOTAL_LAPS, TURNS_PER_LAP, DEFAULT_SPEED,
    TURN_ANGLE, TARGET_DISTANCE_MM,
    TURN_DELAY, WALL_CORRECTION_DELAY
)
import time

# State tracking
turn_counter = 0
lap_counter = 0

def main_autonomous_run():
    global turn_counter, lap_counter

    try:
        while lap_counter < TOTAL_LAPS:
            # Turn detection
            result = check_turn_color()
            if result in ["left", "right"]:
                if result == "left":
                    turn_left()
                else:
                    turn_right()
                turn_counter += 1
                print(f"🔄 {result.capitalize()} turn completed. Total: {turn_counter}")

                if turn_counter >= TURNS_PER_LAP:
                    lap_counter += 1
                    turn_counter = 0
                    print(f"🏁 Lap {lap_counter} completed")
                time.sleep(TURN_DELAY)
                continue

            # Fallback wall following
            distance = ultrasonic_sensor.get_distance()
            if distance == -1:
                drive_forward(speed=DEFAULT_SPEED)
            elif distance > TARGET_DISTANCE_MM + 5:
                steering_motor.run_for_degrees(-5, 30)
                drive_forward(speed=DEFAULT_SPEED)
            elif distance < TARGET_DISTANCE_MM - 5:
                steering_motor.run_for_degrees(5, 30)
                drive_forward(speed=DEFAULT_SPEED)
            else:
                steering_motor.run_to_position(0)
                drive_forward(speed=DEFAULT_SPEED)

            time.sleep(WALL_CORRECTION_DELAY)

    except KeyboardInterrupt:
        print("\n🛑 Autonomous run interrupted by user")
    except Exception as e:
        print(f"❌ Error in autonomous run: {e}")
    finally:
        print("🏁 Route completed")
        stop_all()

if __name__ == "__main__":
    main_autonomous_run()
