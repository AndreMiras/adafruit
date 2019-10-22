"""
Simply shows some randoms colors.
Can adjust the brightness with buttons A or B.
"""
import random
import time

import board
import constants
import digitalio
import neopixel


def get_random_color():
    red, green, blue = (
        random.randint(0, 255) for _ in range(3)
    )
    return red, green, blue


def normalize_brightness(brightness):
    return max(min(brightness, 1), 0)


def more_brightness(brightness):
    return normalize_brightness(brightness + 0.1)


def less_brightness(brightness):
    return normalize_brightness(brightness - 0.1)


def main():
    button_a = digitalio.DigitalInOut(board.BUTTON_A)
    button_a.direction = digitalio.Direction.INPUT
    button_a.pull = digitalio.Pull.DOWN
    button_b = digitalio.DigitalInOut(board.BUTTON_B)
    button_b.direction = digitalio.Direction.INPUT
    button_b.pull = digitalio.Pull.DOWN
    brightness = 0.1
    pixels = neopixel.NeoPixel(
        board.NEOPIXEL, 10, brightness=brightness, auto_write=True)
    loop = 0
    while True:
        loop += 1
        print('brightness: {}'.format(brightness))
        if button_a.value:
            brightness = less_brightness(brightness)
            pixels.brightness = brightness
        if button_b.value:
            brightness = more_brightness(brightness)
            pixels.brightness = brightness
        if loop % 10 == 0:
            for led_index in range(constants.LEDS_COUNT):
                color = get_random_color()
                pixels[led_index] = color
        time.sleep(0.1)
