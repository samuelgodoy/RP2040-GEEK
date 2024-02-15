import time
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

# Inicializa o teclado
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)

# Aguarda um momento para o sistema configurar o dispositivo
time.sleep(1)

# Escreve "Hello, World!" seguido de uma quebra de linha
keyboard_layout.write("Hello, World!\n")

