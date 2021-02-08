#
# HD44780 LCD Script for
# Raspberry Pico


# The wiring for the LCD is as follows:
# 1 : GND
# 2 : 5V
# 3 : Contrast (0-5V)*
# 4 : RS (Register Select)
# 5 : R/W (Read Write)       - GROUND THIS PIN
# 6 : Enable or Strobe
# 7 : Data Bit 0             - NOT USED
# 8 : Data Bit 1             - NOT USED
# 9 : Data Bit 2             - NOT USED
# 10: Data Bit 3             - NOT USED
# 11: Data Bit 4
# 12: Data Bit 5
# 13: Data Bit 6
# 14: Data Bit 7
# 15: LCD Backlight +5V**
# 16: LCD Backlight GND

from machine import *
import utime


class LCD(object):
    
    # Define PIO to LCD mapping

    LCD_RS = 16
    LCD_E = 17
    LCD_D4 = 22
    LCD_D5 = 19
    LCD_D6 = 20
    LCD_D7 = 21
    # LED_ON = 15

    # Define some device constants

    LCD_WIDTH = 0x10  # Maximum characters per line
    LCD_CHR = True
    LCD_CMD = False

    LCD_LINE_1 = 0x80  # LCD RAM address for the 1st line
    LCD_LINE_2 = 0xC0  # LCD RAM address for the 2nd line
    LCD_LINE_3 = 0x94  # LCD RAM address for the 3rd line
    LCD_LINE_4 = 0xD4  # LCD RAM address for the 4th line 
    # Timing constants

    E_PULSE = 0.001
    E_DELAY = 0.001


    def __init__(self):
        self.lcd_init()

    def lcd_init(self):
        # GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbers
        self.lcd_e = Pin(LCD.LCD_E, Pin.OUT)     # GPIO.setup(LCD_E, GPIO.OUT)  # E
        self.lcd_rs = Pin(LCD.LCD_RS, Pin.OUT)   # GPIO.setup(LCD_RS, GPIO.OUT)  # RS
        self.lcd_d4 = Pin(LCD.LCD_D4, Pin.OUT)   # GPIO.setup(LCD_D4, GPIO.OUT)  # DB4
        self.lcd_d5 = Pin(LCD.LCD_D5, Pin.OUT)   # GPIO.setup(LCD_D5, GPIO.OUT)  # DB5
        self.lcd_d6 = Pin(LCD.LCD_D6, Pin.OUT)   # GPIO.setup(LCD_D6, GPIO.OUT)  # DB6
        self.lcd_d7 = Pin(LCD.LCD_D7, Pin.OUT)   # GPIO.setup(LCD_D7, GPIO.OUT)  # DB7

        # Initialise display
        self.lcd_byte(0x33, self.LCD_CMD)
        self.lcd_byte(0x32, self.LCD_CMD)
        self.lcd_byte(0x28, self.LCD_CMD)
        self.lcd_byte(0x0C, self.LCD_CMD)
        self.lcd_byte(0x06, self.LCD_CMD)
        self.lcd_byte(0x01, self.LCD_CMD)

    def message(self, message, style=1,speed=1):
        # Auto splits, not perfect for clock
        # Send string to display
        # style=1 Left justified
        # style=2 Centred
        # style=3 Right justified
        # style=4 typing

        msgs = message.split('\n')
        for (idx, msg) in enumerate(msgs):
            if idx == 0:
                self.lcd_byte(self.LCD_LINE_1, self.LCD_CMD)
            elif idx == 0x01:
                self.lcd_byte(self.LCD_LINE_2, self.LCD_CMD)
            if style != 4:
                self.lcd_string(msg, style)
            elif style == 4:
                self.type_string(msg, speed)


    def type_string(self, message, speed=1, style=1):

        # Send string to display
        # style=1 Left justified
        # style=2 Centred
        # style=3 Right justified

        if style == 0x01:
            message = "{0:<{w}}".format( message, w=self.LCD_WIDTH )
        elif style == 0x02:
            message = "{0:^{w}}".format( message, w=self.LCD_WIDTH )
        elif style == 3:
            message = "{0:>{w}}".format( message, w=self.LCD_WIDTH )

        for i in range(self.LCD_WIDTH):
            self.lcd_byte(ord(message[i]), self.LCD_CHR)
            if message[i] != " ":
                utime.sleep(speed)

    def clear(self):
        self.lcd_byte(0x06, self.LCD_CMD)
        self.lcd_byte(0x01, self.LCD_CMD)
        utime.sleep(0.45)

    def write_line1(self, message, style):
        self.lcd_byte(self.LCD_LINE_1, self.LCD_CMD)
        self.lcd_string(message, style)

    def write_line2(self, message, style):
        self.lcd_byte(self.LCD_LINE_2, self.LCD_CMD)
        self.lcd_string(message, style)

    def set_line1(self):
        self.lcd_byte(self.LCD_LINE_1, self.LCD_CMD)

    def set_line2(self):
        self.lcd_byte(self.LCD_LINE_2, self.LCD_CMD)

    def lcd_string(self, message, style):
        # Send string to display
        # style=1 Left justified
        # style=2 Centred
        # style=3 Right justified

        if style == 0x01:
            message = "{0:<{w}}".format( message, w=self.LCD_WIDTH )
        elif style == 0x02:
            message = "{0:^{w}}".format( message, w=self.LCD_WIDTH )
        elif style == 3:
            message = "{0:>{w}}".format( message, w=self.LCD_WIDTH )

        for i in range(self.LCD_WIDTH):
            self.lcd_byte(ord(message[i]), self.LCD_CHR)

    def lcd_byte(self, bits, mode):

        # Send byte to data pins
        # bits = data
        # mode = True  for character
        #        False for command

        self.lcd_rs.value( mode ) 

        # High bits

        self.lcd_d4.value( False )       
        self.lcd_d5.value( False )      
        self.lcd_d6.value( False )       
        self.lcd_d7.value( False )       
        if bits & 0x10 == 0x10:
            self.lcd_d4.value( True )    
        if bits & 0x20 == 0x20:
            self.lcd_d5.value( True )    
        if bits & 0x40 == 0x40:
            self.lcd_d6.value( True )    
        if bits & 0x80 == 0x80:
            self.lcd_d7.value( True )    

        # Toggle 'Enable' pin

        utime.sleep(self.E_DELAY)
        self.lcd_e.value( True )         
        utime.sleep(self.E_PULSE)
        self.lcd_e.value( False )        
        utime.sleep(self.E_DELAY)

        # Low bits

        self.lcd_d4.value( False )       
        self.lcd_d5.value( False )       
        self.lcd_d6.value( False )       
        self.lcd_d7.value( False )       
        if bits & 0x01 == 0x01:
            self.lcd_d4.value( True )    
        if bits & 0x02 == 0x02:
            self.lcd_d5.value( True )    
        if bits & 0x04 == 0x04:
            self.lcd_d6.value( True )    
        if bits & 0x08 == 0x08:
            self.lcd_d7.value( True ) 

        # Toggle 'Enable' pin

        utime.sleep(self.E_DELAY)
        self.lcd_e.value( True )         
        utime.sleep(self.E_PULSE)
        self.lcd_e.value( False )   
        utime.sleep(self.E_DELAY)
        

if __name__ == '__main__':
    lcd = LCD()
    lcd.clear()
    lcd.message('It\nworks...!', 1)
    utime.sleep(1)
    lcd.clear()
