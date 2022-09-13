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


def sigmoid(x, num_frames, delta, start):
    SIG_MIN = -6
    SIG_MAX = 6

    step_size = (SIG_MAX - SIG_MIN) / num_frames
    return start + (delta / (1 + math.exp(-(SIG_MIN + (x * step_size)))))


def sinusoid(x, num_frames, delta, start):
    SIN_MIN = 0
    SIN_MAX = 2 * math.pi
    step_size = (SIN_MAX - SIN_MIN) / num_frames
    return 0.5 + math.sin(x * step_size) / 2


def scale_full(x):
    return x


def scale_05(x):
    return x * 0.5 + 0.5


class LightcurveGenerator(object):
    ROTATOR = (
        "Rotator",
        sinusoid,
        scale_05,
        (10, 0),
        (10, 1),
    )
    EXOPLANET = (
        "Exoplanet",
        sigmoid,
        scale_05,
        (10, 1),
        (1, 0),
        (2, 0),
        (1, 1),
    )
    LENSING = (
        "Lensing",
        sigmoid,
        scale_full,
        (5, 0),
        (2, 1),
        (2, 0),
    )

    def __init__(
        self,
        lc_type=None,
        fps=25,
        timescale=1,
        min_brightness=0.05,
        max_brightness=1.0,
        guess_blink_duration=5,
    ):
        self.button_sem = False
        self.lc_type = lc_type
        if self.lc_type is None:
            self.shuffle()
            self.clear_button_sem()

        self.fps = fps
        self.delay = 1 / fps
        self.timescale = timescale
        self.max_brightness = max_brightness
        self.min_brightness = min_brightness
        self.value = self.lc_type[3][1]
        self.guess_blink_duration = guess_blink_duration
        self.reset_flag = False

        shuffle_button.when_pressed = self.shuffle
        exoplanet_button.when_pressed = lambda: self.guess(self.EXOPLANET)
        rotator_button.when_pressed = lambda: self.guess(self.ROTATOR)
        lensing_button.when_pressed = lambda: self.guess(self.LENSING)

        shuffle_button.when_released = self.clear_button_sem
        exoplanet_button.when_released = self.clear_button_sem
        rotator_button.when_released = self.clear_button_sem
        lensing_button.when_released = self.clear_button_sem

    def clear_button_sem(self):
        print("Clearning button_sem")
        self.button_sem = False

    def shuffle(self):
        if self.button_sem:
            print("Skipping duplicate press")
            return
        self.button_sem = True
        green_led.off()
        red_led.off()
        green_led.blink(on_time=0.25, n=3)
        red_led.blink(on_time=0.25, n=3)
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
            print("Skipping duplicate press")
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

        new_val = self.value

        for x in range(num_frames):
            new_val = self.lc_type[1](x, num_frames, delta, self.value)
            main_led.value = new_val
            yield self.lc_type[2](new_val)

        self.value = new_val

    def repeat(self):
        while True:
            for duration, target in self.lc_type[3:]:
                if self.reset_flag:
                    self.reset_flag = False
                    break
                for val in self.fade_curve(duration, target):
                    if self.reset_flag:
                        break
                    yield val
