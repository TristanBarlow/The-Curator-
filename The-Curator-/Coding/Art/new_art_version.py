import pygame, sys, time, random, math
from pygame.locals import *

pygame.init()

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

spawn_timer = 0
spawn_time = 150
last_milestone = 0
score = 0
level = 0

player_scale = (100, 100)
raptor_scale = (150, 150)

player_standing = pygame.transform.scale(pygame.image.load('player_new_standing.png'), player_scale)
player_walking1 = pygame.transform.scale(pygame.image.load('player_walk_lfb.png'), player_scale)
player_walking2 = pygame.transform.scale(pygame.image.load('player_walk_lff.png'), player_scale)
player_jacket = pygame.transform.scale(pygame.image.load('player_side_jacket_reach.png'), player_scale)
player_rifle_stand = pygame.transform.scale(pygame.image.load('player_side_stand_rifle.png'), player_scale)
player_rifle_walk1 = pygame.transform.scale(pygame.image.load('player_side_run_lff_rifle.png'), player_scale)
player_rifle_walk2 = pygame.transform.scale(pygame.image.load('player_side_run_lfb_rifle.png'), player_scale)

player_walking = [player_walking1, player_walking2]
player_rifle_walking = [player_rifle_walk1, player_rifle_walk2]
player_rifle_equip = [player_standing, player_jacket, player_rifle_stand]

raptor_standing = pygame.transform.scale(pygame.image.load('rap_side_stand.png'), raptor_scale)
raptor_attack = pygame.transform.scale(pygame.image.load('rap_side_attack.png'), raptor_scale)
raptor_dead = pygame.transform.scale(pygame.image.load('rap_dead.png'), raptor_scale)
raptor_run1 = pygame.transform.scale(pygame.image.load('rap_side_run1.png'), raptor_scale)
raptor_run2 = pygame.transform.scale(pygame.image.load('rap_side_run2.png'), raptor_scale)
raptor_run3 = pygame.transform.scale(pygame.image.load('rap_side_run3.png'), raptor_scale)
raptor_run4 = pygame.transform.scale(pygame.image.load('rap_side_run4.png'), raptor_scale)
raptor_run5 = pygame.transform.scale(pygame.image.load('rap_side_run5.png'), raptor_scale)
raptor_walk1 = raptor_run1
raptor_walk2 = raptor_run3
raptor_walk3 = raptor_run4

raptor_walking = [raptor_walk1, raptor_walk2, raptor_walk3]
raptor_running = [raptor_run1, raptor_run2, raptor_run3, raptor_run4, raptor_run5]
raptor_attack = [raptor_standing, raptor_attack]

# for x in xrange (1, 6):
#    raptor_images.append(pygame.image.load('rap_side_run%i.png'%x))

movement_speed = 5
animation_frame_step = 10


class Controls:
    """Controls"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move_up(self):
        self.y += movement_speed

    def move_down(self):
        self.y += -movement_speed

    def move_left(self):
        self.x += movement_speed

    def move_right(self):
        self.x += -movement_speed

# Controls dictionary
controls = {'w' : Controls.move_up,
            's' : Controls.move_down,
            'a' : Controls.move_left,
            'd' : Controls.move_right}


def animator(asset):
    """animator function, maybe swap to pyganim"""
    asset.keyframe += 1
    if asset.keyframe == animation_frame_step:
        asset.keyframe = 0
        asset.animation_frame += 1
        if asset.animation_frame == asset.image_list.__len__():
            asset.animation_frame = 0
    return asset.image_list[asset.animation_frame]


class Player:
    """player class"""
    def __init__(self, image_list, x, y):
        self.x = x
        self.y = y
        self.keyframe = 0
        self.animation_frame = 0
        self.image_list = image_list
        self.image = player_standing

    def standing(self):
        self.keyframe = 0
        self.animation_frame = 0
        self.image = self.image_list[0]


class Raptor:
    """Raptor class"""
    def __init__(self, image_list, x, y):
        self.x = x
        self.y = y
        self.keyframe = 0
        self.animation_frame = 0
        self.image_list = image_list
        self.image = raptor_standing

    def standing(self):
        self.keyframe = 0
        self.animation_frame = 0
        self.image = self.image_list[0]

    def advance(self, player):
        difference_x = player.x - self.x
        difference_y = player.y - self.y
        self.x += int(difference_x / 100)
        self.y += int(difference_y / 100)


# initiate enemy list
enemies = [Raptor(raptor_running, WINDOW_WIDTH, WINDOW_HEIGHT / 2)]
player = Player(player_rifle_walking, 0, 0)


while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # advance enemies
    for i in xrange(0, enemies.__len__() - 1):
        enemies[i].image = pygame.transform.flip(animator(enemies[i]), True, False)
        enemies[i].advance(player)

    # check timer to spawn
    if spawn_timer == spawn_time:
        enemies.append(Raptor(raptor_running, random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)))
        spawn_timer = 0
        if score - last_milestone == 10:
            print('up a level')
            level += 1
            spawn_time += -15
            last_milestone = score
    else:
        spawn_timer += 1

    # controls
    if event.type == pygame.KEYDOWN:
        key_pressed = pygame.key.name(event.key)
        if key_pressed in controls:
            controls[key_pressed]()

    window.fill((255, 255, 255))

    for i in xrange(0, enemies.__len__() - 1):
        window.blit(enemies[i].image, (enemies[i].x, enemies[i].y))

    player.image = animator(player)
    window.blit(player.image, (player.x, player.y))

    pygame.display.update()

    clock = pygame.time.Clock()
    clock.tick(60)