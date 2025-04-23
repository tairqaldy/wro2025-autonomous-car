import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

motor = GPIO.PWM(18, 50)
motor.start(0)

try:
    print("🚀 Мотор на 70%")
    motor.ChangeDutyCycle(70)
    time.sleep(3)
    print("🛑 Стоп")
    motor.ChangeDutyCycle(0)
    motor.stop()
    GPIO.cleanup()

except KeyboardInterrupt:
    GPIO.cleanup()
