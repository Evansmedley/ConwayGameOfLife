# Implementation of Conway's Game of Life using a matplotlib FuncAnimation
# Evan Smedley
# August 2021

import time
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib import animation

# Grid Dimensions
X = 50
Y = 25

# This function is called by the FuncAnimation to modify the values in the grid according to the rules of Conway's Game of Life
def step(i):
    change = []
    a = im.get_array()

    # Iterate through all cells in the grid
    for x in range(X):
        for y in range(Y):
            if not (a[y][x] == 2):

                # Identify the coordinates of the 8 pcells of the grid surrounding the cell that we are currently looking at
                neighbour_coords = [(x-1, y-1), (x, y-1), (x+1, y-1), (x-1, y), (x+1, y), (x-1, y+1), (x, y+1), (x+1, y+1)]
                num_living_neighbors = 0

                # Look through all neighbouring cells of the grid, if they are outside of the grid then ignore them
                for i, j in neighbour_coords:
                    if (not (i < 0 or i >= X - 1 or j < 0 or j >= Y - 1)) and a[j][i] == 1:
                        num_living_neighbors += 1

                # If the current cell of the grid is dead (0) and has 3 living neighbours then set it to be alive
                if a[y][x] == 0 and num_living_neighbors == 3:
                    change.append((x, y, 1))

                # If the current cell of the grid is alive and doesn't have 2 or 3 neighbours then set it to be dead
                elif a[y][x] == 1:
                    if num_living_neighbors < 2 or num_living_neighbors > 3:
                        change.append((x, y, 0))

    # Apply all grid changes
    for x, y, val in change:
        a[y][x] = val

    im.set_array(a)

    return [im]

# This function can be used to see the numbers of the grid for debugging
def display_array(array):
    print(pd.DataFrame(data=array))

# Create a figure and a colour map to match the ints in the 2D array to a colour
fig = plt.figure(figsize=(10,10))
cmap = ListedColormap(["white", "green", "green"])
norm = BoundaryNorm([0, 1, 2], cmap.N)

# Create the numpy array that will be used to represent the grid
a = np.array([0] * X * Y, dtype=np.int8).reshape(Y, X)

# blinker (period 2)
#a[2, 4], a[3,4], a[4,4] = 1, 1, 1

# penta-decathlon (oscillator with a period of 15)
a[6, 6], a[7, 6], a[8, 5], a[8, 7], a[9, 6], a[10, 6], a[11, 6], a[12, 6], a[13, 5], a[13, 7], a[14, 6], a[15, 6] = tuple(np.ones(12))

# spaceship
a[9, 44], a[10, 44], a[9, 43], a[10, 43], a[8, 41], a[9, 41], a[10, 41], a[11, 41], a[7, 40], a[8, 40], a[11, 40], a[12, 40], a[6, 39], a[13, 39] = tuple(np.ones(14))
a[6, 37], a[13, 37], a[6, 36], a[8, 36], a[11, 36], a[13, 36], a[9, 35], a[10, 35], a[9, 34], a[10, 34], a[7, 33], a[8, 33], a[11, 33], a[12, 33] = tuple(np.ones(14))

# Get rid of the axis markings
ax = plt.gca()
ax.axes.xaxis.set_visible(False)
ax.axes.yaxis.set_visible(False)

# Convert the numpy array to an AxesImage object
im = plt.imshow(a, interpolation='nearest', cmap=cmap, norm=norm, origin='lower', animated=True)

# Create and display the animation
anim = animation.FuncAnimation(fig, step, frames =200, interval = 200, blit=True)
plt.show()