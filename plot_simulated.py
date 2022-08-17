import random
import itertools

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


from lightcurves import LightcurveGenerator

DISPLAY_DURATION = 1000


fig, ax = plt.subplots()
plt.axis("off")
(line,) = ax.plot([], [], lw=2)
ax.grid()
xdata, ydata = list(range(DISPLAY_DURATION)), [0 for x in range(DISPLAY_DURATION)]


def init():
    ax.set_ylim(0, 1.2)
    ax.set_xlim(0, DISPLAY_DURATION)
    line.set_data(xdata, ydata)
    return (line,)


def run(newflux):
    ydata.append(newflux)
    del ydata[0]
    line.set_data(xdata, ydata)

    return (line,)


ani = animation.FuncAnimation(
    fig, run, LightcurveGenerator.random(), interval=0.01, init_func=init
)
plt.show()
