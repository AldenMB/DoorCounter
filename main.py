from machine import Pin, I2C, RTC
import time
import rp2
import ssd1306
import rtc_sync
from rotary_irq_rp2 import RotaryIRQ

rtc_sync.load()
clock = RTC()

samples_per_reading = 4
mask = int('0b'+'10'*samples_per_reading)

@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, autopush=True, fifo_join = rp2.PIO.JOIN_RX, push_thresh=samples_per_reading*2)
def ir_echo():
    # datasheet specifies relaxation time >= 5ms
    # total instructions: 3 + 4(2 + 32*8) = 1035
    # 1035 instructions / 76k instr/sec = 13.6 ms
    set(y, 4)  # 1
    label("blank")
    set(x, 31)  # 4 * 1
    label("blank_inner")
    jmp(x_dec, "blank_inner").delay(7)  # 4*32*8
    jmp(y_dec, "blank")  # 4 * 1

    # datasheet specifies at least 10 pulses per burst
    # NEC protocol uses 21 pulse and 237 pulse bursts
    set(x, 20)  # 1
    label("burst")
    nop().side(1)
    jmp(x_dec, "burst").side(0)
    # 32 pulses / 38khz = 842 us
    
    # response may terminate as early as 6 instructions after last pulse
    # we should take the measurement immediately
    in_(pins, 2) # 1

# asm_pio does not have an input pullup flag, for some reason. Oh well. Set them manually.
Pin(14, Pin.IN, Pin.PULL_UP)
Pin(15, Pin.IN, Pin.PULL_UP)
sensor = rp2.StateMachine(0, ir_echo, freq=2 * 38_000, sideset_base=Pin(13), in_base = Pin(14))
sensor.active(True)

i2c = I2C(id=0, sda=Pin(8), scl=Pin(9))
display = ssd1306.SSD1306_I2C(128, 64, i2c)
display.text('Hello, World!', 0, 0, 1)
display.show()

onboard_led = Pin(25, Pin.OUT)

rotary = RotaryIRQ(6, 7, pull_up=True)
button = Pin(3, Pin.IN, Pin.PULL_UP)

while True:
    display.fill(0)
        
    word = sensor.get()
    A = samples_per_reading- (bin(word & (mask>>1)).count('1'))
    B = samples_per_reading- (bin(word & mask).count('1'))
    
    display.text(f'{A:2d}', 0, 0, 1)
    display.rect(0, 10, 128*A//samples_per_reading, 4, 1)
    display.text(f'{B:2d}', 0, 20, 1)
    display.rect(0, 30, 128*B//samples_per_reading, 4, 1)
    
    display.text(f'{rotary.value()}', 0, 40, 1)
    
    year, month, day, weekday, hour, minute, second, *_ = clock.datetime()
    display.text(f'{year:4d}/{month:02d}/{day:02d}', 0, 48, 1)
    display.text(f'{hour:02d}:{minute:02d}:{second:02d}', 0, 56, 1)
    display.show()
    
    onboard_led.value(not button.value())
