"""Select a program to run via buttons A or B and run it by pressing both."""
import random
import time

import board
import digitalio
import neopixel
import random_colors
import temperature

# TODO: should be available somewhere in the board
LEDS_COUNT = 10


def minmax(value, minimum=0, maximum=1):
    return max(min(value, maximum), minimum)


def get_random_color():
    red, green, blue = (
        random.randint(0, 255) for _ in range(3)
    )
    return red, green, blue


def show_selection(pixels, selection):
    print('selection: {}'.format(selection))
    rgb_color = get_random_color()
    for led_index in range(LEDS_COUNT):
        pixels[led_index] = (0, 0, 0)
    pixels[selection] = rgb_color


def get_selection(button_a, button_b):
    if button_a.value and button_b.value:
        return 0
    elif button_a.value:
        return 1
    elif button_b.value:
        return -1
    return 0


def selection_applied(button_a, button_b):
    return button_a.value and button_b.value


def timed_out(now, start_time, timeout_secounds=5):
    return now < start_time + timeout_secounds


def deinit(*digitalio_list):
    for button in digitalio_list:
        button.deinit()


def start_program(selection):
    modules = (
        temperature,
        random_colors,
    )
    try:
        module = modules[selection]
    except IndexError:
        print('No such program.')
        return
    print('Start program: {}.'.format(module))
    module.main()


def main():
    MAX_PROGRAM = LEDS_COUNT
    pixels = neopixel.NeoPixel(
        board.NEOPIXEL, 10, brightness=0.1, auto_write=True)
    button_a = digitalio.DigitalInOut(board.BUTTON_A)
    button_a.direction = digitalio.Direction.INPUT
    button_a.pull = digitalio.Pull.DOWN
    button_b = digitalio.DigitalInOut(board.BUTTON_B)
    button_b.direction = digitalio.Direction.INPUT
    button_b.pull = digitalio.Pull.DOWN
    start_time = time.monotonic()
    selection = 0
    show_selection(pixels, selection)
    while not (
            timed_out(time.monotonic(), start_time) or
            selection_applied(button_a, button_b)):
        previous_selection = selection
        selection += get_selection(button_a, button_b)
        selection = minmax(selection, 0, MAX_PROGRAM - 1)
        if selection != previous_selection:
            show_selection(pixels, selection)
            start_time = time.monotonic()
        time.sleep(0.1)
    deinit(button_a, button_b, pixels)
    start_program(selection)


main()
