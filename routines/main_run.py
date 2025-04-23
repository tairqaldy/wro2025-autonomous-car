#!/usr/bin/env python3
# main_run.py — Universal robot script: test mode, speed_run mode, and main autonomous mode.

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))  # Ensure current directory is in import path

import time, logging, argparse
from config import DEFAULT_SPEED, PARKING_SPEED, TARGET_DISTANCE_MM, TOLERANCE_MM, TURNS_PER_LAP, TOTAL_LAPS, DEBUG_MODE
from drive.motors import drive_forward, drive_backward, stop_all
from drive.steering import steer_left, steer_right, steer_straight, steering_motor
from drive.turns import turn_left, turn_right
from sensors.ultrasonic_left import get_distance_left
from sensors.ultrasonic_right import get_distance_right
from vision.camera_usb import init_camera, capture_frame, release_camera
from vision.obstacle_detection import analyze_obstacle  # (for future obstacle avoidance, not actively used yet)
from vision.parking_detection import detect_parking_zone  # (for future parking detection)

# Configure logging (console + file), with level based on DEBUG_MODE
log_level = logging.DEBUG if DEBUG_MODE else logging.INFO
logging.basicConfig(
    level=log_level,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("run.log", mode="w", encoding="utf-8")
    ]
)

def run_test_mode():
    """Test all components sequentially: motors, steering, sensors, camera, obstacle detection, parking detection."""
    logging.info("🚦 Starting all tests (mode 'test')")

    # 1. Test drive motors forward/backward
    logging.info("🧪 Test: driving forward")
    drive_forward(speed=100, duration=2.0)   # drive forward at full speed for 2 seconds
    stop_all()
    time.sleep(1)
    logging.info("🧪 Test: driving backward")
    drive_backward(speed=100, duration=2.0)  # drive backward at full speed for 2 seconds
    stop_all()
    time.sleep(1)

    # 2. Test steering motor left/right
    logging.info("🧪 Test: steering left")
    steer_left()
    time.sleep(1)
    logging.info("🧪 Test: steering right")
    steer_right()
    time.sleep(1)
    steer_straight()  # return wheels to center

    # 3. Test ultrasonic sensors
    logging.info("🧪 Test: ultrasonic sensors")
    left_dist = get_distance_left()
    right_dist = get_distance_right()
    if left_dist >= 0:
        logging.info(f"🔵 Left distance: {left_dist:.2f} mm")
    else:
        logging.warning("🔵 Left distance: no reading (no wall detected)")
    if right_dist >= 0:
        logging.info(f"🟠 Right distance: {right_dist:.2f} mm")
    else:
        logging.warning("🟠 Right distance: no reading (no wall detected)")

    # 4. Test camera capture
    logging.info("🧪 Test: USB camera (Limelight 3A)")
    if init_camera():
        frame = capture_frame()
        if frame is not None:
            logging.info("✅ Camera frame captured successfully")
        else:
            logging.warning("⚠️ Failed to capture frame from camera")
    else:
        logging.error("❌ Camera not found or not initialized")
    release_camera()

    # 5. Test obstacle detection (vision-based) - not active in this project phase, but test function if implemented
    logging.info("🧪 Test: obstacle detection via camera")
    if init_camera():
        direction = analyze_obstacle()
        if direction == "left":
            logging.info("🟢 Obstacle detected: would avoid on left")
        elif direction == "right":
            logging.info("🟢 Obstacle detected: would avoid on right")
        else:
            logging.info("✅ No obstacles detected by vision")
    else:
        logging.error("❌ Camera not connected, skipping obstacle test")
    release_camera()

    # 6. Test parking zone detection (vision-based)
    logging.info("🧪 Test: parking zone search")
    if init_camera():
        found = detect_parking_zone()
        if found:
            logging.info("🅿️ Parking zone detected")
        else:
            logging.info("❌ Parking zone not found")
    else:
        logging.error("❌ Camera not connected, skipping parking zone test")
    release_camera()

    logging.info("✅ All tests completed")

def run_speed_mode():
    """High-speed run mode: drive straight in segments and auto-correct course at turns without full stopping."""
    logging.info("🏁 Starting speed run (mode 'speed_run')")
    try:
        while True:
            # Drive forward for a short segment
            drive_forward(speed=DEFAULT_SPEED, duration=1.2)
            stop_all()
            # Read distances on both sides
            left = get_distance_left()
            right = get_distance_right()
            logging.info(f"📏 Ultrasonic readings — Left: {left:.0f} mm, Right: {right:.0f} mm")
            # Analyze walls: if a wall disappears on either side, execute a quick steering adjustment
            if left == -1:   # left wall not detected
                logging.info("🧱 Left wall lost — steering left")
                steer_left()
                time.sleep(0.5)    # brief delay to allow the turn
                steer_straight()
            elif right == -1:  # right wall not detected
                logging.info("🧱 Right wall lost — steering right")
                steer_right()
                time.sleep(0.5)
                steer_straight()
            # Small pause before next iteration
            time.sleep(0.2)
    except KeyboardInterrupt:
        logging.info("🛑 Speed run interrupted by user")
    except Exception as e:
        logging.error(f"❌ Error in speed run mode: {e}")
    finally:
        stop_all()

def run_main_mode():
    """Main autonomous run: continuous driving with wall-centering, automatic turns, and parking at finish."""
    logging.info("🏎️ Starting main autonomous run (mode 'main')")
    # Initialization of state
    turn_counter = 0
    lap_counter = 0
    # Initialize Limelight camera (not critical if unavailable during wall-following phase)
    cam_available = init_camera()
    if not cam_available:
        logging.warning("⚠️ Limelight camera not found – skipping obstacle avoidance and parking features")
    try:
        # Main driving loop (continue until all laps completed)
        while lap_counter < TOTAL_LAPS:
            # Read both ultrasonic sensors to decide turning or centering
            left_dist = get_distance_left()
            right_dist = get_distance_right()
            # Check for missing walls (turn decision)
            if left_dist == -1 or right_dist == -1:
                if left_dist == -1 and right_dist == -1:
                    # Both walls missing (open on both sides) – default to turning left (arbitrary choice for intersection)
                    logging.info("🧭 Both walls open – defaulting to left turn")
                    turn_left()
                elif left_dist == -1:
                    # Left wall disappeared – turn left until it appears again
                    logging.info("🔄 Left turn triggered (left wall lost)")
                    turn_left()
                else:
                    # Right wall disappeared – turn right until it appears again
                    logging.info("🔄 Right turn triggered (right wall lost)")
                    turn_right()
                # After a turn, update turn count
                turn_counter += 1
                logging.info(f"🔄 Turn completed. Total turns so far: {turn_counter}")
                # Check if a lap is completed (based on number of turns)
                if turn_counter >= TURNS_PER_LAP:
                    lap_counter += 1
                    turn_counter = 0
                    logging.info(f"🏁 Lap {lap_counter} completed")
                # Pause briefly after turn for stability
                time.sleep(0.5)  # TURN_DELAY
                # Continue to next loop iteration (skip wall centering this iteration because we just turned)
                continue

            # If both sensors see a wall (no turn), drive straight and make minor adjustments if needed.
            # Centering logic: (Simplified) If both walls detected, assume we're roughly centered and go straight.
            # (Optional fine-tuning: could compare distances to center exactly, but not required in this version.)
            drive_forward(speed=DEFAULT_SPEED)
            steer_straight()
            logging.debug(f"📏 Both walls detected (L={left_dist:.0f}mm, R={right_dist:.0f}mm) — driving straight")

            # Small delay for control loop timing
            time.sleep(0.1)  # WALL_CORRECTION_DELAY

        # Completed all laps – prepare for parking phase
        logging.info("🏁 All laps completed, searching for parking zone.")
        if cam_available:
            parked = False
            while not parked:
                # Use camera to find parking zone (e.g., detect a visual marker or specific area)
                found = detect_parking_zone()
                if found:
                    logging.info("🅿️ Parking zone detected! Executing parking maneuver.")
                    stop_all()
                    # Drive forward slowly into the parking zone
                    drive_forward(speed=PARKING_SPEED, duration=1.0)
                    stop_all()
                    parked = True
                    logging.info("✅ Parking maneuver completed successfully")
                    break
                # If not found yet, inch forward and try again
                drive_forward(speed=PARKING_SPEED, duration=0.3)
                stop_all()
                time.sleep(1.0)  # PARKING_DELAY before next scan
            # Release camera after parking is done
            release_camera()
        else:
            logging.info("🎗 Skipping parking search (camera not available)")
        logging.info("🏁 Route completed")
    except KeyboardInterrupt:
        logging.warning("🛑 Autonomous run interrupted by user")
    except Exception as e:
        logging.error(f"❌ Error in autonomous mode: {e}")
    finally:
        # Stop motors on exit or interruption
        stop_all()
        if cam_available:
            release_camera()

if __name__ == "__main__":
    # Parse command-line argument for mode selection
    parser = argparse.ArgumentParser(description="Universal robot script (modes: test, speed_run, main)")
    parser.add_argument("mode", choices=["test", "speed_run", "main"], help="Operating mode: test / speed_run / main")
    args = parser.parse_args()
    try:
        if args.mode == "test":
            run_test_mode()
        elif args.mode == "speed_run":
            run_speed_mode()
        elif args.mode == "main":
            run_main_mode()
    except KeyboardInterrupt:
        logging.warning("🛑 Execution interrupted by user")
    except Exception as e:
        logging.error(f"❌ Unexpected error: {e}")
        sys.exit(1)
    finally:
        stop_all()
