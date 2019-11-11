"""Turns leds on and change color based on the temperature."""
import time

import adafruit_thermistor
import board
import constants
import digitalio
import neopixel
import utils


def color_1to255(color):
    return int(color * 255)


def temperature_percent_to_color255(temperature_percent):
    red = color_1to255(temperature_percent)
    green = 0
    blue = color_1to255(1 - temperature_percent)
    return (red, green, blue)


def main():
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
        temperature_percent = utils.minmax(
            (temperature - temperature_min) / temperature_delta_max
        )
        print('temperature_percent: {}'.format(temperature_percent))
        rgb_color = temperature_percent_to_color255(temperature_percent)
        leds_on = int(temperature_percent * constants.LEDS_COUNT)
        for led_index in range(constants.LEDS_COUNT):
            if led_index <= leds_on:
                pixels[led_index] = rgb_color
            else:
                pixels[led_index] = (0, 0, 0)
        time.sleep(0.1)
