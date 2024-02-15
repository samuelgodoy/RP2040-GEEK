import storage
import time
import busio
import digitalio
import board
from adafruit_rgb_display import color565
from adafruit_bitmap_font import bitmap_font
from adafruit_rgb_display.st7789 import ST7789
import adafruit_sdcard
import os

# SPI do sd
spi = busio.SPI(clock=board.GP18, MOSI=board.GP19, MISO=board.GP20)
class SDCard:
    def __init__(self, spi_bus, cs_pin):
        self.cs = digitalio.DigitalInOut(cs_pin)
        self.cs.direction = digitalio.Direction.OUTPUT
        self.sdcard = adafruit_sdcard.SDCard(spi_bus, self.cs)
        self.vfs = storage.VfsFat(self.sdcard)

    def mount(self, mount_point):
        storage.mount(self.vfs, mount_point)
        print("SD card mounted at", mount_point)

    def listdir(self, path="/"):
        return os.listdir(path)
    
    def read_file(self, filepath):
        """Lê o conteúdo de um arquivo e retorna como string."""
        with open(filepath, 'r') as file:
            return file.read()
    
# Aguarde até que o SPI esteja pronto
while not spi.try_lock():
    pass
spi.configure(baudrate=1320000)
spi.unlock()




class LCDController:
    def __init__(self, font_path=os.getenv("font_file")):
        # Constantes para configuração do display
        self.font = bitmap_font.load_font(font_path)
        self.DISPLAY_WIDTH = 135
        self.DISPLAY_HEIGHT = 240

        # Configuração dos pinos SPI e display
        spi = busio.SPI(clock=board.GP10, MOSI=board.GP11)
        self.display = ST7789(
            spi,
            width=self.DISPLAY_WIDTH,
            height=self.DISPLAY_HEIGHT,
            x_offset=53,
            y_offset=40,
            baudrate=10_000_000,
            cs=digitalio.DigitalInOut(board.GP9),
            dc=digitalio.DigitalInOut(board.GP8),
            rst=digitalio.DigitalInOut(board.GP12)
        )
        self.display.fill(0)

    def draw_string(self, x, y, string, color):
        current_x = x
        for char in string:
            glyph = self.font.get_glyph(ord(char))
            if glyph:
                bitmap = glyph.bitmap
                width, height = glyph.width, glyph.height
                for j in range(height):
                    for i in range(width):
                        if bitmap[i, j] > 0:
                            self.display.pixel(current_x + i, y + j, color)
                current_x += glyph.shift_x  # Usa a propriedade de deslocamento horizontal do glifo

# Uso da classe
class EnhancedLCDController:
    def __init__(self, lcd):
        self.lcd = lcd
        self.current_y = 0
        self.start_x = 1  # Posição X padrão para texto
        self.eixox = 30  # Posição X específica para arte personalizada
        self.line_height = 15
        self.color = color565(0, 255, 0)  # Define a cor uma única vez

    def draw_strings(self, strings, x=None):
        if x is None:
            x = self.start_x
        for string in strings:
            self.lcd.draw_string(x, self.current_y, string, self.color)
            self.current_y += self.line_height

    def list_py_files_and_exec(self, sd):
        try:
            sd.mount("/sd")
            files = sd.listdir("/sd/")
            for file in files:
                if file.endswith('.py'):
                    self.draw_strings([file, f"$ python {file}"])
                    try:
                        with open(f"/sd/{file}", 'r') as f:
                            file_content = f.read()
                            exec(file_content)
                    except Exception as e:
                        print(f"Error executing {file}: {e}")
                        break
        except Exception as e:
            print(f"Erro ao abrir SD: {e}")

    def display_terminal_sequence(self):
        terminal_sequence = [
            "ob@scorpion:~# /bin/sh", "$ ls", "$ exit ", "ob@scorpion:~#", "ob@scorpion:~# logout", "scorpion login: "
        ]
        self.draw_strings(terminal_sequence)

    def display_custom_art(self):
        art = [
            " .==.", 
            ":    '  _", 
            ' "==___( `', 
            '   <<<< \_,'
        ]
        self.draw_strings(art, self.eixox)  # Usa o eixox para a arte personalizada

# Uso da classe EnhancedLCDController
lcd = LCDController()
enhanced_lcd = EnhancedLCDController(lcd)

# Desenha strings iniciais
enhanced_lcd.draw_strings([
    "scorpion login: ob", "Password: ", "ob@scorpion:~#"
])

# Cria uma instância da classe SDCard e monta o sistema de arquivos
try:
    sd = SDCard(spi, board.GP23)
    enhanced_lcd.list_py_files_and_exec(sd)
finally:
    enhanced_lcd.display_terminal_sequence()
    enhanced_lcd.display_custom_art()





time.sleep(5000)