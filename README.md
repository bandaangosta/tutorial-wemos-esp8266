# Wemos D1 mini development board tutorial
*Notes for IoT sessions by JLO in ALMA - Summer 2020*

[![](http://img.youtube.com/vi/wWWjBbW_QvQ/0.jpg)](http://www.youtube.com/watch?v=wWWjBbW_QvQ "Remote relay activation")

We'll be using the Wemos D1 mini, a [cheap](https://www.aliexpress.com/item/32831353752.html?spm=a2g0s.9042311.0.0.77ba4c4dUDc5of) wifi-enabled board with 4MB flash based on the awesome [ESP-8266EX microcontroller](https://www.espressif.com/en/products/hardware/esp8266ex/overview).
![D1 mini](https://github.com/bandaangosta/tutorial-wemos-esp8266/blob/master/images/products:d1:d1_mini_v3.1.0_1_16x9.jpg)

## Materials
 * [Wemos D1 mini development board](https://www.aliexpress.com/item/32831353752.html?spm=a2g0s.9042311.0.0.77ba4c4dUDc5of)
 * Computer
 * USB-to-microUSB cable
 * Jumpers
 * 5V relay, for later exercise
 
## Features

* 11 digital input/output pins
* All pins have interrupt/pwm/I2C/one-wire supported(except D0)
* 1 analog input(3.2V max input)
* Operating Voltage 3.3V
* Clock Speed   80MHz (max.160MHz)
* Flash 4 MB
* 1 Micro USB connection
* Compatible with MicroPython, Arduino, nodemcu, etc.

Find full details list [here](https://wiki.wemos.cc/products:d1:d1_mini).

## SDK
From the many available alternatives, we will be using the [MycroPython SDK](https://micropython.org/) for our projects.

## Setup
### Getting latest firmware

Get latest MicroPython firmware for ESP8266 boards from [http://micropython.org/download#esp8266](http://micropython.org/download#esp8266)

### Installing esptool bootloader utility
Install ESP8266 serial bootloader utility [esptool](https://github.com/espressif/esptool). You will need either Python 2.7 or Python 3.4 or newer installed on your system.

Typically, it should be as simple as running in a terminal:

    $ pip install esptool

### Erasing/flashing the firmware

Connect your Wemos board to a USB port of your computer. We will assume it appears as device /dev/ttyUSB0.
Make sure to used a fully wired USB cable. If board is not visible in your devices list, it may be possible you are using a power-only USB cable (for charging).

#### Erase flash

    $ esptool.py --port /dev/ttyUSB0 erase_flash

#### Flash the firmware

    $ esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_mode=dout --flash_size=detect 0 esp8266-20191220-v1.12.bin

### Basic testing

The MicroPython firmware comes with the handy REPL (Read Evaluate Print Loop) tool. The "Python prompt", if you will. By far the easiest way to test commands and explore the many possibilities of the microcontroller.
We will need a simple serial port terminal. In these examples, we will use `picocom`.

    $ picocom -b 115200 /dev/ttyUSB0

(Remember: ctrl + a, x to exit)

You should be seeing the REPL prompt. Try any simple operation:

    >>> 2 + 3
    5

Get current firmware:

    >>> import sys
    >>> sys.platform
    'esp8266'
    >>> sys.implementation.name
    'micropython'
    >>> sys.implementation.version
    (1, 12, 0)

Powering on/off the built-in LED (internally connected to pin GPIO2):

    >>> import machine
    >>> led = machine.Pin(2, machine.Pin.OUT) # set to 2 for builtin LED in Wemos D1 mini pro
    >>> led.on()
    >>> led.off()
    >>> led.on()
    >>> led.off()


It works!

### Loading application files

Source Python files can be loaded using the `ampy` tool, which can be installed like so:

    $ pip install adafruit-ampy
    
On board boot, file `boot.py` is run first. This file is automatically created during first-time module set up and contains some initialization routines. Generally, it does not need to be modified. After boot.py is completed, file main.py is run, if found. This is where we can put our code.
 
Listing files on board filesystem:    
    
    $  ampy --port /dev/ttyUSB0 ls

Show contents of existing file main.py:  
    
    $  ampy --port /dev/ttyUSB0 get main.py

Upload main.py to board:
    
    $  ampy --port /dev/ttyUSB0 put main.py

Upload myapp.py to board, renaming it to main.py:
    
    $  ampy --port /dev/ttyUSB0 put myapp.py main.py
    
## Experiments
### LED blinking
Turn on and off board built-in LED in a 1 second cycle:
[led_toggle.py](https://github.com/bandaangosta/tutorial-wemos-esp8266/blob/master/examples/led_toggle.py)

### Relay toggle
For relay experiments we will be using the [Wemos D1 mini relay shield](https://www.aliexpress.com/item/32863745140.html?spm=a2g0s.9042311.0.0.77ba4c4dUDc5of):
![D1 mini](https://github.com/bandaangosta/tutorial-wemos-esp8266/blob/master/images/relay1.jpg)

The relay board uses pin D1 (GPIO 5) for relay control. Therefore, we need to connect D1, 5V and GND lines from Wemos D1 Mini board to relay board.
The following example is very similar to the LED toggle test above, but now controlling the D1 pin: [relay_toggle.py](https://github.com/bandaangosta/tutorial-wemos-esp8266/blob/master/examples/relay_toggle.py)

### Remote relay activation
There are several ways to establish a remote connection to a "home" device. By remote connection here we mean reading variables (e.g., sensor values) and/or controlling actuators (e.g., a relay switching to a lamp or water valve) from a remote device in a different part of the world, through the Internet. Neat stuff.   

The following example accomplishes this purpose using the popular [Message Queue Telemetry Transport ](http://mqtt.org/)(MQTT) protocol. In the center of the MQTT communications there is a broker machine, a server that passes messages between data publishers and subscribers of "topics".   

We could setup our own broker service on a cloud server or a home machine connected to the internet, but we'll take a shortcut for now and use the fantastic service provided by [adafruit](https://io.adafruit.com) for us gadget lovers. Once you get an account, create a new feed or topic called `relay_toggle`. Then, create a new dashboard with a block of type `toggle`. Associate that block or "button" to the `relay_toggle` feed. Take notes of your AIO key.

You should end up with a dashboard like the this:
![D1 mini](https://github.com/bandaangosta/tutorial-wemos-esp8266/blob/master/images/dashboard_toggle.jpg)

Now load the following code on your board and profit: [relay_toggle_mqtt.py](https://github.com/bandaangosta/tutorial-wemos-esp8266/blob/master/examples/relay_toggle_mqtt.py)

Result:
[![](http://img.youtube.com/vi/wWWjBbW_QvQ/0.jpg)](http://www.youtube.com/watch?v=wWWjBbW_QvQ "Remote relay activation")


