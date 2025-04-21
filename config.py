# config.py
# Global configuration for WRO 2025 autonomous robot

# === Movement Speeds ===
DEFAULT_SPEED = 80             # Общая скорость по умолчанию
DRIVE_SPEED = 70               # Используется в drive_forward/backward
PARKING_SPEED = 30             # Медленное движение при парковке
MIN_SPEED = 30                 # Минимально допустимая скорость
MAX_SPEED = 100                # Максимальная безопасная скорость

# === Steering Parameters ===
STRAIGHT_ANGLE = 0             # Угол выравнивания руля
MAX_TURN_ANGLE = 25           # Угол поворота влево/вправо в градусах (ограничен из-за физики)

# === Ultrasonic Sensor Settings ===
TARGET_DISTANCE_MM = 300       # Расстояние до стены при центрировании
TOLERANCE_MM = 10              # Допустимая погрешность (мм)

# === Lap Logic (для будущих speed- и main-запусков) ===
TURNS_PER_LAP = 4              # Кол-во поворотов на круг
TOTAL_LAPS = 3                 # Общее кол-во кругов

# === Timing Delays ===
WALL_CORRECTION_DELAY = 0.1    # Задержка после корректировки руля по стенке
TURN_DELAY = 0.5               # Задержка после завершения поворота
PARKING_DELAY = 1.0            # Задержка между фазами парковки

# === USB Camera Settings ===
CAMERA_INDEX = "/dev/video10"              # Индекс камеры в OpenCV
FRAME_WIDTH = 640              # Ширина кадра
FRAME_HEIGHT = 480             # Высота кадра

# === Debug Mode ===
DEBUG_MODE = True              # Включение/отключение отладочных сообщений
