import time
import RPi.GPIO as GPIO

# --- CONFIGURATION ---
STEERING_PIN = 17   # Серво-привод (GPIO17, pin 11)
MOTOR_PIN = 14      # Мотор заднего хода (GPIO14, pin 8)
PWM_FREQ = 50       # Частота PWM
MAX_ANGLE = 30      # Максимальный угол поворота

# --- GPIO SETUP ---
GPIO.setmode(GPIO.BCM)
GPIO.setup(STEERING_PIN, GPIO.OUT)
GPIO.setup(MOTOR_PIN, GPIO.OUT)

steering_pwm = GPIO.PWM(STEERING_PIN, PWM_FREQ)
motor_pwm = GPIO.PWM(MOTOR_PIN, PWM_FREQ)
steering_pwm.start(0)
motor_pwm.start(0)

def angle_to_duty(angle):
    return 7.5 + (angle / 30) * 2.5

def steer(angle):
    duty = angle_to_duty(max(-MAX_ANGLE, min(MAX_ANGLE, angle)))
    steering_pwm.ChangeDutyCycle(duty)

def drive_forward(speed_percent=70, duration=2):
    motor_pwm.ChangeDutyCycle(speed_percent)
    time.sleep(duration)
    motor_pwm.ChangeDutyCycle(0)

def turn_right(duration=1):
    steer(30)
    time.sleep(duration)
    steer(0)

def stop_all():
    motor_pwm.ChangeDutyCycle(0)
    steering_pwm.ChangeDutyCycle(0)
    GPIO.cleanup()

# --- MAIN LOOP ---
try:
    print("🏁 Starting circular motion test...")

    for lap in range(3):
        print(f"🌀 Lap {lap+1}/3: Driving forward...")
        steer(0)
        drive_forward(duration=3)

        print("↪️ Turning right...")
        turn_right(duration=1.2)

    print("✅ Finished all laps.")

except KeyboardInterrupt:
    print("\n🛑 Interrupted manually.")

finally:
    stop_all()
