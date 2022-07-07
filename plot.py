import random
import itertools

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


from sensor_serial import read_flux

DISPLAY_DURATION = 300


fig, ax = plt.subplots()
plt.axis("off")
(line,) = ax.plot([], [], lw=2)
ax.grid()
xdata, ydata = list(range(DISPLAY_DURATION)), [0 for x in range(DISPLAY_DURATION)]


def init():
    ax.set_ylim(min(ydata), max(ydata))
    ax.set_xlim(0, DISPLAY_DURATION)
    line.set_data(xdata, ydata)
    return (line,)


def run(newflux):
    ydata.append(newflux)
    del ydata[0]
    ax.set_ylim(min(ydata) * 0.8, max(ydata) * 1.2)
    line.set_data(xdata, ydata)

    return (line,)


ani = animation.FuncAnimation(fig, run, read_flux, interval=1, init_func=init)
plt.show()
