from machine import Pin
import time
import rp2


@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW)
def drone():
    # datasheet specifies relaxation time >= 5ms
    # total instructions: 2 + 4(2 + 32*8) = 1034
    # 1034 instructions / 76k instr/sec = 13.6 ms
    set(y, 4)  # 1
    label("blank")
    set(x, 31)  # 4 * 1
    label("blank_inner")
    jmp(x_dec, "blank_inner").delay(7)  # 4*32*8
    jmp(y_dec, "blank")  # 4 * 1

    # datasheet specifies at least 10 pulses per burst
    # NEC protocol uses 21 pulse and 237 pulse bursts
    set(x, 31)  # 1
    label("burst")
    nop().side(1)
    jmp(x_dec, "burst").side(0)
    # 32 pulses / 38khz = 842 us


beacon = rp2.StateMachine(0, drone, freq=2 * 38_000, sideset_base=Pin(8))
beacon.active(True)

sense = Pin(15, Pin.IN)
onboard_led = Pin(25, Pin.OUT)
while True:
    onboard_led.value(not sense.value())
