import machine, sdcard, os
from machine import Pin, SPI

spi = SPI(1, 10_000_000) #sck=10, mosi=11 miso=8
cs = Pin(9)

try:
    sd = sdcard.SDCard(spi, cs)
    os.mount(sd, '/sd')
except OSError as e:
    print(e)

print(os.listdir('/'))