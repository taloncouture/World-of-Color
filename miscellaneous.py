import pygame
from config import *

class Wall_Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image, player):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(pygame.image.load(image), (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.player = player
    
