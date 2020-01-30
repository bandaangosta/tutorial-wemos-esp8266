import machine
import time

led = machine.Pin(2, machine.Pin.OUT) # set to 2 for builtin LED in Wemos D1 mini pro

def main():
    print('Starting LED blink...')
    i = 0
    while True:
        print(i)
        led.on()
        time.sleep(0.5)
        led.off()
        time.sleep(0.5)
        i = i + 1

# Run main loop
main()
