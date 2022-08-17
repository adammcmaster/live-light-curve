import math
import random


FPS = 25
DELAY = 1 / FPS
TIMESCALE = 10
MIN_BRIGHTNESS = 0.1
MAX_BRIGHTNESS = 1.0


class LightcurveGenerator(object):
    PULSATOR = (
        (0.5, 0),
        (0.4, 1),
        (1, 0),
        # (0.2, 0),
    )
    ECLIPSING = (
        (0.7, 1),
        (0.6, 1),
        (0.8, 0.5),
        (0.3, 0.5),
    )
    LENSING = (
        (0.5, 0),
        (0.6, 0.9),
        (0.7, 0),
        #   (0.2, 0),
    )

    @classmethod
    def random(cls):
        while True:
            gen = cls(random.choice((cls.PULSATOR, cls.ECLIPSING, cls.LENSING)))
            print(gen.lc_type)
            for val in gen.repeat():
                yield val

    def __init__(
        self, lc_type, fps=25, timescale=10, min_brightness=0.1, max_brightness=1.0
    ):
        self.lc_type = lc_type
        self.fps = fps
        self.delay = 1 / fps
        self.timescale = timescale
        self.max_brightness = max_brightness
        self.min_brightness = min_brightness
        self.value = 0

    def fade(self, dur, target):
        num_frames = int(dur * self.timescale * self.fps)
        if num_frames == 0:
            num_frames = 1
        step_size = (target - self.value) / num_frames
        for i in range(num_frames):
            new_value = self.value + step_size
            if new_value < self.min_brightness:
                new_value = self.min_brightness
            if new_value > self.max_brightness:
                new_value = self.max_brightness
            self.value = new_value
            yield self.value

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
            yield self.value + (delta * sigmoid(SIG_MIN + (x * step_size)))

        self.value = target
        yield self.value

    def repeat(self, num_repeats=3):
        for i in range(num_repeats):
            for duration, target in self.lc_type:
                for val in self.fade_curve(duration, target):
                    yield val
        for val in self.fade_curve(1, 0):
            yield val
