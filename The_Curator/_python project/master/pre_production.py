import pygame, sys, time, random, math, map, load, titlescreen
from pygame.locals import *

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

#TITLE SCREEN LOOP set 4th argument to False to not get title screen.
titlescreen.TitleScreen(WINDOW,WINDOW_WIDTH,WINDOW_HEIGHT,True)
#WHEN TITLE SCREEN ENDS IT CONTINUES

mouse_position = (WINDOW_WIDTH, WINDOW_HEIGHT)
spawn_timer = 0
spawn_time = 150
last_milestone = 0
score = 0
level = 0


PLAYER_SPRITE_POS = ((WINDOW_WIDTH / 2)-25, (WINDOW_HEIGHT / 2)+5)
REAL_PLAYER_SIZE = (40, 90)
player_rect = pygame.Rect(PLAYER_SPRITE_POS, REAL_PLAYER_SIZE)


# for x in xrange (1, 6):
#    raptor_images.append(pygame.image.load('rap_side_run%i.png'%x))

RAPTOR_SPEED = 7
RAPTOR_ATTACK_DISTANCE = 20
ANIMATION_FRAME_STEP = 10
player_health = 100
bullets = []
bullet_size = 10
bullet_speed = 100
bullet_colour = 0, 0, 0
PLAYER_POSITION = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
centre_tile = ()

raptor_patrol_positions_one = [(500, 200), (500, 1200)] # not checked second position yet
patrol_speed = 200


def check_rifle_equipped(asset):
    """checks for end of rifle equip animation and sets the subsequent image_list"""
    if asset.image_list == load.player_rifle_equip and asset.animation_frame == 2:  # final animation frame
        asset.image_list = load.player_rifle_walking
        player.equip_rifle_animation = False
    if asset.image_list == load.player_rifle_holster and asset.animation_frame == 2:  # final animation frame
        asset.image_list = load.player_walking
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
        self.list = []
        self.speed = 4
        self.map_array = map.map_array

    def move_up(self):
        self.y += self.speed

    def move_down(self):
        self.y += -self.speed

    def move_left(self):
        self.x += self.speed

    def move_right(self):
        self.x += -self.speed

    def wall_blit(self,tile_x,tile_y):
        WINDOW.blit(load.tile_wall, (tile_x + self.x, self.y + tile_y))
        collision = pygame.Rect((tile_x + self.x, self.y + tile_y),(load.tile_size, load.tile_size) )
        self.list.append(collision)

    def floor_blit(self,tile_x, tile_y):
        WINDOW.blit(load.tile_floor, (tile_x + self.x, tile_y + self.y))

    def update_map(self):
        tile_y = 0
        tile_x = 0
        map_d = {0: self.floor_blit, 1: self.wall_blit, 2: 0, 9: 0,}
        for tile in self.map_array:
            if tile == 2:
                tile_y += load.tile_size
                tile_x = 0
            elif tile == 9:
                tile_x += load.tile_size
            else:
                command = map_d[tile]
                command(tile_x, tile_y)
                tile_x += load.tile_size

            """find centre tile (x, y)
            for i in xrange(centre_tile[0]-1, centre_tile[0]+1):
                for j in xrange(centre_tile[1]-1, centre_tile[1]+1):
                    # check colliders player vs wall_tile(i, j)"""

    def update_collider(self,last_key):
        for i in self.list:
            if player_rect.colliderect(i):
                print 'hello'
                if last_key == 'w':
                    self.y += -self.speed
                if last_key == 'a':
                    self.x += -self.speed
                if last_key == 's':
                    self.y += self.speed
                if last_key == 'd':
                    self.x += self.speed
                else:
                    pass
        self.list = []


class Actor:
    """Super class for shared fields of player and raptor"""
    def __init__(self, image_list, x, y):
        self.x = x
        self.y = y
        self.keyframe = 0
        self.animation_frame = 0
        self.image_list = image_list
        self.image = self.image_list[0]
        self.look_left = True
        self.moving = True
        self.health = 100

    def standing(self):
        self.keyframe = 0
        # so when the animation sequence starts it begins from the first frame
        self.animation_frame = 1
        self.image = self.image_list[0]

    def health_bar(self, level_map):
        pygame.draw.rect(WINDOW, (255, 0, 0), (self.x+level_map.x, self.y + level_map.y,self.health,5))


class Bullet:
    """Bullet class"""
    def __init__(self, player_position, bullet_direction):
        self.x = player_position[0]
        self.y = player_position[1]
        self.direction = bullet_direction
        self.rect = pygame.Rect(self.x, self.y, bullet_size, bullet_size)

    def fire_bullet(self):
        bullets.append(Bullet((WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2), (normalised_x, normalised_y)))

        enemies[enemies.__len__() - 1].image_list = load.raptor_dead_list

    def move_bullet(self, i, enemies):
        self.x += self.direction[0] * bullet_speed
        self.y += self.direction[1] * bullet_speed
        if self.x < 0 or self.x > WINDOW_WIDTH or self.y < 0 or self.y > WINDOW_HEIGHT:
            bullets.pop(i)

        for j in enemies:
            if self.rect.colliderect(j.rect):
                j.health -= 25
                if j.health < 0:
                    j.image_list = load.raptor_dead_list
                    j.moving = False
                    j.health = 0



    def update_collider(self):
        self.rect = pygame.Rect(self.x, self.y, bullet_size, bullet_size)

    def draw_bullet(self):
        pygame.draw.rect(WINDOW, bullet_colour, self.rect)


class Player(Actor):
    """player class"""

    def __init__(self, image_list, x, y):
        Actor.__init__(self, image_list, x, y)
        self.equip_rifle_animation = False

    def equip_weapon(self):
        """toggles equip/holster image list and starts the animation"""
        self.equip_rifle_animation = True
        if self.image_list == load.player_walking:
            self.image_list = load.player_rifle_equip
        elif self.image_list == load.player_rifle_walking:
            self.image_list = load.player_rifle_holster


class Raptor(Actor):
    """Raptor class"""

    def __init__(self, image_list, x, y):
        Actor.__init__(self, image_list, x, y)
        self.attacking = False
        self.rect = pygame.Rect(self.x, self.y, load.RAPTOR_SCALE[0], load.RAPTOR_SCALE[1])
        self.patrol_timer = 0
        self.patrol_index = 0
        self.next_waypoint = 1

    def update_collider(self, player_position, level_map):
        self.rect = pygame.Rect(self.x+level_map.x, self.y+level_map.y, load.RAPTOR_SCALE[0], load.RAPTOR_SCALE[1])

    def advance(self, player_position, level_map):
        difference_x = player_position[0] - self.x - level_map.x
        difference_y = player_position[1] - self.y - level_map.y

        # stop divide by zero error
        if math.sqrt((math.pow(difference_x, 2) + math.pow(difference_y, 2))) > RAPTOR_ATTACK_DISTANCE:
            normalised_x = difference_x / (math.sqrt((math.pow(difference_x, 2) + math.pow(difference_y, 2))))
            normalised_y = difference_y / (math.sqrt((math.pow(difference_x, 2) + math.pow(difference_y, 2))))
            self.x += normalised_x * RAPTOR_SPEED
            self.y += normalised_y * RAPTOR_SPEED
        else:
            # initiate attacking
            self.attacking = True
            self.image_list = load.raptor_attack

        if difference_x < 0:
            self.look_left = True
        else:
            self.look_left = False

    def patrol(self, position_list, number_of_steps):

        if (self.x, self.y) == position_list[self.next_waypoint]:
            self.patrol_index += 1

        if self.patrol_index == position_list.__len__():
            self.patrol_index = 0

        self.next_waypoint = self.patrol_index + 1

        if self.next_waypoint == position_list.__len__():
            self.next_waypoint = 0

        patrol_path_x = position_list[self.next_waypoint][0] - position_list[self.patrol_index][0]
        patrol_path_y = position_list[self.next_waypoint][1] - position_list[self.patrol_index][1]
        travel_step_x = patrol_path_x / number_of_steps
        travel_step_y = patrol_path_y / number_of_steps

        self.x += travel_step_x
        self.y += travel_step_y
        print self.x, self.y

# initiate enemy list
patrolling_enemies = [Raptor(load.raptor_walking, raptor_patrol_positions_one[0][0], raptor_patrol_positions_one[0][1])]
enemies = [Raptor(load.raptor_running, WINDOW_WIDTH, WINDOW_HEIGHT / 2)]

# create player
player = Player(load.player_walking, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)

# create map
level_map = Map(200, -470)

# Controls dictionary
controls = {'w': level_map.move_up,
            's': level_map.move_down,
            'a': level_map.move_left,
            'd': level_map.move_right,
            'e': player.equip_weapon}

print 'wasd controls, e to equip/holster weapon, player faces mouse cursor'

key_pressed = 0
next_control = None

while True:
    WINDOW.fill((100, 100, 100))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.mouse.set_cursor(*pygame.cursors.broken_x)
            mouse_position = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN and player.image_list == load.player_rifle_walking:
            mouse_delta_x = mouse_position[0] - PLAYER_POSITION[0]
            mouse_delta_y = mouse_position[1] - PLAYER_POSITION[1]

            normalised_x = mouse_delta_x / (math.sqrt((math.pow(mouse_delta_x, 2) + math.pow(mouse_delta_y, 2))))
            normalised_y = mouse_delta_y / (math.sqrt((math.pow(mouse_delta_x, 2) + math.pow(mouse_delta_y, 2))))

            bullets.append(Bullet(PLAYER_POSITION, (normalised_x, normalised_y)))

        # controls
        if event.type == pygame.KEYDOWN:
            key_pressed = pygame.key.name(event.key)
            if key_pressed in controls:
                player.moving = True
                next_control = controls[key_pressed]
        elif event.type == pygame.KEYUP:
            next_control = None



    #controls to run every frame
    if next_control != None:
        next_control()
    # to allow rifle equip animation without interruption
    elif not player.equip_rifle_animation:
        player.moving = False


    # either advance enemies or attacking animation continues
    for i in xrange(0, enemies.__len__()):
        enemies[i].update_collider(PLAYER_POSITION,level_map)
        if not enemies[i].attacking:
            enemies[i].advance((PLAYER_POSITION[0], PLAYER_POSITION[1]), level_map)
        enemies[i].image = pygame.transform.flip(animator(enemies[i]), enemies[i].look_left, False)

    # check timer to spawn   need to put into a function. Actually this is just for demo
    if spawn_timer == spawn_time:
        enemies.append(Raptor(load.raptor_running, random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)))
        spawn_timer = 0
        if score - last_milestone == 10:
            print('up a level')
            level += 1
            spawn_time += -15
            last_milestone = score
    else:
        spawn_timer += 1

    level_map.update_collider(key_pressed)
    level_map.update_map()

    for raptor in patrolling_enemies:
        raptor.patrol(raptor_patrol_positions_one, patrol_speed)
        WINDOW.blit(animator(raptor),(raptor.x + level_map.x, raptor.y + level_map.y))

    for i in xrange(0, enemies.__len__()):
        if enemies[i].health > 0:
            enemies[i].health_bar(level_map)
        WINDOW.blit(enemies[i].image, (enemies[i].x + level_map.x, enemies[i].y + level_map.y))
    player.image = animator(player)
    WINDOW.blit(face_player_towards_cursor(player.x, mouse_position[0]), (player.x - (load.PLAYER_SCALE[0] / 2), player.y))  # blit position is adjusted to centre of image instead of top left corner

    for i in xrange(0, bullets.__len__()-1):
        bullets[i].move_bullet(i, enemies)
        bullets[i].update_collider()
        bullets[i].draw_bullet()

    player.health_bar(level_map)

    pygame.display.update()

    clock = pygame.time.Clock()
    clock.tick(120)
