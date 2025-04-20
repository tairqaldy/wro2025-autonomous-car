# main_run.py
# Main autonomous routine: obstacle avoidance, turns, and parking

from drive.motors import drive_forward, stop_all
from sensors.color_line import check_turn_color
from sensors.ultrasonic import center_with_wall
from vision.obstacle_detection import analyze_obstacle
from vision.parking_detection import detect_parking_zone
from drive.motors import steer_straight
from drive.turns import turn_left, turn_right
import cv2
import time
from config import TOTAL_LAPS, TURNS_PER_LAP

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
                    # TODO: Implement parallel parking function
                    parking_done = True
                    break

            # 2. Obstacle detection and avoidance
            obstacle = analyze_obstacle(frame)
            if obstacle == "right":
                print("⚠️ Obstacle detected on right - avoiding")
                # TODO: Implement right obstacle avoidance
                time.sleep(0.5)  # Pause for obstacle processing
                continue
            elif obstacle == "left":
                print("⚠️ Obstacle detected on left - avoiding")
                # TODO: Implement left obstacle avoidance
                time.sleep(0.5)  # Pause for obstacle processing
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
                time.sleep(0.3)  # Pause after turn
                continue

            # 4. Wall following with continuous movement
            center_with_wall()
            drive_forward(speed=60)
            time.sleep(0.1)  # Small delay for smooth operation

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
