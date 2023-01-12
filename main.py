from machine import Pin
from ir_rx.nec import NEC_8
from ir_tx.nec import NEC
import time

tic = time.ticks_ms()

def make_callback(label):
    def callback(data, addr, ctrl):
        toc = time.ticks_ms() - tic
        if data < 0:  # NEC protocol sends repeat codes.
            print(f'{label} {toc} Repeat code.')
        else:
            print(f'{label} {toc} Data {data:02x} Addr {addr:04x}')
    return callback
    
        
sensor = [NEC_8(Pin(x, Pin.IN), make_callback(x)) for x in [15, 14]]

transmitter = NEC(Pin(8, Pin.OUT, value=0))

while True:
    time.sleep(0.2)
    print()
    tic = time.ticks_ms()
    transmitter.transmit(0x27, 0x18)
    print(time.ticks_ms() - tic)
    