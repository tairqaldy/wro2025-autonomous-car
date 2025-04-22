# routines/speed_run.py
from drive.motors import drive_forward, stop_all
from drive.steering import steer_left, steer_right, steer_straight
from sensors.ultrasonic_left import get_distance_left
from sensors.ultrasonic_right import get_distance_right
import time

def speed_run():
    print("🏁 Starting autonomous track loop...")
    steer_straight()
    drive_forward(speed=-50)

    try:
        while True:
            left_distance = get_distance_left()
            right_distance = get_distance_right()

            if left_distance == -1:
                print("🔵 No wall on the left → turning LEFT")
                steer_left()
                time.sleep(0.3)
                
            elif right_distance == -1:
                print("🟠 No wall on the right → turning RIGHT")
                steer_right()
                time.sleep(0.3)
                
            else:
                steer_straight()

            print(f"📏 Distances | Left: {left_distance:.2f} mm | Right: {right_distance:.2f} mm")
            time.sleep(0.3)

    except KeyboardInterrupt:
        print("🛑 Stopping all motors...")
        stop_all()
        steer_straight()

# Direct run (for testing only)
if __name__ == "__main__":
    speed_run()
