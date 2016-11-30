import pygame, sys, time, random, math, map, load, titlescreen
from pygame.locals import *

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

#TITLE SCREEN LOOP set 4th argument to False to not get title screen.
Title_Choice = titlescreen.TitleScreen(WINDOW,WINDOW_WIDTH,WINDOW_HEIGHT,True)
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



RAPTOR_ATTACK_DISTANCE = 20
ANIMATION_FRAME_STEP = 10
player_health = 100
bullets = []
bullet_size = 10
bullet_speed = 100
bullet_colour = 0, 0, 0
PLAYER_POSITION = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
centre_tile = ()


raptor_patrol_positions_one = [(500, 200), (500, 1200)]
raptor_patrol_positions_two = [(1000, 700), (1500, 700), (1500, 100), (1000, 100)]
patrol_speed_one = 200
patrol_speed_two = 100


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
        self.wall_list = []
        self.speed = 4
        self.level_1 = Title_Choice


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
        collision = pygame.Rect((tile_x + self.x, self.y + tile_y),(load.tile_size, load.tile_size))
        self.wall_list.append(collision)

    def floor_blit(self,tile_x, tile_y):
        WINDOW.blit(load.tile_floor, (tile_x + self.x, tile_y + self.y))

    def update_map(self):
        if self.level_1:
            self.map_array = map.map_array_sneak
        else:
            self.map_array = map.map_array_swarm
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

            """
            Return the rectangle colliding with rather than,
            bool
            """

    def update_collider(self,last_key):
        for i in self.wall_list:
            if player_rect.colliderect(i):
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
        self.wall_list = []

    def level_copmlete(self):
        if self.x < -600 and self.x > -750:         # Rough x of map end
            if self.y <-2850 and self.y > -2950:    # Rough y of map end
                print 'hello'
                self.level_1 = False                # Ends level_1

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
        self.dead = False


    def standing(self):
        self.keyframe = 0
        # so when the animation sequence starts it begins from the first frame
        self.animation_frame = 1
        self.image = self.image_list[0]

    def health_bar(self, level_map):
        pygame.draw.rect(WINDOW, (255, 0, 0), (self.x+ level_map.x, self.y + level_map.y,self.health,5))


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

    def move_bullet(self,i, enemies):
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
                    j.dead = True




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

    def update_collider(self, player_position, level_map):
        self.rect = pygame.Rect(self.x+level_map.x, self.y+level_map.y, load.RAPTOR_SCALE[0], load.RAPTOR_SCALE[1])

    def advance(self, player_position, level_map, player_health):
        RAPTOR_SPEED = 7
        difference_x = player_position[0] - self.x - level_map.x
        difference_y = player_position[1] - self.y - level_map.y
        if self.attacking:
            RAPTOR_SPEED = 2
        # stop divide by zero error
        if not self.dead:
            if math.sqrt((math.pow(difference_x, 2) + math.pow(difference_y, 2))) > RAPTOR_ATTACK_DISTANCE:
                normalised_x = difference_x / (math.sqrt((math.pow(difference_x, 2) + math.pow(difference_y, 2))))
                normalised_y = difference_y / (math.sqrt((math.pow(difference_x, 2) + math.pow(difference_y, 2))))
                self.x += normalised_x * RAPTOR_SPEED
                self.y += normalised_y * RAPTOR_SPEED
            else:
                self.attacking = True
                self.image_list = load.raptor_attack

            if difference_x < 0:
                self.look_left = True
            else:
                self.look_left = False

        return player_health


class PatrollingRaptor(Raptor):
    def __init__(self, image_list, patrolling_position_list, patrol_speed, x, y):
        Raptor.__init__(self, image_list, x, y)
        self.patrol_position_list = patrolling_position_list
        self.patrol_timer = 0
        self.patrol_index = 0
        self.next_waypoint = 1
        self.patrol_speed = patrol_speed

    def patrol(self):

        if (self.x, self.y) == self.patrol_position_list[self.next_waypoint]:
            self.patrol_index += 1

        if self.patrol_index == self.patrol_position_list.__len__():
            self.patrol_index = 0

        self.next_waypoint = self.patrol_index + 1

        if self.next_waypoint == self.patrol_position_list.__len__():
            self.next_waypoint = 0

        patrol_path_x = self.patrol_position_list[self.next_waypoint][0] - self.patrol_position_list[self.patrol_index][0]
        patrol_path_y = self.patrol_position_list[self.next_waypoint][1] - self.patrol_position_list[self.patrol_index][1]
        travel_step_x = patrol_path_x / self.patrol_speed
        travel_step_y = patrol_path_y / self.patrol_speed

        self.x += travel_step_x
        self.y += travel_step_y

# initiate enemy list
patrolling_enemies = [PatrollingRaptor(load.raptor_walking, raptor_patrol_positions_one, patrol_speed_one, raptor_patrol_positions_one[0][0], raptor_patrol_positions_one[0][1]),
                      PatrollingRaptor(load.raptor_walking, raptor_patrol_positions_two, patrol_speed_two, raptor_patrol_positions_two[0][0], raptor_patrol_positions_two[0][1])]
enemies = []#[Raptor(load.raptor_running, 1000, 150)] # WINDOW_WIDTH, WINDOW_HEIGHT / 2)]

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

key_pressed = None
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

    # check timer to spawn need to put into a function. Provided level 1 is complete
    if not level_map.level_1:
        if spawn_timer == spawn_time:
           enemies.append(Raptor(load.raptor_running, random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)))
           spawn_timer = 0

        else:
           spawn_timer += 1

    level_map.update_collider(key_pressed)
    level_map.update_map()

    if level_map.level_1:
        for raptor in patrolling_enemies:
            raptor.patrol()
            WINDOW.blit(animator(raptor),(raptor.x + level_map.x, raptor.y + level_map.y))

     # either advance enemies or attacking animation continues


    for enemy in enemies:
        enemy.update_collider(PLAYER_POSITION, level_map)
        if enemy.rect.colliderect(player_rect) and not enemy.dead:
            player_health -= 1
        player_health = enemy.advance((PLAYER_POSITION[0], PLAYER_POSITION[1]), level_map, player_health)
        enemy.image = pygame.transform.flip(animator(enemy), enemy.look_left, False)
        if enemy.health > 0:
            enemy.health_bar(level_map)
        WINDOW.blit(enemy.image,(enemy.x + level_map.x, enemy.y+level_map.y))
    player.image = animator(player)
    WINDOW.blit(face_player_towards_cursor(player.x, mouse_position[0]),
                (player.x - (load.PLAYER_SCALE[0] / 2), player.y))

    #Bullet stuff
    counter = 0
    for i in bullets:
        i.move_bullet(counter, enemies)
        i.update_collider()
        i.draw_bullet()
        counter += 1

    level_map.level_copmlete()

    pygame.draw.rect(WINDOW, (255, 0, 0), (0,20, player_health*2, 10))

    pygame.display.update()
    clock = pygame.time.Clock()
    clock.tick(120)

