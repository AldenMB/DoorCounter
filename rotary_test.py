from rotary_irq_rp2 import RotaryIRQ
from machine import Pin
import time

rotary = RotaryIRQ(6, 7, pull_up=True)
button = Pin(3, Pin.IN, Pin.PULL_UP)

while True:
    print(button.value(), rotary.value())
    time.sleep(0.2)