import random
import itertools

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


DISPLAY_DURATION = 3000
MIN_FLUX = 0
MAX_FLUX = 100


fig, ax = plt.subplots()
(line,) = ax.plot([], [], lw=2)
ax.grid()
xdata, ydata = list(range(DISPLAY_DURATION)), [0 for x in range(DISPLAY_DURATION)]


def data_gen():
    newflux = ydata[-1] + (random.random() * random.choice([1, -1]))
    if newflux < MIN_FLUX:
        yield MIN_FLUX
    elif newflux > MAX_FLUX:
        yield MAX_FLUX
    else:
        yield newflux


def init():
    ax.set_ylim(MIN_FLUX, MAX_FLUX)
    ax.set_xlim(0, DISPLAY_DURATION)
    line.set_data(xdata, ydata)
    return (line,)


def run(newflux):
    ydata.append(newflux)
    del ydata[0]
    xmin, xmax = ax.get_xlim()
    line.set_data(xdata, ydata)

    return (line,)


ani = animation.FuncAnimation(fig, run, data_gen, interval=1, init_func=init)
plt.show()
