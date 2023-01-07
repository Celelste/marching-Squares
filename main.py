import pygame as pg
from polygon import Polygon
from player import player

pg.init()
 
GREEN = (20, 255, 140)
GREY = (210, 210 ,210)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)
BLUE = (0, 0, 255)

SCREENWIDTH=500
SCREENHEIGHT=500

size = (SCREENWIDTH, SCREENHEIGHT)
screen = pg.display.set_mode(size)
pg.display.set_caption("Marching Squares")

all_sprites_list = pg.sprite.Group()

polygon1 = Polygon(screen, RED, [(100, 100), (300, 100), (100, 300)])
all_sprites_list.add(polygon1)

player1 = player(BLUE, 20, 20)
all_sprites_list.add(player1)

running = True
clock = pg.time.Clock()

while running:
    for event in pg.event.get():
        if event.type==pg.QUIT:
            running=False
        elif event.type==pg.KEYDOWN:
            if event.key==pg.K_ESCAPE:
                running=False
    
    keys = pg.key.get_pressed()
    if keys[pg.K_a]:
        player1.moveLeft(5)
    if keys[pg.K_d]:
        player1.moveRight(5)
    if keys[pg.K_w]:
        player1.moveUp(5)
    if keys[pg.K_s]:
        player1.moveDown(5)
    
    all_sprites_list.update()
    
    screen.fill(GREY)
    
    all_sprites_list.draw(screen)
    
    #Refresh Screen
    pg.display.flip()
 
    #Number of frames per secong e.g. 60
    clock.tick(60)

quit()