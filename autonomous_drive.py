import time
import board
import busio
import digitalio
import adafruit_vl53l0x
import RPi.GPIO as GPIO

# ------------------------ Параметры ------------------------
STEERING_PIN = 12  # GPIO12 (PWM0, physical pin 32)
MOTOR_PIN = 13     # GPIO13 (PWM1, physical pin 33)
PWM_FREQ = 50      # Гц для серво и мотора
K = 0.1            # Константа масштабирования угла
MAX_ANGLE = 30     # Максимальный угол влево/вправо

# ------------------------ Настройка GPIO ------------------------
GPIO.setmode(GPIO.BCM)
GPIO.setup(STEERING_PIN, GPIO.OUT)
GPIO.setup(MOTOR_PIN, GPIO.OUT)

steering_pwm = GPIO.PWM(STEERING_PIN, PWM_FREQ)
motor_pwm = GPIO.PWM(MOTOR_PIN, PWM_FREQ)
steering_pwm.start(0)
motor_pwm.start(0)

def angle_to_duty(angle):
    # Конвертация угла [-30, 30] в duty cycle [5, 10]
    return 7.5 + (angle / 30) * 2.5  # Центр = 7.5

def set_steering(angle):
    angle = max(-MAX_ANGLE, min(MAX_ANGLE, angle))  # Ограничение угла
    duty = angle_to_duty(angle)
    steering_pwm.ChangeDutyCycle(duty)

def start_motor(speed_percent=70):
    motor_pwm.ChangeDutyCycle(speed_percent)

def stop():
    steering_pwm.ChangeDutyCycle(0)
    motor_pwm.ChangeDutyCycle(0)
    GPIO.cleanup()

# ------------------------ Настройка VL53L0X ------------------------
print("📡 Initializing I2C sensors...")

i2c = busio.I2C(board.SCL, board.SDA)

xshut_left = digitalio.DigitalInOut(board.D5)
xshut_right = digitalio.DigitalInOut(board.D6)
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

# ------------------------ Главный цикл ------------------------
print("🏁 Starting autonomous loop...")
start_motor(70)

try:
    while True:
        left = sensor_left.range
        right = sensor_right.range

        if left == 0 or right == 0:
            print("⚠️ Sensor returned 0 — possible loss")
            continue

        dir_angle = (left - right) * K
        dir_angle = max(-MAX_ANGLE, min(MAX_ANGLE, dir_angle))
        set_steering(dir_angle)

        print(f"🔵 L: {left} mm | 🟠 R: {right} mm | ➡️ Angle: {dir_angle:.1f}")
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\n🛑 Stopping...")
    stop()
