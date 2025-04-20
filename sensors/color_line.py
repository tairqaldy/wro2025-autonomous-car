# color_line.py
# Обработка поворотов по цвету линии на полу

from buildhat import ColorSensor
from drive.turns import turn_left, turn_right

color_sensor = ColorSensor('D')  # Порт, где подключён сенсор

# Цвета, определяющие направление
BLUE = 'blue'
ORANGE = 'orange'

def check_turn_color():
    color = color_sensor.get_color()
    print(f"Обнаружен цвет: {color}")

    if color == BLUE:
        turn_left()
        return "left"
    elif color == ORANGE:
        turn_right()
        return "right"
    return "none"
