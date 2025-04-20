# color_line.py
# Обработка поворотов по цвету линии на полу

from buildhat import ColorSensor
from drive.turns import perform_left_turn, perform_right_turn

color_sensor = ColorSensor('D')  # Порт, где подключён сенсор

# Цвета, определяющие направление
BLUE = 'blue'
ORANGE = 'orange'

def check_turn_color():
    color = color_sensor.get_color()
    print(f"Обнаружен цвет: {color}")

    if color == BLUE:
        perform_left_turn()
        return "left"
    elif color == ORANGE:
        perform_right_turn()
        return "right"
    return "none"
