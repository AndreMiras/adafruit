"""Turns leds on and change color based on the temperature."""
import random
import time

import adafruit_thermistor
import board
import digitalio
import neopixel


def get_random_color():
    red, green, blue = (
        random.randint(0, 255) for _ in range(3)
    )
    return red, green, blue


def color_1to255(color):
    return int(color * 255)


def color_255to1(color):
    return color / 255.0


def minmax(value, minimum=0, maximum=1):
    return max(min(value, maximum), minimum)


def temperature_percent_to_color255(temperature_percent):
    red = color_1to255(temperature_percent)
    green = 0
    blue = color_1to255(1 - temperature_percent)
    return (red, green, blue)


def main():
    LEDS_COUNT = 10
    pixels = neopixel.NeoPixel(
        board.NEOPIXEL, 10, brightness=0.1, auto_write=True)
    thermistor = adafruit_thermistor.Thermistor(
        board.TEMPERATURE, 10000, 10000, 25, 3950)
    button_a = digitalio.DigitalInOut(board.BUTTON_A)
    button_a.direction = digitalio.Direction.INPUT
    button_a.pull = digitalio.Pull.DOWN
    button_b = digitalio.DigitalInOut(board.BUTTON_B)
    button_b.direction = digitalio.Direction.INPUT
    button_b.pull = digitalio.Pull.DOWN
    temperature_min = thermistor.temperature
    temperature_delta_max = 4
    while True:
        temperature = thermistor.temperature
        temperature_percent = minmax(
            (temperature - temperature_min) / temperature_delta_max
        )
        print('temperature_percent: {}'.format(temperature_percent))
        rgb_color = temperature_percent_to_color255(temperature_percent)
        leds_on = int(temperature_percent * LEDS_COUNT)
        for led_index in range(LEDS_COUNT):
            if led_index <= leds_on:
                pixels[led_index] = rgb_color
            else:
                pixels[led_index] = (0, 0, 0)
        time.sleep(0.1)