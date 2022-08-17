#!/usr/bin/python3

import gpiozero
import time
import itertools
import random


FPS = 25
DELAY = 1 / FPS
TIMESCALE = 10
MIN_BRIGHTNESS = 0.1
MAX_BRIGHTNESS = 1.0
REPEATS = 3

led = gpiozero.PWMLED(12)

lightcurves = {
    'pulsator': (
        (0, 0),
        (0.4, 1),
        (1.0, 0),
        (0.2, 0),
    ),
    'eclipsing': (
        (0, 1),
        (0.4, 1),
        (0.05, 0.5),
        (0.3, 0.5),
        (0.05, 1),
        (0.4, 1),
        (0.05, 0.1),
        (0.3, 0.1),
        (0.05, 1),
    ),
    'lensing': (
        (0, 0),
        (0.6, 0.9),
        (0.7, 0),
        (0.2, 0),
    ),
}


def fade(dur, target):
    num_frames = int(dur * TIMESCALE * FPS)
    if num_frames == 0:
        num_frames = 1
    step_size = (target - led.value) / num_frames
    for i in range(num_frames):
        new_value = led.value + step_size
        if new_value < MIN_BRIGHTNESS:
            new_value = MIN_BRIGHTNESS
        if new_value > MAX_BRIGHTNESS:
            new_value = MAX_BRIGHTNESS
        led.value = new_value
        time.sleep(DELAY)


led.value = MIN_BRIGHTNESS

for name, lightcurve in lightcurves.items():
    print(name)
    for i in range(REPEATS):
        for duration, target in lightcurve:
            fade(duration, target)
