from pygame import *

WHITE = (255, 255, 255)

class Polygon(sprite.Sprite):
    def __init__(self, screen, color, points):
        # initialize sprite
        super().__init__()
        
        # create image from polygon points
        self.image = Surface(screen.get_size(), SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        draw.polygon(self.image, color, points)
        
        # set rect to the bounding rect of the polygon
        self.rect = self.image.get_bounding_rect()
