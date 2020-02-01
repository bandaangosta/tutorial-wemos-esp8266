import network
import ubinascii
from umqtt.simple import MQTTClient # See https://github.com/micropython/micropython-lib/tree/master/umqtt.simple
import machine
import time

# Pin definitions
relay = machine.Pin(5, machine.Pin.OUT) # relay shield uses pin D1 (GPIO5) for relay control

# Constants
MQTT_CLIENT_ID = ubinascii.hexlify(machine.unique_id())
MQTT_SERVER = "io.adafruit.com"
MQTT_PORT = 1883
MQTT_USER = "<your io.adafruit.com AIO user here>"
MQTT_PWD = "<your io.adafruit.com AIO password here>"
MQTT_FEED = b"<feed identifier to subscribe. Create it in io.adafruit.com>" # e.g., bandaangosta/feeds/relay_toggle that sends values ON or OFF
WIFI_SSID = '<your wifi network SSID here>'
WIFI_PWD = '<your wifi network password here>'


def wifi_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('Connecting to network...')
        sta_if.active(True)
        sta_if.connect(WIFI_SSID, WIFI_PWD)
        while not sta_if.isconnected():
            machine.idle()
    print('Network config:', sta_if.ifconfig())


def settimeout(duration):
   pass

# Received messages from subscriptions will be delivered to this callback
def sub_cb(topic, msg):
    print((topic, msg))

    if msg == b'ON':
        print('Turning LED on...')
        relay.on()
    else:
        print('Turning LED off...')
        relay.off()

def check_for_msg(client, blocking=False):
    if blocking:
        # Blocking wait for message
        client.wait_msg()
    else:
        # Non-blocking wait for message
        client.check_msg()

def main():
    wifi_connect()
    client = MQTTClient(
                MQTT_CLIENT_ID,
                MQTT_SERVER,
                user = MQTT_USER,
                password = MQTT_PWD,
                port = MQTT_PORT
             )

    client.settimeout = settimeout
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(MQTT_FEED)
    relay.off()

    while True:
        try:
            check_for_msg(client, True)
            # Add a sleep to avoid close to 100% CPU usage (in a more real
            # application other useful actions would be performed instead)
            time.sleep(0.1)
        except KeyboardInterrupt:
            print('Disconnecting...')
            client.disconnect()

main()