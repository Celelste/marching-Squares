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
SCREENHEIGHT=1080

window = pg.display.Info()

#system variables
accuracy = 32 #the density of points, think of as 1/accuracy
target_fps = 60 #the ideal fps
threshold = 0 #threshold for drawing lines !!!DO NOT CHANGE FROM 0 IF INTERPOLATION IS ON!!!
z_increment = 0.25 #how much it changes per frame
fill = True #wether or not to fill in the lines
interpolate = True #wether or not to interpolate the lines

#initialize the screen
size = (window.current_w, window.current_h)
screen = pg.display.set_mode(size)
pg.display.set_caption("Marching Squares")
screen.fill(BLACK)

#misc. variables
running = True
frame_count = 0
z = 0
drawing = -1

#initialize the clock
clock = pg.time.Clock()

#define the points, noise, and an empty array
x_points = np.linspace(0, SCREENWIDTH, int(SCREENWIDTH/accuracy))
y_points = np.linspace(0, SCREENHEIGHT, int(SCREENHEIGHT/accuracy))
noise = OpenSimplex(random.randint(0, 100000))
empty = np.zeros((int(SCREENWIDTH/accuracy), int(SCREENHEIGHT/accuracy)))
points = empty

def draw_wire(v, top, right, bottom, left, index):
    
    '''
    take the index of the configuration and render the corresponding lines
    
    also requires the value and points.
    '''
    
    if index == 1:
        pg.draw.line(screen, (0, v, 0), (bottom), (left), 1) #bottom left
    elif index == 2:
        pg.draw.line(screen, (0, v, 0), (bottom), (right), 1) #bottom right
    elif index == 3:
        pg.draw.line(screen, (0, v, 0), (left), (right), 1) #hor line
    elif index == 4:
        pg.draw.line(screen, (0, v, 0), (top), (right), 1) #top right
    elif index == 5:
        pg.draw.line(screen, (0, v, 0), (top), (left), 1) #top left, bottom right (out)
        pg.draw.line(screen, (0, v, 0), (bottom), (right), 1)
    elif index == 6:
        pg.draw.line(screen, (0, v, 0), (top), (bottom), 1) #vert line
    elif index == 7:
        pg.draw.line(screen, (0, v, 0), (top), (left), 1) #top left out
    elif index == 8:
        pg.draw.line(screen, (0, v, 0), (top), (left), 1) #top left
    elif index == 9:
        pg.draw.line(screen, (0, v, 0), (top), (bottom), 1) #vert line
    elif index == 10:
        pg.draw.line(screen, (0, v, 0), (bottom), (left), 1) #bottom left, top right (out)
        pg.draw.line(screen, (0, v, 0), (top), (right), 1)
    elif index == 11:
        pg.draw.line(screen, (0, v, 0), (top), (right), 1) #top right out
    elif index == 12:
        pg.draw.line(screen, (0, v, 0), (left), (right), 1) #hor line
    elif index == 13:
        pg.draw.line(screen, (0, v, 0), (bottom), (right), 1) #bottom right out
    elif index == 14:
        pg.draw.line(screen, (0, v, 0), (bottom), (left), 1) #bottom left out
    elif index == 15:
        pass #fill):

def draw_fill(x1, y1, x2, y2, v, top, right, bottom, left, index):
    
    top_left = (x1, y1)
    top_right = (x2, y1)
    bottom_left = (x1, y2)
    bottom_right = (x2, y2)
    
    '''
    take the index of the configuration and render the corresponding polygons
    
    also requires the value and points.
    '''
    
    if index != 15:
        pg.draw.rect(screen, (0, 0, v), (x1, y1, x2 - x1, y2 - y1))
    if index == 1:
        pg.draw.polygon(screen, (0, v, 0), (bottom_left, left, bottom)) #bottom left
    elif index == 2:
        pg.draw.polygon(screen, (0, v, 0), (bottom_right, right, bottom)) #bottom right
    elif index == 3:
        pg.draw.polygon(screen, (0, v, 0), (left, right, bottom_right, bottom_left)) #top out
    elif index == 4:
        pg.draw.polygon(screen, (0, v, 0), (top_right, right, top)) #top right
    elif index == 5:
        pg.draw.polygon(screen, (0, v, 0), (top_right, right, bottom, bottom_left, left, top)) #top left, bottom right (out)
    elif index == 6:
        pg.draw.polygon(screen, (0, v, 0), (top_right, top, bottom, bottom_right)) #left out
    elif index == 7:
        pg.draw.polygon(screen, (0, v, 0), (top, top_right, bottom_right, bottom_left, left)) #top left out
    elif index == 8:
        pg.draw.polygon(screen, (0, v, 0), (top_left, top, left)) #top left
    elif index == 9:
        pg.draw.polygon(screen, (0, v, 0), (top_left, top, bottom, bottom_left)) #right out
    elif index == 10:
        pg.draw.polygon(screen, (0, v, 0), (top_left, top, right, bottom_right, bottom, left)) #bottom left, top right (out)
    elif index == 11:
        pg.draw.polygon(screen, (0, v, 0), (top_left, top, right, bottom_right, bottom_left)) #top right out
    elif index == 12:
        pg.draw.polygon(screen, (0, v, 0), (top_left, top_right, right, left)) #bottom out
    elif index == 13:
        pg.draw.polygon(screen, (0, v, 0), (top_left, top_right, right, bottom, bottom_left)) #bottom right out
    elif index == 14:
        pg.draw.polygon(screen, (0, v, 0), (top_left, top_right, bottom_right, bottom, left)) #bottom left out
    elif index == 15:
        pg.draw.rect(screen, (0, v, 0), (x1, y1, x2 - x1, y2 - y1))

while running: #main loop
    frame_count += 1
    dt = clock.tick(target_fps)
    start_time = time.time()
    for event in pg.event.get(): #check keyboard inputs and if the window was closed, if it was closed then end the main loop
        if event.type==pg.QUIT:
            running=False
        elif event.type==pg.KEYDOWN:
            if event.key==pg.K_ESCAPE:
                running=False
            if event.key==pg.K_SPACE:
                drawing *= -1
            if event.key==pg.K_f:
                fill = not fill
            if event.key==pg.K_i:
                interpolate = not interpolate
    
    input_time = time.time()

    screen.fill(BLACK)
    if drawing == -1:
        z += z_increment * dt
        points = empty
        for y in range(len(y_points)):
            for x in range(len(x_points)):
                xs = x_points[x]
                ys = y_points[y]
                
                n = noise.noise3(xs / 100, ys / 100, z / 1000)
                #v = int((points[x][y] + 1) * 128)
                points[int(x)][int(y)] = n
                if fill == False:
                    pg.draw.circle(screen, (0, int((n + 1) * 128), 0), (int(x_points[x]), int(y_points[y])), accuracy/8)
    if drawing == 1:
        pass

    data_time = time.time()
    
    for x in range(len(x_points) - 1): 
        for y in range(len(y_points) - 1):
            index = 0
            x1 = int(x_points[x])
            y1 = int(y_points[y])
            x2 = int(x_points[x + 1])
            y2 = int(y_points[y + 1])
            if interpolate == True:
                v1 = (points[x][y])
                v2 = (points[x + 1][y])
                v3 = (points[x][y + 1])
                v4 = (points[x + 1][y + 1])
                right = (x2, ((((0-v2)/(v4-v2))*(y2-y1)) + y1))
                bottom = (((((0-v3)/(v4-v3))*(x2-x1)) + x1), y2)
                left = (x1, ((((0-v1)/(v3-v1))*(y2-y1)) + y1))
                top = (((((0-v1)/(v2-v1))*(x2-x1)) + x1), y1)
            else:
                x_center = x1 + (x2 - x1)/2
                y_center = y1 + (y2 - y1)/2
                right = (x2, y_center)
                bottom = (x_center, y2)
                left = (x1, y_center)
                top = (x_center, y1)
            v = int((((points[x][y] + points[x + 1][y] + points[x][y + 1] + points[x + 1][y + 1])/4)+ 1) * 128)
            if points[x][y] > threshold:
                index += 8
            if points[x + 1][y] > threshold:
                index += 4
            if points[x][y + 1] > threshold:
                index += 1
            if points[x + 1][y + 1] > threshold:
                index += 2
            
            if fill == False:
                draw_wire(v, top, right, bottom, left, index)
            else:
                draw_fill(x1, y1, x2, y2, v, top, right, bottom, left, index)
    
    draw_time = time.time()

    pg.display.flip() #update the screen

    end_time = time.time()

    if frame_count == 10:

        frame_count = 0

        fps = round(clock.get_fps(), 3)

        frame_time = round(end_time - start_time, 3)

        input_timed = round(input_time - start_time, 3)

        data_timed = round(data_time - input_time, 3)

        draw_timed = round(draw_time - data_time, 3)

        print(f'FPS: {fps}, Frame time: {frame_time}, Input time: {input_timed}, Data time: {data_timed}, Draw time: {draw_timed}')

quit()