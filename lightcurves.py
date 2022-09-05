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


class LightcurveGenerator(object):
    ROTATOR = (
        "Rotator",
        (2, 0),
        (2, 1),
    )
    EXOPLANET = (
        "Exoplanet",
        (5, 1),
        (2, 0),
        (3, 0),
        (2, 1),
    )
    LENSING = (
        "Lensing",
        (5, 0),
        (2, 1),
        (2, 0),
    )

    def __init__(
        self,
        lc_type=None,
        init_value=0,
        fps=25,
        timescale=1,
        min_brightness=0.1,
        max_brightness=1.0,
        guess_blink_duration=5,
    ):
        self.button_sem = False
        self.lc_type = lc_type
        if self.lc_type is None:
            self.shuffle()

        self.fps = fps
        self.delay = 1 / fps
        self.timescale = timescale
        self.max_brightness = max_brightness
        self.min_brightness = min_brightness
        self.value = init_value
        self.init_value = init_value
        self.guess_blink_duration = guess_blink_duration
        self.reset_flag = False

        shuffle_button.when_pressed = self.shuffle
        exoplanet_button.when_pressed = lambda: self.guess(self.EXOPLANET)
        rotator_button.when_pressed = lambda: self.guess(self.ROTATOR)
        lensing_button.when_pressed = lambda: self.guess(self.LENSING)

        shuffle_button.when_released = self.clear_button_sem
        exoplanet_button.when_released = lambda: self.clear_button_sem
        rotator_button.when_released = lambda: self.clear_button_sem
        lensing_button.when_released = lambda: self.clear_button_sem

    def clear_button_sem(self):
        self.button_sem = False

    def shuffle(self):
        if self.button_sem:
            return
        self.button_sem = True
        green_led.off()
        red_led.off()
        green_led.blink(on_time=1, n=3)
        red_led.blink(on_time=1, n=3)
        self.lc_type = random.choice(
            [
                lc_type
                for lc_type in (self.ROTATOR, self.EXOPLANET, self.LENSING)
                if lc_type != self.lc_type
            ]
        )
        print("Selected", self.lc_type[0])
        self.reset_flag = True

    def guess(self, lc_type):
        if self.button_sem:
            return
        self.button_sem = True
        print("Guessed", lc_type[0])
        if lc_type == self.lc_type:
            print("Correct guess")
            red_led.off()
            green_led.blink(on_time=self.guess_blink_duration, n=1)
        else:
            print("Incorrect guess")
            green_led.off()
            red_led.blink(on_time=self.guess_blink_duration, n=1)

    def fade_curve(self, dur, target):
        if target > self.max_brightness:
            target = self.max_brightness
        if target < self.min_brightness:
            target = self.min_brightness

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
                    if self.reset_flag:
                        break
                    main_led.value = val
                    yield val

        for val in self.fade_curve(1, self.init_value):
            main_led.value = val
            yield val
