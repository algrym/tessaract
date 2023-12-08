#!/usr/bin/env python3
""" code.py -- github.com/algrym/tesseract """
import atexit
import time

import adafruit_fancyled.adafruit_fancyled as fancyled
import board
import neopixel
import supervisor
from rainbowio import colorwheel

import version

# Global constants
NEOPIXEL_COUNT: int = 10
NEOPIXEL_BRIGHTNESS: float = 0.03
NEOPIXEL_PIN: Pin = board.NEOPIXEL

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
    print("[tesseract] - github.com/algrym/tesseract/code.py version", version.__version__)
    print(f" - Adafruit FancyLed v{fancyled.__version__}")


def main_event_loop():
    """For CircuitPython optimization, this is just the primary loop
    of the script tucked into one big fat function.
    We also pull some global vars in, so now they're function-local.

    It turns out that fetching global vars is expensive."""

    # balance the colors better so white doesn't appear blue-tinged
    BRIGHTNESS_LEVELS = (0.25, 0.3, 0.15)

    # define colors that will be used inside the loop
    BLUE = fancyled.gamma_adjust(fancyled.CRGB(0, 0, 255), brightness=BRIGHTNESS_LEVELS).pack()
    WHITE = fancyled.gamma_adjust(fancyled.CRGB(255, 255, 255), brightness=BRIGHTNESS_LEVELS).pack()

    while True:
        for i in range(255):
            pixels.fill(colorwheel(i))
            time.sleep(0.05)


if __name__ == "__main__":
    main_event_loop()
