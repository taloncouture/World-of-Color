import pygame
pygame.mixer.init()
from config import *

class Spikes(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image, player, create_level, lost_life_sound):
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
        self.create_level = create_level
        self.lost_life_sound = lost_life_sound
    
    def update(self):
        if self.player.rect.colliderect(self.rect):
           self.player.player_kill()
           self.create_level()
           pygame.mixer.Sound.play(self.lost_life_sound)
