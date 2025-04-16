from buildhat import Motor
from time import sleep, time

rear_motor = Motor('A')    # Задний мотор
front_motor = Motor('C')   # Передний мотор

print("Запуск. Длительность: 10 секунд.")

# Запускаем задний мотор
rear_motor.start(25)

# Настройки
turn_speed = 50
turn_duration = 2
start_time = time()
direction = 1

while time() - start_time < 10:
    front_motor.run_for_degrees(90 * direction, speed=turn_speed)
    direction *= -1
    sleep(turn_duration)

# Явная остановка и сброс
rear_motor.stop()
rear_motor.set_default_speed(0)
front_motor.stop()

print("Остановка завершена.")
