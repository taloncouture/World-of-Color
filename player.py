import pygame
from config import *
from pygame.math import Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, start_x, start_y, obstacle_group, hazard_group, ladder_group, door_group, wall_group):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.lives = DEFAULT_LIVES

        self.image = pygame.transform.scale(pygame.image.load('graphics/player_idle_right.png'), (self.width, self.height))
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.start_x = start_x
        self.start_y = start_y

        self.velocity = 0
        self.player_gravity = 0
        self.obstacle_group = obstacle_group
        self.hazard_group = hazard_group
        self.ladder_group = ladder_group
        self.door_group = door_group
        self.wall_group = wall_group
        self.direction = Vector2()
        self.grounded = False
        self.walking = False

        self.animation_index = 0
        self.anim_direction = [1, 0]
        self.right_frames = ['graphics/player_right.png', 'graphics/player_idle_right.png']
        self.left_frames = ['graphics/player_left.png', 'graphics/player_idle_left.png']
        self.idle_frames_right = ['graphics/player_idle_right.png']
        self.idle_frames_left = ['graphics/player_idle_left.png']
        self.jump_right_frames = ['graphics/player_jump_right.png']
        self.jump_left_frames = ['graphics/player_jump_left.png']
        self.xscroll = 0
        self.x_offset = self.rect.x

        self.offset = 0

    def update(self):
        self.input()
        self.move()
        self.animate()

    def is_collision(self, group):
        for object in group:
            if object.rect.colliderect(self.rect):
                return True
        return False

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.rect.x >= 0:
            self.velocity = -1
            self.anim_direction[0] = -1
            self.walking = True
        elif keys[pygame.K_RIGHT] and self.rect.right <= WIDTH:
            self.velocity = 1
            self.anim_direction[0] = 1
            self.walking = True
        else:
            self.velocity = 0
            self.walking = False

        if keys[pygame.K_UP] and self.grounded or keys[pygame.K_SPACE]and self.grounded:
            if self.is_collision(self.ladder_group):
                    self.rect.y -= PLAYER_SPEED
            elif self.is_collision(self.door_group) or self.is_collision(self.wall_group):
                pass
            else:
                self.player_gravity = -PLAYER_JUMP


    def animate(self):
        if self.walking == True:
            if self.anim_direction[0] == -1:
                if self.anim_direction[1] == 0:
                    frames = self.left_frames
                else: frames = self.jump_left_frames
            if self.anim_direction[0] == 1:
                if self.anim_direction[1] == 0:
                    frames = self.right_frames
                else: frames = self.jump_right_frames
        else:
            if self.anim_direction[0] == -1:
                if self.anim_direction[1] == 0:
                    frames = self.idle_frames_left
                else: frames = self.jump_left_frames
            if self.anim_direction[0] == 1:
                if self.anim_direction[1] == 0:
                    frames = self.idle_frames_right
                else: frames = self.jump_right_frames

        
        if len(frames) > 1:
            self.image = pygame.transform.scale(pygame.image.load(frames[int(self.animation_index)]), (self.width, self.height))
            self.animation_index += 0.1
            if self.animation_index >= len(frames):
                self.animation_index = 0
        else:
            self.image = pygame.transform.scale(pygame.image.load(frames[0]), (self.width, self.height))

    def is_grounded(self):
        self.grounded = False
        for obstacle in self.obstacle_group:
            if obstacle.rect.collidepoint((self.rect.x + PLAYER_SPEED, self.rect.y + self.height + PLAYER_SPEED + 1)) or obstacle.rect.collidepoint((self.rect.x + self.width - PLAYER_SPEED, self.rect.y + self.height + PLAYER_SPEED + 1)) or self.is_collision(self.ladder_group):
                self.grounded = True
                self.direction.y = 0
                break

    def move(self):
        self.rect.x += self.velocity * PLAYER_SPEED

        for obstacle in self.obstacle_group:
            if obstacle.rect.colliderect(self.rect):
                if self.velocity == 1:
                    self.rect.right = obstacle.rect.left
                elif self.velocity == -1:
                    self.rect.left = obstacle.rect.right

        for hazard in self.hazard_group:
            if hazard.rect.colliderect(self.rect):
                if self.velocity == 1:
                    self.rect.right = hazard.rect.left
                elif self.velocity == -1:
                    self.rect.left = hazard.rect.right
    
        self.is_grounded()
        self.rect.y += self.player_gravity
        self.offset += self.velocity

        if self.player_gravity < 0:
            self.direction.y = -1
        elif self.player_gravity > 0:
            self.direction.y = 1

        self.anim_direction[1] = self.direction.y

        for obstacle in self.obstacle_group:
            if obstacle.rect.colliderect(self.rect):
                if self.direction.y == 1:
                    self.rect.bottom = obstacle.rect.top
                    self.direction.y = 0
                elif self.direction.y == -1:
                    self.rect.top = obstacle.rect.bottom
                    self.direction.y = 0

        if self.grounded != True:
            self.player_gravity += PLAYER_JUMP_FACTOR
        else:
            self.player_gravity = 0

    def player_kill(self):
        self.lives -= 1

        


        

            
            
            

               

