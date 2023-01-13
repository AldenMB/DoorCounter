from machine import Pin
import time
import rp2

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

Pin(14, Pin.IN, Pin.PULL_UP)
Pin(15, Pin.IN, Pin.PULL_UP)
sensor = rp2.StateMachine(0, ir_echo, freq=2 * 38_000, sideset_base=Pin(8), in_base = Pin(14))
sensor.active(True)

onboard_led = Pin(25, Pin.OUT)
while True:
    word = sensor.get()
    A = samples_per_reading- (bin(word & (mask>>1)).count('1'))
    B = samples_per_reading- (bin(word & mask).count('1'))
    print(f'{A}\t{B}')
