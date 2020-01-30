import machine
import time

relay = machine.Pin(5, machine.Pin.OUT) # relay shield uses pin D1 (GPIO5) for relay control

def main():
    print('Starting relay control ...')
    i = 0
    while True:
        print(i)
        relay.on()
        time.sleep(3)
        relay.off()
        time.sleep(3)
        i = i + 1

# Run main loop
main()
