import machine, sdcard, os
from machine import Pin, SPI

spi = SPI(0, 10_000_000, sck=Pin(2), mosi=Pin(3), miso=Pin(0)) #sck=10, mosi=11 miso=8
cs = Pin(1)
detect = Pin(4, Pin.IN, Pin.PULL_UP)

try:
    sd = sdcard.SDCard(spi, cs)
    os.mount(sd, '/sd')
except OSError as e:
    print(e)

print(os.listdir('/'))
print(detect.value())