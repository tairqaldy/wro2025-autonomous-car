import time
import board
import busio
import digitalio
import adafruit_vl53l0x
import RPi.GPIO as GPIO
from adafruit_blinka.microcontroller.bcm283x import pin

# --- CONFIGURATION ---
STEERING_PIN = 17   # Servo (GPIO17, physical pin 11)
MOTOR_PIN = 14      # Rear Motor (GPIO14, physical pin 8)
PWM_FREQ = 50
K = 0.1
MAX_ANGLE = 30

# --- GPIO SETUP ---
GPIO.setmode(GPIO.BCM)
GPIO.setup(STEERING_PIN, GPIO.OUT)
GPIO.setup(MOTOR_PIN, GPIO.OUT)

steering_pwm = GPIO.PWM(STEERING_PIN, PWM_FREQ)
motor_pwm = GPIO.PWM(MOTOR_PIN, PWM_FREQ)
steering_pwm.start(0)
motor_pwm.start(0)

def angle_to_duty(angle):
    return 7.5 + (angle / 30) * 2.5  # -30°→5, 0°→7.5, +30°→10

def set_steering(angle):
    angle = max(-MAX_ANGLE, min(MAX_ANGLE, angle))
    steering_pwm.ChangeDutyCycle(angle_to_duty(angle))

def start_motor(speed_percent=70):
    motor_pwm.ChangeDutyCycle(speed_percent)

def stop():
    steering_pwm.ChangeDutyCycle(0)
    motor_pwm.ChangeDutyCycle(0)
    GPIO.cleanup()

# --- SENSOR SETUP ---
print("📡 Initializing VL53L0X sensors...")

i2c = busio.I2C(board.SCL, board.SDA)

xshut_left = digitalio.DigitalInOut(board.D27)   # GPIO 0 (pin 27)
xshut_right = digitalio.DigitalInOut(board.D28)  # GPIO 1 (pin 28)
xshut_left.direction = digitalio.Direction.OUTPUT
xshut_right.direction = digitalio.Direction.OUTPUT

xshut_left.value = False
xshut_right.value = False
time.sleep(0.5)

xshut_left.value = True
time.sleep(0.5)
sensor_left = adafruit_vl53l0x.VL53L0X(i2c)
sensor_left.set_address(0x30)
print("✅ Left sensor (0x30) initialized")

xshut_right.value = True
time.sleep(0.5)
sensor_right = adafruit_vl53l0x.VL53L0X(i2c)
sensor_right.set_address(0x31)
print("✅ Right sensor (0x31) initialized")

# --- AUTONOMOUS LOOP ---
print("🏁 Starting loop...")
start_motor(70)

try:
    while True:
        left = sensor_left.range
        right = sensor_right.range

        if left == 0 or right == 0:
            print("⚠️ Sensor error: One of them returned 0")
            continue

        dir_angle = (left - right) * K
        dir_angle = max(-MAX_ANGLE, min(MAX_ANGLE, dir_angle))
        set_steering(dir_angle)

        print(f"🔵 L: {left} mm | 🟠 R: {right} mm | ➡️ Angle: {dir_angle:.1f}")
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\n🛑 Stopping...")
    stop()
