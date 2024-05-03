# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple test for NeoPixels on Raspberry Pi
import time
import neopixel
import board
import digitalio


# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 32

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.3, auto_write=False, pixel_order=ORDER
)


# Set up motion detection
# using input GPIO5 = pi pin 29

pir = digitalio.DigitalInOut(board.D5)
pir.direction = digitalio.Direction.INPUT

#   Yellow shades
#   255,255,[0-51-102-153-204]

while True:
    pir_value = pir.value
    if pir_value:
        #PIR detecting motion
        #repeat the blinking loop x times
        for x in range(0,4):

            pixels.fill((255, 255, 0))
            pixels.show()
            time.sleep(0.1)

            pixels.fill((80, 80, 0))
            pixels.show()
            time.sleep(0.1)

            pixels.fill((200, 200, 0))
            pixels.show()
            time.sleep(0.1)

            pixels.fill((20, 20, 0))
            pixels.show()
            time.sleep(0.1)

    else:
        #PIR not detecting motion
        pixels.fill((0, 0, 0))
        pixels.show()
        time.sleep(0.5)
