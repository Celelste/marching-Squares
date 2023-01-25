import pygame as pg
import time
import numpy as np
import random
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

#system variables
accuracy = 32
frame_skip = 1
target_fps = 60
threshold = 0
z_increment = 0.002

#define the z variable
z = 0

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
noise = OpenSimplex(random.randint(0, 100000))
empty = np.zeros((int(SCREENWIDTH/accuracy), int(SCREENHEIGHT/accuracy)))

#main loop
while running:
    for event in pg.event.get():
        if event.type==pg.QUIT:
            running=False
        elif event.type==pg.KEYDOWN:
            if event.key==pg.K_ESCAPE:
                running=False
    
    if frame_count % frame_skip == 0:
        z += z_increment * frame_skip
        screen.fill(BLACK)
        current_z = z
        points = empty
        for y in range(len(y_points)):
            for x in range(len(x_points)):
                xs = x_points[x]
                ys = y_points[y]
                n = noise.noise3(xs / 100, ys / 100, z)
                #v = int((points[x][y] + 1) * 128)
                points[int(x)][int(y)] = n
                pg.draw.circle(screen, (0, int((n + 1) * 128), 0), (int(x_points[x]), int(y_points[y])), 1)
        
        for x in range(len(x_points) - 1): 
            for y in range(len(y_points) - 1):
                
                index = 0
                
                x1 = int(x_points[x])
                y1 = int(y_points[y])
                
                x2 = int(x_points[x + 1])
                y2 = int(y_points[y])
                
                x3 = int(x_points[x])
                y3 = int(y_points[y + 1])
                
                x4 = int(x_points[x + 1])
                y4 = int(y_points[y + 1])
                
                half_value = accuracy/ 2
                
                if points[x][y] > threshold:
                    index += 8
                if points[x + 1][y] > threshold:
                    index += 4
                if points[x][y + 1] > threshold:
                    index += 1
                if points[x + 1][y + 1] > threshold:
                    index += 2
                
                match index:
                    case 1:
                        pg.draw.line(screen, (0, 128, 0), (x1, y1 + half_value), (x1 + half_value, y1 + accuracy), 1)
                    case 2:
                        pg.draw.line(screen, (0, 128, 0), (x1 + half_value, y1 + accuracy), (x1 + accuracy, y1 + half_value), 1)
                    case 3:
                        pg.draw.line(screen, (0, 128, 0), (x1, y1 + half_value), (x1 + accuracy, y1 + half_value), 1)
                    case 4:
                        pg.draw.line(screen, (0, 128, 0), (x1 + half_value, y1), (x1 + accuracy, y1 + half_value), 1)
                    case 5:
                        pg.draw.line(screen, (0, 128, 0), (x1, y1 + half_value), (x1 + half_value, y1), 1)
                        pg.draw.line(screen, (0, 128, 0), (x1 + half_value, y1 + accuracy), (x1 + accuracy, y1 + half_value), 1)
                    case 6:
                        pg.draw.line(screen, (0, 128, 0), (x1 + half_value, y1), (x1 + half_value, y1 + accuracy), 1)
                    case 7:
                        pg.draw.line(screen, (0, 128, 0), (x1, y1 + half_value), (x1 + half_value, y1), 1)
                    case 8:
                        pg.draw.line(screen, (0, 128, 0), (x1, y1 + half_value), (x1 + half_value, y1), 1)
                    case 9:
                        pg.draw.line(screen, (0, 128, 0), (x1 + half_value, y1), (x1 + half_value, y1 + accuracy), 1)
                    case 10:
                        pg.draw.line(screen, (0, 128, 0), (x1, y1 + half_value), (x1 + half_value, y1 + accuracy), 1)
                        pg.draw.line(screen, (0, 128, 0), (x1 + half_value, y1), (x1 + accuracy, y1 + half_value), 1)
                    case 11:
                        pg.draw.line(screen, (0, 128, 0), (x1 + half_value, y1), (x1 + accuracy, y1 + half_value), 1)
                    case 12:
                        pg.draw.line(screen, (0, 128, 0), (x1, y1 + half_value), (x1 + accuracy, y1 + half_value), 1)
                    case 13:
                        pg.draw.line(screen, (0, 128, 0), (x1 + half_value, y1 + accuracy), (x1 + accuracy, y1 + half_value), 1)
                    case 14:
                        pg.draw.line(screen, (0, 128, 0), (x1, y1 + half_value), (x1 + half_value, y1 + accuracy), 1)
                    case 15:
                        pass
    
    pg.display.flip()
    
    frame_count += 1
    if frame_count % 10 == 0:
        end_time = time.time()
        fps = frame_count / (end_time - start_time)
        print("FPS: ", round(fps, 3))

    #Number of frames per second e.g. 60
    clock.tick(target_fps)
quit()