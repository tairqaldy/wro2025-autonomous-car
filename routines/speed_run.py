# speed_run.py
# High-speed racing routine with wall following and color-based turns

from drive.motors import drive_forward, stop_all, steering_motor
from sensors.color_line import check_turn_color
from sensors.ultrasonic import ultrasonic_sensor
from config import DEFAULT_SPEED, TURN_ANGLE
import time

# Wall following parameters
TARGET_DISTANCE_MM = 300  # Target distance from wall in millimeters
TOLERANCE_MM = 20        # Acceptable deviation from target distance

# Race parameters
TOTAL_TURNS = 12         # Total number of turns to complete
turn_counter = 0         # Current turn count
first_turn_completed = False  # Flag for first turn completion

def fast_speed_run():
    """
    High-speed racing routine that:
    - Handles initial turn detection
    - Performs color-based turns
    - Maintains wall following
    - Tracks turn completion
    """
    global turn_counter, first_turn_completed
    
    print("🚦 Starting movement...")
    
    try:
        while turn_counter < TOTAL_TURNS:
            # Initial phase - waiting for first turn
            if not first_turn_completed:
                turn_direction = check_turn_color()
                if turn_direction == "left":
                    print("🔵 First left turn detected (Cyan)")
                    execute_turn("left")
                    first_turn_completed = True
                    turn_counter += 1
                    time.sleep(0.5)  # Recovery time after turn
                    continue
                elif turn_direction == "right":
                    print("🔴 First right turn detected (Red)")
                    execute_turn("right")
                    first_turn_completed = True
                    turn_counter += 1
                    time.sleep(0.5)  # Recovery time after turn
                    continue
                else:
                    drive_forward(speed=DEFAULT_SPEED)
                    time.sleep(0.1)  # Small delay for smooth operation
                    continue

            # Main racing phase - color detection and wall following
            color_result = check_turn_color()
            if color_result == "left":
                print("🔵 Left turn detected (Cyan)")
                execute_turn("left")
                turn_counter += 1
                time.sleep(0.5)  # Recovery time after turn
                continue
            elif color_result == "right":
                print("🔴 Right turn detected (Red)")
                execute_turn("right")
                turn_counter += 1
                time.sleep(0.5)  # Recovery time after turn
                continue

            # Wall following logic
            distance = ultrasonic_sensor.get_distance()
            if distance == -1:
                drive_forward(speed=DEFAULT_SPEED)
            elif distance > TARGET_DISTANCE_MM + TOLERANCE_MM:
                steering_motor.run_for_degrees(-5, 30)
                drive_forward(speed=DEFAULT_SPEED)
            elif distance < TARGET_DISTANCE_MM - TOLERANCE_MM:
                steering_motor.run_for_degrees(5, 30)
                drive_forward(speed=DEFAULT_SPEED)
            else:
                steering_motor.run_to_position(0)
                drive_forward(speed=DEFAULT_SPEED)

            time.sleep(0.1)  # Control loop delay

    except KeyboardInterrupt:
        print("\n🛑 Speed run interrupted by user")
    except Exception as e:
        print(f"❌ Error in speed run: {e}")
    finally:
        print("✅ Track completed")
        stop_all()
        input("🔚 Press Enter to stop\n")
        stop_all()

def execute_turn(direction):
    """
    Executes a turn in the specified direction
    Args:
        direction (str): "left" or "right"
    """
    angle = -TURN_ANGLE if direction == "left" else TURN_ANGLE
    steering_motor.run_for_degrees(angle, 40)
    drive_forward(speed=DEFAULT_SPEED, duration=0.8)
    stop_all()
    steering_motor.run_to_position(0)

if __name__ == "__main__":
    fast_speed_run()
