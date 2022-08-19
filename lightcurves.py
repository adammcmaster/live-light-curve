import math
import random
import time

from inputoutput import (
    main_led,
    green_led,
    red_led,
    exoplanet_button,
    rotator_button,
    lensing_button,
    shuffle_button,
)


FPS = 25
DELAY = 1 / FPS
TIMESCALE = 10
MIN_BRIGHTNESS = 0.1
MAX_BRIGHTNESS = 0.9


class LightcurveGenerator(object):
    ROTATOR = (
        "Rotator",
        (1.5, 0.3),
        (1.5, 0.7),
    )
    EXOPLANET = (
        "Exoplanet",
        (1, 1),
        (0.8, 0.5),
        (0.3, 0.5),
        (0.8, 1),
    )
    LENSING = (
        "Lensing",
        (1, 0),
        (0.6, 1),
        (0.6, 0),
    )

    @classmethod
    def random(cls):
        while True:
            gen = cls(random.choice((cls.ROTATOR, cls.EXOPLANET, cls.LENSING)))
            for val in gen.repeat():
                yield val

    def __init__(
        self,
        lc_type=None,
        init_value=0,
        fps=25,
        timescale=10,
        min_brightness=0.1,
        max_brightness=1.0,
    ):
        if lc_type is None:
            self.shuffle()
        else:
            self.lc_type = lc_type
        self.fps = fps
        self.delay = 1 / fps
        self.timescale = timescale
        self.max_brightness = max_brightness
        self.min_brightness = min_brightness
        self.value = init_value
        self.init_value = init_value
        self.reset_flag = False

        shuffle_button.when_pressed = self.shuffle
        exoplanet_button.when_pressed = lambda: self.guess(self.EXOPLANET)
        rotator_button.when_pressed = lambda: self.guess(self.ROTATOR)
        lensing_button.when_pressed = lambda: self.guess(self.LENSING)

    def shuffle(self):
        lc_type = random.choice((self.ROTATOR, self.EXOPLANET, self.LENSING))
        print("Selected", self.lc_type[0])
        self.reset_flag = True

    def guess(self, lc_type):
        print('Guessed', lc_type[0])
        if lc_type == self.lc_type:
            print('Correct guess')
            green_led.blink(on_time=10, n=1)
        else:
            print('Incorrect guess')
            red_led.blink(on_time=10, n=1)

    def fade_curve(self, dur, target):
        if target > self.max_brightness:
            target = self.max_brightness
        if target < self.min_brightness:
            taregt = self.min_brightness

        delta = target - self.value

        num_frames = int(dur * self.timescale * self.fps)
        if num_frames == 0:
            num_frames = 1

        SIG_MIN = -6
        SIG_MAX = 6

        step_size = (SIG_MAX - SIG_MIN) / num_frames

        def sigmoid(x):
            return 1 / (1 + math.exp(-x))

        for x in range(num_frames):
            new_val = self.value + (delta * sigmoid(SIG_MIN + (x * step_size)))
            main_led.value = new_val
            yield new_val

        self.value = target
        main_led.value = self.value
        yield self.value

    def repeat(self):
        while True:
            for duration, target in self.lc_type[1:]:
                if self.reset_flag:
                    self.reset_flag = False
                    break
                for val in self.fade_curve(duration, target):
                    main_led.value = val
                    yield val

        for val in self.fade_curve(1, self.init_value):
            main_led.value = val
            yield val
