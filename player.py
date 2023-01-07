from pygame import *

WHITE = (255, 255, 255)

class player(sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = Surface([width, height])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        
        draw.rect(self.image, color, [0, 0, width, height])
        
        self.rect = self.image.get_rect()
    
    def moveRight(self, pixels):
        self.rect.x += pixels
    
    def moveLeft(self, pixels):
        self.rect.x -= pixels
    
    def moveUp(self, pixels):
        self.rect.y -= pixels
    
    def moveDown(self, pixels):
        self.rect.y += pixels