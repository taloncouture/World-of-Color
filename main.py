#671 Lines of Code


import pygame
import sys
from config import *
from player import *
from obstacle import *
from levels import *
from spikes import *
from ladder import *
from door import *
from miscellaneous import *
from item import *

pygame.mixer.pre_init()
pygame.mixer.init()
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('World of Color')
clock = pygame.time.Clock()
game_font = pygame.font.Font('fonts/unlearne.ttf', 120)
subtitle_font = pygame.font.Font('fonts/unlearne.ttf', 50)
heart = pygame.transform.scale(pygame.image.load('graphics/heart.png'), (int(TILESIZE / 2), int(TILESIZE / 2)))

jump_sound = pygame.mixer.Sound('sounds/jump.wav')
lost_life_sound = pygame.mixer.Sound('sounds/lost_life.wav')
game_over_sound = pygame.mixer.Sound('sounds/game_over.wav')
click_sound = pygame.mixer.Sound('sounds/click.wav')

player_group = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()
hazard_group = pygame.sprite.Group()
ladder_group = pygame.sprite.Group()
door_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()

game_active = False
game_over = False

current_level = level_1
level_index = 0

player_start_x = PLAYER_START_X
player_start_y = PLAYER_START_Y

player = Player(TILESIZE * PLAYER_START_X, TILESIZE * PLAYER_START_Y, TILESIZE, TILESIZE, player_start_x, player_start_y, obstacle_group, hazard_group, ladder_group, door_group, wall_group)
player_group.add(player)

def erase():
    for obstacle in obstacle_group:
        obstacle.kill()
    for hazard in hazard_group:
        hazard.kill()
    for ladder in ladder_group:
        ladder.kill()
    for door in door_group:
        door.kill()
    for object in wall_group:
        object.kill()
    for item in item_group:
        item.kill()

def create_level(): 

    erase()

    for y in range(len(current_level)):
        for x in range(len(current_level[y])):
            if current_level[y][x] == '2' or current_level[y][x] == '1':
                obstacle = Obstacle(TILESIZE * x, TILESIZE * y, TILESIZE, TILESIZE, TileID(current_level[y][x]))
                obstacle_group.add(obstacle)
            elif current_level[y][x] == 'w':
                hazard = Spikes(TILESIZE * x, TILESIZE * y, TILESIZE, TILESIZE, TileID(current_level[y][x]), player, create_level, lost_life_sound)
                hazard_group.add(hazard)
            elif current_level[y][x] == 'H':
                ladder = Ladder(TILESIZE * x, TILESIZE * y, TILESIZE, TILESIZE, TileID(current_level[y][x]), player)
                ladder_group.add(ladder)
            elif current_level[y][x] == 'D':
                door = Door(TILESIZE * x, TILESIZE * y, TILESIZE, TILESIZE, TileID(current_level[y][x]), player)
                door_group.add(door)
            elif current_level[y][x] == 'C':
                closed_door = Wall_Object(TILESIZE * x, TILESIZE * y, TILESIZE, TILESIZE, TileID(current_level[y][x]), player)
                wall_group.add(closed_door)
                player.rect.x = x * TILESIZE
                player.rect.y = y * TILESIZE
            elif current_level[y][x] == 'X':
                item = Item(TILESIZE * x, TILESIZE * y, TILESIZE, TILESIZE, TileID(current_level[y][x]), player)
                item_group.add(item)
            

create_level()

def start_menu():
    screen.fill((70, 70, 70))
    keys = pygame.key.get_pressed()
    title_message = game_font.render('World of Color', False, (255, 255, 255))
    title_message_rect = title_message.get_rect(center = (WIDTH / 2, HEIGHT / 2))
    play_message = subtitle_font.render(' > Press Space To Start < ', False, (255, 255, 255))
    play_message_rect = play_message.get_rect(center = (WIDTH / 2, (HEIGHT / 2 + HEIGHT / 8)))
    screen.blit(title_message, title_message_rect)
    screen.blit(play_message, play_message_rect)

    if keys[pygame.K_SPACE]:
        pygame.mixer.Sound.play(click_sound)
        return True
    return False

def end_screen():
    if player.lives > 0:
        screen.fill((70, 70, 70))
        title_message = game_font.render('You Win!', False, (255, 255, 255))
        title_message_rect = title_message.get_rect(center = (WIDTH / 2, HEIGHT / 2))
        play_message = subtitle_font.render('The color wheel has', False, (255, 255, 255))
        play_message2 = subtitle_font.render('restored color to the world.', False, (255, 255, 255))
        play_message_rect = play_message.get_rect(center = (WIDTH / 2, (HEIGHT / 2 + HEIGHT / 8)))
        play_message2_rect = play_message2.get_rect(center = (WIDTH / 2, (HEIGHT / 2 + HEIGHT / 8 + HEIGHT / 16)))
        screen.blit(title_message, title_message_rect)
        screen.blit(play_message, play_message_rect)
        screen.blit(play_message2, play_message2_rect)
    else:
        screen.fill((70, 70, 70))
        title_message = game_font.render('Game Over', False, (255, 255, 255))
        title_message_rect = title_message.get_rect(center = (WIDTH / 2, HEIGHT / 2))
        screen.blit(title_message, title_message_rect)



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if game_active and player.lives > 0:
        
        if player.rect.y > HEIGHT:
            pygame.mixer.Sound.play(lost_life_sound)
            player.player_kill()
            create_level()


        screen.fill((200, 200, 210))
        obstacle_group.draw(screen)
        wall_group.draw(screen)
        ladder_group.draw(screen)
        door_group.draw(screen)
        item_group.draw(screen)
        player_group.draw(screen)
        hazard_group.draw(screen)


        try:
            for door in door_group:
                if door.rect.colliderect(player.rect):
                    keys = pygame.key.get_pressed()

                    if keys[pygame.K_UP]:
                        pygame.mixer.Sound.play(click_sound)
                        level_index += 1
                        current_level = levels[level_index]
                        create_level()
        except:
            pass

        try:

            for item in item_group:
                if item.rect.colliderect(player.rect):
                    item.kill()
                    game_over = True
                    game_active = False
        except:
            pass


        for lives in range(player.lives):
            screen.blit(heart, ((TILESIZE / 2 * lives) + (HEART_MARGIN * lives) + HEART_MARGIN, HEART_MARGIN))
            

        player_group.update()
        hazard_group.update()

        keys = pygame.key.get_pressed()
        if player.grounded and keys[pygame.K_UP] and player.is_collision(ladder_group) == False and player.is_collision(door_group) == False and player.is_collision(wall_group) == False:
            pygame.mixer.Sound.play(jump_sound)

        if player.lives <= 0:
            pygame.mixer.Sound.play(game_over_sound)
            game_active = False
            game_over = True

    elif game_active == False:
        if game_over == False:
            start_menu()
            game_active = start_menu()
        else:
            end_screen()
        
    pygame.display.update()
    clock.tick(FPS)