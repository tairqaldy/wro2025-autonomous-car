# main_run.py
# Main autonomous routine: obstacle avoidance, turns, and parking

from drive.motors import drive_forward, stop_all, steering_motor
from sensors.color_line import check_turn_color
from sensors.ultrasonic import center_with_wall, get_distance
from vision.obstacle_detection import analyze_obstacle
from vision.parking_detection import detect_parking_zone
from drive.motors import steer_straight
from drive.turns import turn_left, turn_right
import cv2
import time
from config import (
    TOTAL_LAPS, TURNS_PER_LAP, DEFAULT_SPEED, PARKING_SPEED,
    TURN_ANGLE, PARKING_TURN_ANGLE, TARGET_DISTANCE_MM,
    TURN_DELAY, OBSTACLE_DELAY, WALL_CORRECTION_DELAY, PARKING_DELAY
)

# Camera setup with error handling
try:
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        raise Exception("Camera initialization failed")
except Exception as e:
    print(f"❌ Camera error: {e}")
    raise

# State tracking
turn_counter = 0
lap_counter = 0
parking_done = False

def avoid_obstacle(direction):
    """
    Executes obstacle avoidance maneuver
    Args:
        direction (str): "left" or "right" indicating which side to avoid
    """
    print(f"🔄 Avoiding obstacle on {direction}")
    if direction == "right":
        # Move slightly left to avoid right obstacle
        steering_motor.run_for_degrees(-TURN_ANGLE//2, 30)
        drive_forward(speed=DEFAULT_SPEED, duration=0.5)
        stop_all()
        steering_motor.run_to_position(0)
    else:
        # Move slightly right to avoid left obstacle
        steering_motor.run_for_degrees(TURN_ANGLE//2, 30)
        drive_forward(speed=DEFAULT_SPEED, duration=0.5)
        stop_all()
        steering_motor.run_to_position(0)
    time.sleep(OBSTACLE_DELAY)

def parallel_park():
    """
    Executes parallel parking maneuver
    """
    print("🅿️ Starting parallel parking")
    # Initial positioning
    drive_forward(speed=PARKING_SPEED, duration=0.5)
    stop_all()
    
    # First turn
    steering_motor.run_for_degrees(PARKING_TURN_ANGLE, 30)
    drive_forward(speed=PARKING_SPEED, duration=0.8)
    stop_all()
    
    # Second turn
    steering_motor.run_for_degrees(-PARKING_TURN_ANGLE, 30)
    drive_forward(speed=PARKING_SPEED, duration=0.8)
    stop_all()
    
    # Final adjustment
    steering_motor.run_to_position(0)
    drive_forward(speed=PARKING_SPEED, duration=0.3)
    stop_all()
    
    time.sleep(PARKING_DELAY)
    print("✅ Parking completed")

def main_autonomous_run():
    """
    Main autonomous driving routine that handles:
    - Obstacle detection and avoidance
    - Color-based turns
    - Wall following
    - Final parking
    """
    global turn_counter, lap_counter, parking_done

    try:
        while lap_counter < TOTAL_LAPS:
            # Camera frame capture with error handling
            ret, frame = camera.read()
            if not ret:
                print("⚠️ Camera frame capture failed, retrying...")
                time.sleep(0.1)
                continue

            # 1. Parking detection (only on final lap)
            if lap_counter == TOTAL_LAPS - 1 and not parking_done:
                if detect_parking_zone(frame):
                    print("🅿️ Final parking zone detected - initiating parking")
                    stop_all()
                    parallel_park()
                    parking_done = True
                    break

            # 2. Obstacle detection and avoidance
            obstacle = analyze_obstacle(frame)
            if obstacle == "right":
                avoid_obstacle("right")
                continue
            elif obstacle == "left":
                avoid_obstacle("left")
                continue

            # 3. Color-based turn detection
            result = check_turn_color()
            if result in ["left", "right"]:
                turn_counter += 1
                print(f"🔄 {result.capitalize()} turn completed. Total: {turn_counter}")

                if turn_counter >= TURNS_PER_LAP:
                    lap_counter += 1
                    turn_counter = 0
                    print(f"🏁 Lap {lap_counter} completed")
                time.sleep(TURN_DELAY)
                continue

            # 4. Wall following with continuous movement
            center_with_wall()
            drive_forward(speed=DEFAULT_SPEED)
            time.sleep(WALL_CORRECTION_DELAY)

    except KeyboardInterrupt:
        print("\n🛑 Autonomous run interrupted by user")
    except Exception as e:
        print(f"❌ Error in autonomous run: {e}")
    finally:
        print("🏁 Route completed")
        stop_all()
        camera.release()

if __name__ == "__main__":
    main_autonomous_run()
