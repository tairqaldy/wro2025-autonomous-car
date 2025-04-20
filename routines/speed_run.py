# speed_run.py
# Wall following and color detection routine with lap counting

from drive.motors import drive_forward, stop_all, steering_motor
from sensors.ultrasonic import ultrasonic_sensor
from sensors.color_line import check_turn_color
from config import (
    WALL_FOLLOW_SPEED, WALL_SEARCH_SPEED, MIN_SPEED,
    COLOR_DETECTION_SPEED, TURN_SPEED,
    STRAIGHT_ANGLE, WALL_CORRECTION_ANGLE, SNAKE_TURN_ANGLE,
    TURN_ANGLE, BLUE, ORANGE,
    TARGET_DISTANCE_MM, TOLERANCE_MM,
    MIN_WALL_DISTANCE, MAX_WALL_DISTANCE,
    CORRECTION_THRESHOLD, WALL_SEARCH_TIMEOUT,
    WALL_CORRECTION_DELAY, WALL_READ_DELAY,
    SNAKE_TURN_DELAY, SNAKE_FORWARD_DELAY,
    COLOR_READ_DELAY, TURN_DURATION,
    COLOR_DETECTION_DURATION, LINES_PER_LAP, TOTAL_LAPS
)
import time

line_counter = 0
lap_counter = 0
last_color = None
error_count = 0
MAX_ERRORS = 3

def get_smoothed_distance(samples=3):
    readings = []
    for _ in range(samples):
        try:
            distance = ultrasonic_sensor.get_distance()
            if distance != -1:
                readings.append(distance)
            time.sleep(WALL_READ_DELAY)
        except:
            continue
    if not readings:
        return -1
    return sum(readings) / len(readings)

def update_lap_counter(color):
    global line_counter, lap_counter, last_color
    if color == last_color:
        return False
    last_color = color
    line_counter += 1
    print(f"📊 Line: {color}, Count: {line_counter}")
    if line_counter >= LINES_PER_LAP:
        lap_counter += 1
        line_counter = 0
        print(f"🏁 Lap {lap_counter} complete!")
        return True
    return False

def detect_turn_color():
    try:
        drive_forward(speed=COLOR_DETECTION_SPEED)
        first_color = check_turn_color()
        time.sleep(COLOR_READ_DELAY)
        if first_color == BLUE:
            print("🔵 Blue = Left Turn")
            update_lap_counter(BLUE)
            return "left"
        elif first_color == ORANGE:
            time.sleep(COLOR_DETECTION_DURATION)
            second_color = check_turn_color()
            if second_color == BLUE:
                print("🟠→🔵 Orange+Blue = Right Turn")
                update_lap_counter(ORANGE)
                update_lap_counter(BLUE)
                return "right"
            elif second_color == ORANGE:
                update_lap_counter(ORANGE)
        return None
    except Exception as e:
        print(f"⚠️ Color Error: {e}")
        return None

def execute_turn(direction):
    try:
        print(f"🔄 Turn: {direction}")
        angle = -TURN_ANGLE if direction == "left" else TURN_ANGLE
        steering_motor.run_for_degrees(angle, 30)
        drive_forward(speed=TURN_SPEED)
        time.sleep(TURN_DURATION)
        distance = get_smoothed_distance()
        if distance == -1 or distance > MAX_WALL_DISTANCE:
            print("❌ Wall lost during turn")
            stop_all()
            return False
        stop_all()
        steering_motor.run_to_position(STRAIGHT_ANGLE)
        time.sleep(0.2)
        return True
    except Exception as e:
        print(f"⚠️ Turn Error: {e}")
        stop_all()
        return False

def wall_following():
    global error_count
    print("🚦 Starting speed mode wall following")
    steering_motor.run_to_position(STRAIGHT_ANGLE)
    time.sleep(0.2)
    drive_forward(speed=WALL_FOLLOW_SPEED)
    while lap_counter < TOTAL_LAPS:
        try:
            turn_direction = detect_turn_color()
            if turn_direction:
                if not execute_turn(turn_direction):
                    error_count += 1
                    if error_count >= MAX_ERRORS:
                        print("❌ Too many turn errors")
                        break
                continue
            distance = get_smoothed_distance()
            if distance == -1 or distance > MAX_WALL_DISTANCE:
                print("⚠️ Wall lost, continuing straight")
                drive_forward(speed=WALL_FOLLOW_SPEED)
                continue
            if distance < MIN_WALL_DISTANCE:
                print("⚠️ Too close to wall")
                stop_all()
                break
            error = distance - TARGET_DISTANCE_MM
            if abs(error) > CORRECTION_THRESHOLD:
                correction = min(abs(error) * 0.5, WALL_CORRECTION_ANGLE)
                if error > 0:
                    steering_motor.run_for_degrees(-correction, 30)
                else:
                    steering_motor.run_for_degrees(correction, 30)
            else:
                steering_motor.run_to_position(STRAIGHT_ANGLE)
            speed = max(MIN_SPEED, WALL_FOLLOW_SPEED - abs(error)) if abs(error) > TOLERANCE_MM else WALL_FOLLOW_SPEED
            drive_forward(speed=int(speed))
            time.sleep(WALL_CORRECTION_DELAY)
        except Exception as e:
            print(f"⚠️ Main Loop Error: {e}")
            error_count += 1
            if error_count >= MAX_ERRORS:
                print("❌ Critical Error Threshold Exceeded")
                break
    print(f"🏁 Speed mode complete. Laps: {lap_counter}")
    stop_all()
    steering_motor.run_to_position(STRAIGHT_ANGLE)

if __name__ == "__main__":
    wall_following()