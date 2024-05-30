import pygame as pg
import time
import numpy as np
import random
from opensimplex.internals import _noise3, _init
from numba import njit

# initialize the engine
pg.init()

# define constants
GREEN = (20, 255, 140)
GREY = (210, 210, 210)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)
BLUE = (0, 0, 255)

SCREENWIDTH = 2560
SCREENHEIGHT = 1440

window = pg.display.Info()

# system variables
target_fps = 60  # the ideal fps
threshold = 0  # threshold for drawing lines !!!DO NOT CHANGE FROM 0 IF INTERPOLATION IS ON!!!
z_increment = 0.001  # how much it changes per frame
fill = True  # wether or not to fill in the lines
interpolate = True  # wether or not to interpolate the lines
point_density = 100  # in percent
point_density /= 100

# initialize the screen
size = (SCREENWIDTH, SCREENHEIGHT)
screen = pg.display.set_mode(size)
pg.display.set_caption("Marching Squares")
screen.fill(BLACK)

# misc. variables
running = True
frame_count = 0
z = 0
drawing = -1

# initialize the clock
clock = pg.time.Clock()

# define the points, noise, and an empty array
x_points = np.linspace(0, SCREENWIDTH, int(SCREENWIDTH / accuracy))
y_points = np.linspace(0, SCREENHEIGHT, int(SCREENHEIGHT / accuracy))
empty = np.zeros((int(SCREENWIDTH / accuracy), int(SCREENHEIGHT / accuracy)))
points = empty

perm, perm_grad_index3 = _init(seed=16)


@njit(cache=True)
def noise3(x, y, z):
    return _noise3(x, y, z, perm, perm_grad_index3)


def Interpolate(tl, br, x0, x1):
    return x0 + ((1 - tl) / (br - tl)) * (x1 - x0)

while running:  # main loop
    frame_count += 1
    dt = clock.tick(target_fps)
    start_time = time.time()
    for event in pg.event.get():  # event loop
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            if event.key == pg.K_SPACE:
                drawing *= -1
            if event.key == pg.K_f:
                fill = not fill
            if event.key == pg.K_i:
                interpolate = not interpolate

    input_time = time.time()

    screen.fill(BLACK)
    z += z_increment * dt
    points = empty
    for y in range(len(y_points)):
        for x in range(len(x_points)):
            n = noise3(x, y, z)
            points[int(x)][int(y)] = n

    data_time = time.time()

    for x in range(len(x_points) - 1):
        for y in range(len(y_points) - 1):
            index = 0
            x1 = int(x_points[x])
            y1 = int(y_points[y])
            x2 = int(x_points[x + 1])
            y2 = int(y_points[y + 1])
            v1 = (points[x][y])
            v2 = (points[x + 1][y])
            v3 = (points[x][y + 1])
            v4 = (points[x + 1][y + 1])
            right = (x2, ((((0 - v2) / (v4 - v2)) * (y2 - y1)) + y1))
            bottom = (((((0 - v3) / (v4 - v3)) * (x2 - x1)) + x1), y2)
            left = (x1, ((((0 - v1) / (v3 - v1)) * (y2 - y1)) + y1))
            top = (((((0 - v1) / (v2 - v1)) * (x2 - x1)) + x1), y1)

    draw_time = time.time()

    pg.display.flip()  # update the screen

    end_time = time.time()

    if frame_count == 10:
        frame_count = 0

        fps = round(clock.get_fps(), 3)

        frame_time = round(end_time - start_time, 3)

        input_timed = round(input_time - start_time, 3)

        data_timed = round(data_time - input_time, 3)

        draw_timed = round(draw_time - data_time, 3)

        print(
            f'FPS: {fps}, Frame time: {frame_time}, Input time: {input_timed}, Data time: {data_timed}, Draw time: {draw_timed}')

quit()