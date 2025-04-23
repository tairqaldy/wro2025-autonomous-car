import time
import RPi.GPIO as GPIO

# Настройка GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)  # Серво: GPIO17 (пин 11)
GPIO.setup(14, GPIO.OUT)  # Мотор: GPIO14 (пин 8)

servo = GPIO.PWM(17, 50)  # 50 Гц для серво
motor = GPIO.PWM(14, 50)  # 50 Гц для мотора

servo.start(0)
motor.start(0)

def set_servo(angle):
    duty = 7.5 + (angle / 30) * 2.5  # Центр = 7.5; -30° = ~5; +30° = ~10
    servo.ChangeDutyCycle(duty)

def drive_forward(duration, angle=0):
    set_servo(angle)
    motor.ChangeDutyCycle(70)  # Просто езда вперёд
    time.sleep(duration)
    motor.ChangeDutyCycle(0)

try:
    while True:
        print("🚗 Едем прямо...")
        drive_forward(2, angle=0)

        print("↪️ Поворот вправо...")
        drive_forward(1, angle=25)

        print("🚗 Снова прямо...")
        drive_forward(2, angle=0)

        print("↩️ Поворот влево...")
        drive_forward(1, angle=-25)

except KeyboardInterrupt:
    print("\n🛑 Остановка...")
    motor.ChangeDutyCycle(0)
    servo.ChangeDutyCycle(0)
    GPIO.cleanup()
