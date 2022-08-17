import math
import random


FPS = 25
DELAY = 1 / FPS
TIMESCALE = 10
MIN_BRIGHTNESS = 0.1
MAX_BRIGHTNESS = 0.9


class LightcurveGenerator(object):
    ROTATOR = (
        (1.5, 0.3),
        (1.5, 0.7),
    )
    EXOPLANET = (
        (1, 1),
        (0.8, 0.5),
        (0.3, 0.5),
        (0.8, 1),
    )
    LENSING = (
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
        lc_type,
        init_value=0,
        fps=25,
        timescale=10,
        min_brightness=0.1,
        max_brightness=1.0,
    ):
        self.lc_type = lc_type
        self.fps = fps
        self.delay = 1 / fps
        self.timescale = timescale
        self.max_brightness = max_brightness
        self.min_brightness = min_brightness
        self.value = init_value
        self.init_value = init_value

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

    def repeat(self, num_repeats=5):
        for i in range(num_repeats):
            for duration, target in self.lc_type:
                for val in self.fade_curve(duration, target):
                    yield val

        for val in self.fade_curve(1, self.init_value):
            yield val
