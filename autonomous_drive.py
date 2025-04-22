# autonomous_drive.py
# Basic autonomous drive script using two VL53L0X sensors and one servo motor

import time
import board
import busio
import adafruit_vl53l0x
import RPi.GPIO as GPIO

# Constants
SERVO_PIN = 17           # GPIO17 for servo motor
REAR_MOTOR_PIN = 18      # GPIO18 for rear driving motor (PWM-based)
SERVO_FREQ = 50          # Frequency for servo motor PWM
MAX_ANGLE = 30
MIN_ANGLE = -30
K = 0.5                  # Tuning constant for steering sensitivity

# Setup I2C and sensors
i2c = busio.I2C(board.SCL, board.SDA)
sensor_left = adafruit_vl53l0x.VL53L0X(i2c)
time.sleep(0.1)
sensor_left.set_address(0x30)
time.sleep(0.1)
sensor_right = adafruit_vl53l0x.VL53L0X(i2c)
time.sleep(0.1)
sensor_right.set_address(0x31)
time.sleep(0.1)

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)
GPIO.setup(REAR_MOTOR_PIN, GPIO.OUT)

servo_pwm = GPIO.PWM(SERVO_PIN, SERVO_FREQ)
rear_pwm = GPIO.PWM(REAR_MOTOR_PIN, 100)

servo_pwm.start(7.5)   # Middle (straight)
rear_pwm.start(50)     # Constant rear motor speed

def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))

def angle_to_duty(angle):
    """Convert angle to PWM duty cycle for servo"""
    duty = 7.5 + (angle / 90) * 2.5  # Approx 5 (left) to 10 (right)
    return constrain(duty, 5, 10)

try:
    print("🚗 Starting autonomous drive loop...")

    while True:
        left = sensor_left.range
        right = sensor_right.range

        # If any sensor fails, try to avoid obstacle by turning toward detected side
        if left == 0 and right != 0:
            angle = MAX_ANGLE
            print("🟠 Left sensor failed, turning RIGHT")
        elif right == 0 and left != 0:
            angle = MIN_ANGLE
            print("🔵 Right sensor failed, turning LEFT")
        elif left == 0 and right == 0:
            angle = 0
            print("⚠️ Both sensors failed, driving straight")
        else:
            angle = (left - right) * K
            angle = constrain(angle, MIN_ANGLE, MAX_ANGLE)
            print(f"📏 L: {left} mm | R: {right} mm | 🧭 Angle: {angle:.1f}°")

        # Update steering
        duty = angle_to_duty(angle)
        servo_pwm.ChangeDutyCycle(duty)

        time.sleep(0.1)

except KeyboardInterrupt:
    print("🛑 Stopping...")
    servo_pwm.stop()
    rear_pwm.stop()
    GPIO.cleanup()
