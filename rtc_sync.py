from machine import Pin, RTC
import ds1302

external = ds1302.DS1302(clk = Pin(12), dio = Pin(10), cs = Pin(11))
internal = RTC()

def show():
    print(f'''\
external clock: {external.date_time()}
internal clock: {internal.datetime()}''')
    
def save():
    print('Synchronizing clocks...', end = '')
    external.date_time(internal.datetime())
    print(' ...done!')

def load():
    internal.datetime(external.date_time()+[0])

if __name__ == '__main__':
    show()
    save()
    show()