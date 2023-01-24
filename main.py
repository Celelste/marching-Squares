import pygame as pg
import time
import numpy as np
from numba import jit
from opensimplex import OpenSimplex

#initialize the engine
pg.init()

#define constants
GREEN = (20, 255, 140)
GREY = (210, 210 ,210)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)
BLUE = (0, 0, 255)

SCREENWIDTH=1920
SCREENHEIGHT=1200
accuracy = 8
target_fps = 2

#good settings: (8,2)

#define the z variable
current_z = 0
z = current_z
fps = 0

#initialize the screen
size = (SCREENWIDTH, SCREENHEIGHT)
screen = pg.display.set_mode(size)
pg.display.set_caption("Marching Squares")
screen.fill(BLACK)

#define the list of all sprites
all_sprites_list = pg.sprite.Group()

#initialize the clock and time
running = True
clock = pg.time.Clock()
start_time = time.time()
frame_count = 0

x_points = np.linspace(0, SCREENWIDTH, int(SCREENWIDTH/accuracy))
y_points = np.linspace(0, SCREENHEIGHT, int(SCREENHEIGHT/accuracy))
noise = OpenSimplex(1)

@jit(parallel=True)
def draw_points():
    global y_points, x_points, z, noise, screen
    for y in y_points:
        for x in x_points:
            n = noise.noise3(x / 100, y / 100, z) # generate a 3D noise value using the x, y, and z coordinates of the point
            v = int((n + 1) * 128) # scale the noise value to a range of 0-255
            pg.draw.circle(screen, (0, v, 0), (int(x), int(y)), 1)

#main loop
while running:
    generate = False
    for event in pg.event.get():
        if event.type==pg.QUIT:
            running=False
        elif event.type==pg.KEYDOWN:
            if event.key==pg.K_ESCAPE:
                running=False
    
    #draw the background
    if current_z != z:
        current_z = z
        draw_points()
        pg.display.flip()
    
    if frame_count % target_fps == 0:
        z += 0.01*target_fps
    
    frame_count += 1
    if frame_count % 10 == 0:
        end_time = time.time()
        fps = frame_count / (end_time - start_time)
        print("FPS: ", fps)
 
    #Number of frames per second e.g. 60
    clock.tick(60)

quit()