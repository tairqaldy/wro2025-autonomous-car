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

# Global variables for lap counting
line_counter = 0
lap_counter = 0
last_color = None  # To avoid counting the same line multiple times
error_count = 0    # Counter for consecutive errors
MAX_ERRORS = 3     # Maximum number of consecutive errors before stopping

def get_smoothed_distance(samples=3):
    """
    Get smoothed distance reading by averaging multiple samples
    Args:
        samples (int): Number of samples to average
    Returns:
        float: Averaged distance in millimeters
    """
    readings = []
    for _ in range(samples):
        try:
            distance = ultrasonic_sensor.get_distance()
            if distance != -1:  # Only use valid readings
                readings.append(distance)
            time.sleep(WALL_READ_DELAY)
        except Exception as e:
            print(f"⚠️ Error reading distance: {e}")
            continue
    
    if not readings:
        return -1
    return sum(readings) / len(readings)

def update_lap_counter(color):
    """
    Update lap counter based on color detection
    Args:
        color (str): Detected color
    Returns:
        bool: True if lap completed, False otherwise
    """
    global line_counter, lap_counter, last_color
    
    # Skip if same color detected multiple times
    if color == last_color:
        return False
    
    last_color = color
    line_counter += 1
    print(f"📊 Line detected: {color}. Total lines: {line_counter}")
    
    # Check if lap completed
    if line_counter >= LINES_PER_LAP:
        lap_counter += 1
        line_counter = 0
        print(f"🏁 Lap {lap_counter} completed!")
        return True
    
    return False

def detect_turn_color():
    """
    Detect turn color with priority:
    - If blue detected first -> left turn
    - If orange detected first, then blue -> right turn
    Returns:
        str: "left", "right", or None
    """
    try:
        # Slow down for better color detection
        drive_forward(speed=COLOR_DETECTION_SPEED)
        
        # First color check
        first_color = check_turn_color()
        time.sleep(COLOR_READ_DELAY)
        
        if first_color == BLUE:
            print("🔵 Blue detected -> Left turn")
            update_lap_counter(BLUE)
            return "left"
        elif first_color == ORANGE:
            # Check for blue after orange
            time.sleep(COLOR_DETECTION_DURATION)
            second_color = check_turn_color()
            if second_color == BLUE:
                print("🟠 Orange then Blue detected -> Right turn")
                update_lap_counter(ORANGE)
                update_lap_counter(BLUE)
                return "right"
            elif second_color == ORANGE:
                update_lap_counter(ORANGE)
        
        return None
    except Exception as e:
        print(f"⚠️ Error in color detection: {e}")
        return None

def execute_turn(direction):
    """
    Execute a turn in the specified direction
    Args:
        direction (str): "left" or "right"
    """
    print(f"🔄 Executing {direction} turn")
    
    try:
        # Set turn angle
        angle = -TURN_ANGLE if direction == "left" else TURN_ANGLE
        steering_motor.run_for_degrees(angle, 30)
        
        # Execute turn at slow speed
        drive_forward(speed=TURN_SPEED)
        time.sleep(TURN_DURATION)
        
        # Check wall distance during turn
        distance = get_smoothed_distance()
        if distance == -1 or distance > MAX_WALL_DISTANCE:
            print("⚠️ Wall lost during turn, stopping")
            stop_all()
            return False
        
        # Stop and straighten
        stop_all()
        steering_motor.run_to_position(STRAIGHT_ANGLE)
        time.sleep(0.2)  # Wait for steering to settle
        return True
    except Exception as e:
        print(f"⚠️ Error during turn: {e}")
        stop_all()
        return False

def search_for_wall():
    """
    Search for wall using snake movement pattern
    Returns:
        bool: True if wall found, False if timeout
    """
    print("🔍 Starting wall search with snake movement...")
    start_time = time.time()
    turn_direction = 1  # 1 for right, -1 for left
    
    while time.time() - start_time < WALL_SEARCH_TIMEOUT:
        try:
            # Check for wall
            distance = get_smoothed_distance()
            if distance != -1 and distance <= MAX_WALL_DISTANCE:
                print("✅ Wall found!")
                return True
                
            # Execute snake movement
            # Turn
            steering_motor.run_for_degrees(turn_direction * SNAKE_TURN_ANGLE, 30)
            drive_forward(speed=WALL_SEARCH_SPEED)
            time.sleep(SNAKE_TURN_DELAY)
            
            # Move forward
            steering_motor.run_to_position(STRAIGHT_ANGLE)
            drive_forward(speed=WALL_SEARCH_SPEED)
            time.sleep(SNAKE_FORWARD_DELAY)
            
            # Reverse turn direction
            turn_direction *= -1
            
        except Exception as e:
            print(f"⚠️ Error during wall search: {e}")
            continue
            
    print("⚠️ Wall search timeout")
    return False

def wall_following():
    """
    Wall following routine that:
    - Maintains precise 80mm distance from wall
    - Implements smooth corrections
    - Provides safety checks
    - Uses averaged distance readings
    - Searches for wall if lost
    - Prioritizes color detection for turns
    - Counts laps through line detection
    """
    global line_counter, lap_counter, last_color, error_count
    
    print("🚦 Starting wall following...")
    
    try:
        # Ensure steering is straight
        steering_motor.run_to_position(STRAIGHT_ANGLE)
        time.sleep(0.2)  # Wait for steering to settle
        
        # Start movement
        drive_forward(speed=WALL_FOLLOW_SPEED)
        
        while lap_counter < TOTAL_LAPS:
            try:
                # Check for turn colors
                turn_direction = detect_turn_color()
                if turn_direction:
                    if not execute_turn(turn_direction):
                        error_count += 1
                        if error_count >= MAX_ERRORS:
                            print("❌ Too many errors during turns, stopping")
                            break
                    continue
                
                # Get smoothed distance reading
                distance = get_smoothed_distance()
                
                # Check if wall is lost
                if distance == -1 or distance > MAX_WALL_DISTANCE:
                    print("⚠️ Wall lost, starting search...")
                    stop_all()
                    if not search_for_wall():
                        print("❌ Failed to find wall, stopping")
                        break
                    # Reset error count on successful wall find
                    error_count = 0
                    # Resume wall following after finding wall
                    drive_forward(speed=WALL_FOLLOW_SPEED)
                    continue
                
                # Emergency stop if too close
                if distance < MIN_WALL_DISTANCE:
                    print("⚠️ Emergency stop: Too close to wall")
                    stop_all()
                    break
                
                # Calculate distance error
                error = distance - TARGET_DISTANCE_MM
                
                # Only correct if error is significant
                if abs(error) > CORRECTION_THRESHOLD:
                    if error > 0:  # Too far from wall
                        # Turn slightly towards wall
                        correction = min(error * 0.5, WALL_CORRECTION_ANGLE)
                        steering_motor.run_for_degrees(-correction, 30)
                    else:  # Too close to wall
                        # Turn slightly away from wall
                        correction = min(abs(error) * 0.5, WALL_CORRECTION_ANGLE)
                        steering_motor.run_for_degrees(correction, 30)
                else:
                    # Maintain straight course
                    steering_motor.run_to_position(STRAIGHT_ANGLE)
                
                # Adjust speed based on error
                if abs(error) > TOLERANCE_MM:
                    # Slow down when making corrections
                    current_speed = max(MIN_SPEED, WALL_FOLLOW_SPEED - abs(error))
                    drive_forward(speed=int(current_speed))
                else:
                    drive_forward(speed=WALL_FOLLOW_SPEED)
                
                time.sleep(WALL_CORRECTION_DELAY)
                
            except Exception as e:
                print(f"⚠️ Error in main loop: {e}")
                error_count += 1
                if error_count >= MAX_ERRORS:
                    print("❌ Too many errors, stopping")
                    break
                continue
            
        print(f"🏁 Race completed! Total laps: {lap_counter}")
            
    except KeyboardInterrupt:
        print("\n🛑 Wall following interrupted by user")
    except Exception as e:
        print(f"❌ Error in wall following: {e}")
    finally:
        print("🏁 Wall following completed")
        stop_all()
        steering_motor.run_to_position(STRAIGHT_ANGLE)

if __name__ == "__main__":
    wall_following()
