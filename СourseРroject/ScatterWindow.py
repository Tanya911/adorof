__author__ = 'Tanya'

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as pyplot
import mpl_toolkits.mplot3d

import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.backend_bases import key_press_handler

n = 100

def randrange(n, vmin, vmax):
    return (vmax-vmin)*np.random.rand(n) + vmin

figure = pyplot.figure(figsize=(8,4), facecolor='w')
ax = figure.gca(projection='3d')

xLabel = ax.set_xlabel('\nX', linespacing=3.2)
yLabel = ax.set_ylabel('\nY', linespacing=3.1)
zLabel = ax.set_zlabel('\nZ', linespacing=3.4)

for c, m, zl, zh in [('r', 'o', -50, -25), ('b', '^', -30, -5)]:
    xs = randrange(n, 23, 50)
    ys = randrange(n, 0, 100)
    zs = randrange(n, zl, zh)
    ax.scatter(xs, ys, zs, c=c, marker=m)

ax.dist = 10

pyplot.show()
