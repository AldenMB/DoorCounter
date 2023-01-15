from machine import Pin, I2C
import ssd1306

i2c = I2C(id=0, sda=Pin(20), scl=Pin(21))
display = ssd1306.SSD1306_I2C(128, 64, i2c)

display.text('Hello, World!', 0, 0, 1)
display.show()
