#!/usr/bin/env python3
""" code.py -- github.com/algrym/tesseract """
import atexit
import math
import random
import sys
import time

import adafruit_lis3dh
import board
import busio
import digitalio
import neopixel
import supervisor
from rainbowio import colorwheel

import version

# Global constants
NEOPIXEL_COUNT: int = 10
NEOPIXEL_BRIGHTNESS: float = 0.1
NEOPIXEL_PIN: Pin = board.NEOPIXEL
ACCELEROMETER_ADDRESS: int = 0x19

# No config beyond this point

# Set up the neopixels on the board
pixels = neopixel.NeoPixel(board.NEOPIXEL,
                           NEOPIXEL_COUNT,
                           brightness=NEOPIXEL_BRIGHTNESS,
                           auto_write=True)


def all_off():
    """callback to turn everything off on exit"""
    if supervisor.runtime.serial_connected:
        print(' - Watchdog: standing down.')
    if supervisor.runtime.serial_connected:
        print(' - Exiting: setting all pixels off.')
    pixels.fill(0)
    supervisor.reload()


# turn everything off on exit
atexit.register(all_off)

# Display program header
if supervisor.runtime.serial_connected:
    print("[tesseract] - github.com/algrym/tesseract/code.py\n - version", version.__version__)
    print(f" - Adafruit lis3dh v{adafruit_lis3dh.__version__}")

# initialize the onboard LED
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT


def main_event_loop():
    """For CircuitPython optimization, this is just the primary loop
    of the script tucked into one big fat function.
    We also pull some global vars in, so now they're function-local.

    It turns out that fetching global vars is expensive."""

    # Setup the accelerometer
    # https://learn.adafruit.com/adafruit-lis3dh-triple-axis-accelerometer-breakout/python-circuitpython
    accel_lis3dh = adafruit_lis3dh.LIS3DH_I2C(
        busio.I2C(board.ACCELEROMETER_SCL, board.ACCELEROMETER_SDA),
        int1=digitalio.DigitalInOut(board.ACCELEROMETER_INTERRUPT),
        address=ACCELEROMETER_ADDRESS)
    accel_lis3dh.range = adafruit_lis3dh.RANGE_2_G
    accel_lis3dh.set_tap(1, 90)

    # How many iterations?
    count: int = 0;

    # event loop
    while True:
        # blue pixels should pulse over time
        pixels.fill((0, 0, (35 + (20 * math.sin(count / 1.5)))))

        # flash a pixel when accelerometer says so
        if accel_lis3dh.shake(shake_threshold=10) or accel_lis3dh.tapped:
            pixels[random.randint(0, NEOPIXEL_COUNT - 1)] = colorwheel(random.uniform(0, 255))

        # flash the onboard LED
        led.value = not led.value

        # sleep long enough for interrupts, but short enough for reactivity
        time.sleep(0.1)

        # increment the counter
        count += 1
        if count >= sys.maxsize:
            count = 0


if __name__ == "__main__":
    main_event_loop()
