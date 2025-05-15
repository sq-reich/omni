import smbus2 as smbus
import time
import random as rnd
class LCD:
    I2C_ADDR = 0x27
    LCD_WIDTH = 16  # 16 characters per line

    LCD_CHR = 1  # Character mode
    LCD_CMD = 0  # Command mode

    LCD_LINE_1 = 0x80  # First line
    LCD_LINE_2 = 0xC0  # Second line

    ENABLE = 0b00000100  # Enable bit
    BACKLIGHT = 0x08     # Backlight ON

    def __init__(self, bus_number=1):
        self.bus = smbus.SMBus(bus_number)
        self.init_display()

        self.heyMsg = ["Hallo", "Moin", "Willkommen", "Viel Spass!", "Guten Tag"]
        self.beyMsg = ["Tschüss", "Adios", "Auf Wiedersehen", "Schoenen Tag noch"]


    def init_display(self):
        """Initialize the LCD display."""
        time.sleep(0.5)
        self.send_byte(0x33, self.LCD_CMD)
        self.send_byte(0x32, self.LCD_CMD)
        self.send_byte(0x28, self.LCD_CMD)
        self.send_byte(0x0C, self.LCD_CMD)
        self.send_byte(0x06, self.LCD_CMD)
        self.clear()

    def send_byte(self, bits, mode):
        """Send a byte to the LCD."""
        try:
            high = mode | (bits & 0xF0) | self.BACKLIGHT | self.ENABLE
            low = mode | ((bits << 4) & 0xF0) | self.BACKLIGHT | self.ENABLE
            self.bus.write_byte(self.I2C_ADDR, high)
            self.bus.write_byte(self.I2C_ADDR, high & ~self.ENABLE)
            self.bus.write_byte(self.I2C_ADDR, low)
            self.bus.write_byte(self.I2C_ADDR, low & ~self.ENABLE)
        except Exception as e:
            print(f"I2C error: {e}")

    def send_string(self, message, line, center=False):
        """Send a string to a specific line."""
        if center:
            message = message.center(self.LCD_WIDTH)
        else:
            message = message.ljust(self.LCD_WIDTH, ' ')

        self.send_byte(line, self.LCD_CMD)
        for char in message:
            self.send_byte(ord(char), self.LCD_CHR)

    def display_text(self, text, center=False):
        """Display text across one or two lines."""
        text = str(text)

        if len(text) <= self.LCD_WIDTH:
            self.send_string(text, self.LCD_LINE_1, center)
        else:
            first_line = text[:self.LCD_WIDTH]
            second_line = text[self.LCD_WIDTH:self.LCD_WIDTH*2]

            self.send_string(first_line, self.LCD_LINE_1, center)
            self.send_string(second_line, self.LCD_LINE_2, center)

    def display_two_lines(self, text_line1, text_line2, center=False):
        """Display two separate lines."""
        self.send_string(str(text_line1)[:self.LCD_WIDTH], self.LCD_LINE_1, center)
        self.send_string(str(text_line2)[:self.LCD_WIDTH], self.LCD_LINE_2, center)
    
    def scroll_text(self, text, line=1, delay=0.3, repeat=1):
        """Scroll a long text on the display."""
        text = str(text)
        text += " " * self.LCD_WIDTH  # Abstand zum Wiederanfang
        display_line = self.LCD_LINE_1 if line == 1 else self.LCD_LINE_2

        for _ in range(repeat):
            for i in range(len(text) - self.LCD_WIDTH + 1):
                part = text[i:i + self.LCD_WIDTH]
                self.send_string(part, display_line)
                time.sleep(delay)

    def clear(self):
        """Clear the LCD display."""
        self.send_byte(0x01, self.LCD_CMD)
        time.sleep(0.2)
        