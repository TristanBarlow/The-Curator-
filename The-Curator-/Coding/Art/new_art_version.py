import pygame, sys, time, random, math
from pygame.locals import *

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

mouse_position = (WINDOW_WIDTH, WINDOW_HEIGHT)
spawn_timer = 0
spawn_time = 150
last_milestone = 0
score = 0
level = 0
tile_size = 64

PLAYER_SCALE = (200, 200)
RAPTOR_SCALE = (300, 300)

wall = pygame.image.load('Tile_Wall.png')
tile_wall = pygame.transform.scale(wall, (tile_size, tile_size))
floor = pygame.image.load('Cave_floor.png')
tile_floor = pygame.transform.scale(floor, (tile_size, tile_size))

player_standing = pygame.transform.scale(pygame.image.load('player_new_standing.png'), PLAYER_SCALE)
player_walking1 = pygame.transform.scale(pygame.image.load('player_walk_lfb.png'), PLAYER_SCALE)
player_walking2 = pygame.transform.scale(pygame.image.load('player_walk_lff.png'), PLAYER_SCALE)
player_jacket = pygame.transform.scale(pygame.image.load('player_side_jacket_reach.png'), PLAYER_SCALE)
player_rifle_stand = pygame.transform.scale(pygame.image.load('player_side_stand_rifle.png'), PLAYER_SCALE)
player_rifle_walk1 = pygame.transform.scale(pygame.image.load('player_side_run_lff_rifle.png'), PLAYER_SCALE)
player_rifle_walk2 = pygame.transform.scale(pygame.image.load('player_side_run_lfb_rifle.png'), PLAYER_SCALE)

raptor_standing = pygame.transform.scale(pygame.image.load('rap_side_stand.png'), RAPTOR_SCALE)
raptor_attack = pygame.transform.scale(pygame.image.load('rap_side_attack.png'), RAPTOR_SCALE)
raptor_dead = pygame.transform.scale(pygame.image.load('rap_dead.png'), RAPTOR_SCALE)
raptor_run1 = pygame.transform.scale(pygame.image.load('rap_side_run1.png'), RAPTOR_SCALE)
raptor_run2 = pygame.transform.scale(pygame.image.load('rap_side_run2.png'), RAPTOR_SCALE)
raptor_run3 = pygame.transform.scale(pygame.image.load('rap_side_run3.png'), RAPTOR_SCALE)
raptor_run4 = pygame.transform.scale(pygame.image.load('rap_side_run4.png'), RAPTOR_SCALE)
raptor_run5 = pygame.transform.scale(pygame.image.load('rap_side_run5.png'), RAPTOR_SCALE)
raptor_walk1 = raptor_run1
raptor_walk2 = raptor_run3
raptor_walk3 = raptor_run4

player_walking = [player_standing, player_walking1, player_walking2]
player_rifle_walking = [player_rifle_stand, player_rifle_walk1, player_rifle_walk2]
player_rifle_equip = [player_standing, player_jacket, player_rifle_stand]
player_rifle_holster = [player_rifle_stand, player_jacket, player_standing]

raptor_walking = [raptor_standing, raptor_walk1, raptor_walk2, raptor_walk3]
raptor_running = [raptor_standing, raptor_run1, raptor_run2, raptor_run3, raptor_run4, raptor_run5]
raptor_attack = [raptor_standing, raptor_standing, raptor_attack]
raptor_dead_list = [raptor_dead, raptor_dead]

# for x in xrange (1, 6):
#    raptor_images.append(pygame.image.load('rap_side_run%i.png'%x))

PLAYER_SPEED = 4
RAPTOR_SPEED = 7
RAPTOR_ATTACK_DISTANCE = 20
ANIMATION_FRAME_STEP = 10





def check_rifle_equipped(asset):
    """checks for end of rifle equip animation and sets the subsequent image_list"""
    if asset.image_list == player_rifle_equip and asset.animation_frame == 2:  # final animation frame
        asset.image_list = player_rifle_walking
        player.equip_rifle_animation = False
    if asset.image_list == player_rifle_holster and asset.animation_frame == 2:  # final animation frame
        asset.image_list = player_walking
        player.equip_rifle_animation = False


def face_player_towards_cursor(player_x, mouse_x):
    """checks mouse position against player position and faces player towards cursor"""
    delta_x = mouse_x - player_x
    if delta_x < 0:
        return pygame.transform.flip(player.image, True, False)
    else:
        return player.image


def animator(asset):
    """animator function, maybe swap to pyganim"""
    if not asset.moving:
        asset.animation_frame = 0
    else:
        asset.keyframe += 1
        if asset.keyframe == ANIMATION_FRAME_STEP:
            asset.keyframe = 0
            asset.animation_frame += 1
        if asset.animation_frame >= asset.image_list.__len__():
            asset.animation_frame = 1
    check_rifle_equipped(asset)
    return asset.image_list[asset.animation_frame]


class Map:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.map_array =[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2,
                         1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2,
                         1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2,
                         1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2,
                         1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2,
                         1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2,
                         1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2,
                         1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2,
                         1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2,
                         1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2,
                         1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2,
                         1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2,
                         1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2,
                         1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2,
                         1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2,
                         1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2,
                         1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2,
                         1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2,
                         1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2]


    def move_up(self):
        self.y += PLAYER_SPEED

    def move_down(self):
        self.y += -PLAYER_SPEED

    def move_left(self):
        self.x += PLAYER_SPEED

    def move_right(self):
        self.x += -PLAYER_SPEED

    def wall_blit(self,tile_x,tile_y):
        WINDOW.blit(tile_wall, (tile_x + self.x, self.y + tile_y))
        #pygame.Rect((tile_x + moveX, moveY + tile_y), (tile_size, tile_size))

    def floor_blit(self,tile_x, tile_y):
        WINDOW.blit(tile_floor, (tile_x + self.x, tile_y + self.y))


    def update_map(self):
        tile_y = 0
        tile_x = 0
        map_d = {0: self.floor_blit, 1: self.wall_blit, 2: 0}
        for tile in self.map_array:
            if tile == 2:
                tile_y += tile_size
                tile_x = 0
            else:
                command = map_d[tile]
                command(tile_x, tile_y)
                tile_x += tile_size

class Player:
    """player class"""

    def __init__(self, image_list, x, y):
        self.x = x
        self.y = y
        self.keyframe = 0
        self.animation_frame = 0
        self.image_list = image_list
        self.image = self.image_list[0]
        self.look_left = False
        self.moving = True
        self.equip_rifle_animation = False

    def standing(self):
        self.keyframe = 0
        # so when the animation sequence starts it begins from the first frame
        self.animation_frame = 1
        self.image = self.image_list[0]

    def equip_weapon(self):
        """toggles equip/holster image list and starts the animation"""
        self.equip_rifle_animation = True
        if self.image_list == player_walking:
            self.image_list = player_rifle_equip
        elif self.image_list == player_rifle_walking:
            self.image_list = player_rifle_holster


class Raptor:
    """Raptor class"""

    def __init__(self, image_list, x, y):
        self.x = x
        self.y = y
        self.keyframe = 0
        self.animation_frame = 0
        self.image_list = image_list
        self.image = self.image_list[0]
        self.look_left = True
        self.moving = True
        self.attacking = False

    def standing(self):  # is this used? Maybe in sneak section
        self.keyframe = 0
        # so when the animation sequence starts it begins from the first frame
        self.animation_frame = 1
        self.image = self.image_list[0]

    def advance(self, player):
        difference_x = player.x - self.x
        difference_y = player.y - self.y

        # stop divide by zero error
        if math.sqrt((math.pow(difference_x, 2) + math.pow(difference_y, 2))) > RAPTOR_ATTACK_DISTANCE:
            normalised_x = difference_x / (math.sqrt((math.pow(difference_x, 2) + math.pow(difference_y, 2))))
            normalised_y = difference_y / (math.sqrt((math.pow(difference_x, 2) + math.pow(difference_y, 2))))
            self.x += normalised_x * RAPTOR_SPEED
            self.y += normalised_y * RAPTOR_SPEED
        else:
            # initiate attacking
            self.attacking = True
            self.image_list = raptor_attack

        if difference_x < 0:
            self.look_left = True
        else:
            self.look_left = False


# initiate enemy list
enemies = [Raptor(raptor_running, WINDOW_WIDTH, WINDOW_HEIGHT / 2)]

# create player
player = Player(player_walking, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)

# create map
level_map = Map(0, 0)



# Controls dictionary
controls = {'w': level_map.move_up,
            's': level_map.move_down,
            'a': level_map.move_left,
            'd': level_map.move_right,
            'e': player.equip_weapon}

print 'wasd controls, e to equip/holster weapon, player faces mouse cursor'


while True:
    WINDOW.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.mouse.set_cursor(*pygame.cursors.broken_x)
            mouse_position = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            enemies[enemies.__len__() - 1].image_list = raptor_dead_list

    # either advance enemies or attacking animation continues
    for i in xrange(0, enemies.__len__()):
        if not enemies[i].attacking:
            enemies[i].advance(player)
        enemies[i].image = pygame.transform.flip(animator(enemies[i]), enemies[i].look_left, False)

    # check timer to spawn   need to put into a function. Actually this is just for demo
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
    level_map.update_map()
    # controls
    if event.type == pygame.KEYDOWN:
        key_pressed = pygame.key.name(event.key)
        if key_pressed in controls:
            player.moving = True
            controls[key_pressed]()



    # to allow rifle equip animation without interruption
    elif not player.equip_rifle_animation:
        player.moving = False

    # Display


    for i in xrange(0, enemies.__len__()):
        WINDOW.blit(enemies[i].image, (enemies[i].x, enemies[i].y))

    player.image = animator(player)
    WINDOW.blit(face_player_towards_cursor(player.x, mouse_position[0]), (player.x - (PLAYER_SCALE[0] / 2),
                                                                          player.y))  # blit position is adjusted to centre of image instead of top left corner


    pygame.display.update()

    clock = pygame.time.Clock()
    clock.tick(120)
